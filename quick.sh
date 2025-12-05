python binarize_data.py \
    --input_path <输入文件路径> \
    --output_path <输出文件路径> \
    --tokenizer_path <tokenizer路径> \
    --max_len <最大长度> \
    --workers <并行进程数> \
    --save_format <保存格式>

  参数说明：
  - --input_path: 输入的 JSONL 文件路径
  - --output_path: 输出文件路径（不含扩展名）
  - --tokenizer_path: Qwen tokenizer 的路径（如
  ./pretrained_models/qwen/Qwen2.5-Coder-7B/）
  - --max_len: 最大序列长度，默认 8192
  - --workers: 并行处理的进程数，默认 1
  - --save_format: 保存格式，支持 .npy（默认）、.jsonl、.mmap

  # 处理验证数据
  python binarize_data.py \
    --input_path ./val_data.json \
    --output_path ./processed/val \
    --tokenizer_path ./pretrained_models/qwen/Qwen2.5-Coder-7B/ \
    --max_len 8192 \
    --workers 64 \
    --save_format .npy

  # 处理测试数据
  python binarize_data.py \
    --input_path ./test_data.json \
    --output_path ./processed/test \
    --tokenizer_path ./pretrained_models/qwen/Qwen2.5-Coder-7B/ \
    --max_len 8192 \
    --workers 64 \
    --save_format .npy