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

  python sft/binarize_data.py \
    -input_path ./train_chatml.jsonl \
    -output_path ./processed/ \
    -tokenizer_path /public/huggingface-models/Qwen/Qwen3-1.7B/ \
    -workers 64 


export NCCL_IB_DISABLE=1 
# 环境变量，解决显存碎片
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
DATA_PATH="/root/data/UTer/processed/train.npy"
PRETRAINED_MODEL="/public/huggingface-models/Qwen/Qwen3-1.7B"
OUTPUT_DIR="./checkpoints/sft_model/"
bash sft/scripts/sft_qwencoder_with_lora.sh ${DATA_PATH} ${PRETRAINED_MODEL} ${OUTPUT_DIR}