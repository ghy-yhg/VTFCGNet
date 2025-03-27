import json
import os

# 定义输入文件和输出文件路径
input_file = "../data/annotations/train.json"
output_dir = "../data/annotations"
output_file = os.path.join(output_dir, "filtered.json")  # 合成完整路径

try:
    # 1. 读取源 JSON 文件
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 检查数据类型
    if not isinstance(data, list):
        raise ValueError("数据格式错误，期待列表类型的 JSON 数据。")

    # 2. 筛选需要的键值
    filtered_data = []
    for item in data:
        if "answers" in item:  # 确保键存在
            filtered_data.append({"ans": item["answers"]})

    # 3. 确保目标目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 4. 保存为新的 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print(f"新的 JSON 文件已生成：{os.path.abspath(output_file)}")

except FileNotFoundError:
    print(f"文件未找到：{input_file}")
except json.JSONDecodeError:
    print("JSON 文件格式错误，请检查源文件。")
except Exception as e:
    print(f"发生错误：{e}")
