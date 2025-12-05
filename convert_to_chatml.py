#!/usr/bin/env python3
"""
将 JSON 数据文件转换为 ChatML 格式的 JSONL 文件
"""

import json
import argparse
from pathlib import Path
from tqdm import tqdm


def read_prompt_file(prompt_path):
    """读取 prompt.md 文件并提取 system 和 user 部分"""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 提取 system 部分 (第 2-53 行，去掉首行的 "# system")
    system_content = ''.join(lines[1:53]).strip()

    # 提取 user 部分 (第 56-60 行，去掉首行的 "# user")
    user_template = ''.join(lines[55:]).strip()

    return system_content, user_template


def convert_record_to_chatml(record, system_content, user_template):
    """将单条记录转换为 ChatML 格式"""
    # 获取 Code 和 Unit Test 字段
    code = record.get("Code", "")
    unit_test = record.get("Unit Test - (Ground Truth)", "")

    # 将 <CONTEXT> 替换为实际的代码
    user_content = user_template.replace("<CONTEXT>", code)

    # 构建 ChatML 格式
    chatml = {
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": unit_test}
        ]
    }

    return chatml


def count_lines(file_path):
    """计算 JSON 数组中的元素数量"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return len(data)


def convert_file(input_file, output_file, system_content, user_template):
    """转换单个 JSON 文件为 ChatML JSONL 格式"""
    print(f"\n正在转换: {input_file} -> {output_file}")

    # 读取输入 JSON 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_records = len(data)
    success_count = 0
    error_count = 0

    # 逐条处理并写入 JSONL 文件
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for record in tqdm(data, desc="处理进度", unit="条"):
            try:
                chatml = convert_record_to_chatml(record, system_content, user_template)
                # 写入 JSONL 格式（每行一个 JSON 对象）
                out_f.write(json.dumps(chatml, ensure_ascii=False) + '\n')
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"\n错误处理记录: {e}")

    print(f"✓ 完成! 成功: {success_count}, 失败: {error_count}, 总计: {total_records}")
    return success_count, error_count


def main():
    parser = argparse.ArgumentParser(description='将 JSON 数据转换为 ChatML 格式的 JSONL 文件')
    parser.add_argument('--prompt', default='prompt.md', help='prompt.md 文件路径')
    parser.add_argument('--input-dir', default='.', help='输入文件目录')
    parser.add_argument('--output-dir', default='.', help='输出文件目录')
    parser.add_argument('--files', nargs='+',
                        default=['train_data.json', 'test_data.json', 'val_data.json'],
                        help='要转换的文件列表')

    args = parser.parse_args()

    # 读取 prompt 文件
    prompt_path = Path(args.prompt)
    if not prompt_path.exists():
        print(f"错误: prompt 文件不存在: {prompt_path}")
        return

    print(f"读取 prompt 文件: {prompt_path}")
    system_content, user_template = read_prompt_file(prompt_path)
    print(f"✓ System 部分长度: {len(system_content)} 字符")
    print(f"✓ User 模板长度: {len(user_template)} 字符")

    # 转换文件映射
    file_mapping = {
        'train_data.json': 'train_chatml.jsonl',
        'test_data.json': 'test_chatml.jsonl',
        'val_data.json': 'val_chatml.jsonl'
    }

    total_success = 0
    total_error = 0

    # 处理每个文件
    for input_filename in args.files:
        input_path = Path(args.input_dir) / input_filename

        if not input_path.exists():
            print(f"\n⚠ 跳过不存在的文件: {input_path}")
            continue

        # 确定输出文件名
        output_filename = file_mapping.get(input_filename,
                                          input_filename.replace('.json', '_chatml.jsonl'))
        output_path = Path(args.output_dir) / output_filename

        # 转换文件
        success, error = convert_file(input_path, output_path, system_content, user_template)
        total_success += success
        total_error += error

    # 打印总结
    print("\n" + "="*60)
    print("转换完成!")
    print(f"总成功记录数: {total_success}")
    print(f"总失败记录数: {total_error}")
    print("="*60)


if __name__ == '__main__':
    main()
