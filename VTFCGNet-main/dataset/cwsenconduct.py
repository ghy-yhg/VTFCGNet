import json

# 加载 JSON 文件
with open("../data/annotations/train_cws_zh.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 检查数据是否存在缺少的字段
missing_fields = []
for idx, item in enumerate(data):
    if 'image_local_path' not in item:
        missing_fields.append(idx)

if missing_fields:
    print(f"Missing 'image_local_path' in entries at indices: {missing_fields}")
else:
    print("All entries contain 'image_local_path'.")
