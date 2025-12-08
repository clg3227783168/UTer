import numpy as np

# 你的数据路径
DATA_PATH = "processed/train.npy"

try:
    data = np.load(DATA_PATH, allow_pickle=True)
    print(f"数据总条数: {len(data)}")
    
    # 打印前2条数据看看长什么样
    for i in range(2):
        print(f"\n--- Sample {i} ---")
        print(data[i])
        
    # 检查类型
    print(f"\n数据类型: {type(data[0])}")
    if isinstance(data[0], dict):
        print(f"包含的键: {data[0].keys()}")
except Exception as e:
    print(f"加载失败: {e}")