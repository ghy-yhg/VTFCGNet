import json
import os

# 输入和输出文件路径
input_file = '../data/annotations/test_dev.json'  # 你的原始 train.json 文件路径
output_file = '../data/annotations/test_dev_cws_zh.json'  # 输出的 train_cws_zh.json 文件路径

# 读取原始 JSON 数据
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 用于保存转换后的数据
output_data = []

# 处理每个条目
for item in data:
    # 获取图像路径
    image_name = item['image_name']['image']
    image_local_path = os.path.join('../data/images/test_dev', image_name)  # 根据实际路径调整

    # 获取上下文文本
    context_zh = item['context']['cws']['zh']

    # 获取问题文本
    question_zh = item['question']['cws']['zh']

    # 获取答案
   # answer_zh = item['answers'][0]['answer']['zh']  # 假设每个问题只有一个答案

    # 将数据转化为所需的格式
    output_data.append({
        'image_local_path': image_local_path,
        'text_cws': context_zh,
        'question_cws': question_zh,
        #'answer': answer_zh
    })

# 将生成的数据写入文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f'Generated {output_file} successfully.')
