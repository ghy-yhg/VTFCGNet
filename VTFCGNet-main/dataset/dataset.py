import glob
import json
import torch
import numpy as np
import torch.utils.data as Data
from torch.utils.data import DataLoader


class DataSet(Data.Dataset):
    def __init__(self, __C, mode='train'):
        lang = __C.LANG
        self.max_context_token = __C.MAX_CONTEXT_TOKEN
        self.max_question_token = __C.MAX_QUESTION_TOKEN
        self.pretrained_emb = np.load(__C.DATASET_PATH + f'annotations/embedding_{lang}.npy')
        self.ans2id = json.load(
            open(__C.DATASET_PATH + f'annotations/ans2id_{lang}.json', 'r', encoding='utf-8')
        )
        self.id2ans = {str(v): k for k, v in self.ans2id.items()}
        self.token2id = json.load(
            open(__C.DATASET_PATH + f'annotations/token2id_{lang}.json', 'r', encoding='utf-8')
        )

        self.mode = mode

        self.data = json.load(
            open(__C.DATASET_PATH + f'annotations/{mode}_cws_{lang}.json', 'r', encoding='utf-8')
        )
        print(f"Data loaded: {self.data}")

        if __C.FEATURE_TYPE == 'image':
            suffix = '.jpg'
        elif __C.FEATURE_TYPE == 'grid':
            self.img_max_token = 608
            suffix = '.npy'
        elif __C.FEATURE_TYPE == 'region':
            self.img_max_token = 100
            suffix = '.npz'

        img_feat_path_list = glob.glob(__C.DATASET_PATH + 'images/{}/*'.format(mode) + suffix)
        self.iid_to_img_path = {
            str(int(p.split('/')[-1].split('_')[-1].split('.')[0])): p for p in img_feat_path_list
        }

        self.token_size = len(self.token2id)
        self.ans_size = len(self.ans2id)

        self.data_size = len(self.data)

        self.__C = __C

    def __getitem__(self, idx):
        print(f"Dataset size: {len(self.data)}")  # 打印数据集的长度，确保索引是有效的
        print(f"Fetching data for index: {idx}")

        # 处理缺少 'image_local_path' 或其他键的情况
        try:
            if 'image_local_path' not in self.data[idx]:
                print(f"Missing 'image_local_path' for index {idx}: {self.data[idx]}")
                return None  # 如果缺少 'image_local_path'，可以选择返回 None 或默认值
        except KeyError as e:
            print(f"KeyError: {e}. Skipping index {idx}.")
            return None  # 捕获 KeyError，跳过该数据条目

        img_id = int(
            self.data[idx]['image_local_path']
            .replace("\\", "/")  # 处理 Windows 路径
            .split('/')[-1]
            .split('_')[-1]
            .split('.')[0]
        )

        # 获取图像特征并处理可能的 KeyError
        try:
            img_feat = self.proc_img(str(img_id), self.img_max_token)
        except KeyError as e:
            print(f"KeyError: {e}. Skipping index {idx}. Image ID {img_id} not found.")
            return None  # 如果找不到对应的图像特征，返回 None 跳过

        # 处理文本数据
        context = self.data[idx]['text_cws']
        context_iter = self.proc_context(context, self.max_context_token)

        question = self.data[idx]['question_cws']
        question_iter = self.proc_ques(question, self.max_question_token)

        if 'test' not in self.mode:
            answer = self.data[idx]['answer']
            answer_iter = self.proc_answer(answer)

            return (
                torch.from_numpy(img_feat),
                torch.from_numpy(context_iter),
                torch.from_numpy(question_iter),
                torch.from_numpy(answer_iter),
            )
        else:
            return (
                torch.from_numpy(img_feat),
                torch.from_numpy(context_iter),
                torch.from_numpy(question_iter),
            )

    def __len__(self):
        return self.data_size

    def proc_img(self, img_id, img_feat_pad_size):
        # 处理图像特征的加载与填充
        if img_id not in self.iid_to_img_path:
            print(f"Image ID {img_id} not found in iid_to_img_path. Returning default feature vector.")
            return np.zeros((img_feat_pad_size, 2048))  # 如果找不到图像ID，返回一个默认的零向量

        path = self.iid_to_img_path[img_id]
        try:
            img_feat = (
                np.load(path).transpose((1, 0))
                if self.__C.FEATURE_TYPE == 'grid'
                else np.load(path)['x'].transpose((1, 0))
            )
        except Exception as e:
            print(f"Error loading image feature for {img_id}: {e}. Returning default feature vector.")
            return np.zeros((img_feat_pad_size, 2048))  # 发生异常时返回默认零向量

        if img_feat.shape[0] > img_feat_pad_size:
            img_feat = img_feat[:img_feat_pad_size]

        img_feat = np.pad(
            img_feat,
            ((0, img_feat_pad_size - img_feat.shape[0]), (0, 0)),
            mode='constant',
            constant_values=0,
        )
        return img_feat

    def proc_context(self, context, max_token):
        context_id = np.zeros(max_token, np.int64)
        ix = 0
        for word in context:
            if word in self.token2id:
                context_id[ix] = self.token2id[word]
            else:
                context_id[ix] = self.token2id['UNK']

            if ix + 1 == max_token:
                break
            ix += 1

        return context_id

    def proc_ques(self, question, max_token):
        question_id = np.zeros(max_token, np.int64)
        ix = 0
        for word in question:
            if word in self.token2id:
                question_id[ix] = self.token2id[word]
            else:
                question_id[ix] = self.token2id['UNK']

            if ix + 1 == max_token:
                break
            ix += 1

        return question_id

    def proc_answer(self, answer):
        ans_score = np.zeros(self.ans2id.__len__(), np.float32)
        if answer in self.ans2id:
            ans_score[self.ans2id[answer]] = 1
        else:
            pass
        return ans_score


# 自定义 collate_fn 函数
def collate_fn(batch):
    # 过滤掉返回 None 的数据
    batch = [item for item in batch if item is not None]

    # 如果批次为空，返回一个空批次（可以根据需求修改）
    if len(batch) == 0:
        return None

    # 使用默认的 collate_fn 将数据合并为一个批次
    return torch.utils.data.dataloader.default_collate(batch)


if __name__ == "__main__":
    from config import Cfgs

    dataset = DataSet(Cfgs())

    # 使用自定义 collate_fn 来创建 DataLoader
    train_loader = DataLoader(
        dataset,
        batch_size=32,
        collate_fn=collate_fn,  # 使用自定义的 collate_fn
        num_workers=4
    )

    # 测试加载第12个数据
    d = dataset[12]
    print(d)
