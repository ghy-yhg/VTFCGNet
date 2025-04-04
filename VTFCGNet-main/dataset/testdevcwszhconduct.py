import json
import os

# 定义输入文件和输出文件路径
input_file = "../data/annotations/test_dev.json"  # 这里是val.json文件
output_dir = "../data/annotations"
output_file = os.path.join(output_dir, "test_dev_cws_zh.json")  # 输出文件

try:
    # 1. 读取源 JSON 文件
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. 提取所有的中文词汇并分配 ID
    word_to_id = {"PAD": 0, "UNK": 1}  # 初始化 PAD 和 UNK
    current_id = 2  # 从 2 开始为词汇分配 ID

    # 3. 遍历每个条目，提取 question 和 context 中的 'zh' 字段
    for item in data:
        # 提取 question 中的中文词汇
        zh_words = item.get("question", {}).get("cws", {}).get("zh", [])
        for word in zh_words:
            # 如果词汇不在映射中，则添加
            if word not in word_to_id:
                word_to_id[word] = current_id
                current_id += 1

        # 提取 context 中的中文词汇
        zh_words = item.get("context", {}).get("cws", {}).get("zh", [])
        for word in zh_words:
            # 如果词汇不在映射中，则添加
            if word not in word_to_id:
                word_to_id[word] = current_id
                current_id += 1

    # 4. 确保目标目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 5. 保存为新的 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(word_to_id, f, indent=4, ensure_ascii=False)

    print(f"新的 JSON 文件已生成：{os.path.abspath(output_file)}")

except FileNotFoundError:
    print(f"文件未找到：{input_file}")
except json.JSONDecodeError:
    print("JSON 文件格式错误，请检查源文件。")
except Exception as e:
    print(f"发生错误：{e}")
