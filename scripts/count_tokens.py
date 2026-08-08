#!/usr/bin/env python3
"""Script đếm token cho code và text.
Sử dụng tiktoken (OpenAI tokenizer) hoặc approximate method.

Usage:
    python scripts/count_tokens.py <file_or_text>
    python scripts/count_tokens.py --file src/agents/nodes/respond_node.py
    python scripts/count_tokens.py --text "Xin chào, tôi muốn tìm căn hộ ở quận 7"
    python scripts/count_tokens.py --dir src/
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Approximate tokenizer (không cần API key)
# 1 token ≈ 4 chars cho tiếng Anh, ≈ 2-3 chars cho tiếng Việt
def approximate_token_count(text: str) -> int:
    """Đếm token ước lượng bằng heuristic."""
    if not text:
        return 0

    # Đếm tokens cho tiếng Anh: ~4 chars/token
    english_chars = sum(1 for c in text if ord(c) < 128 and not c.isspace())

    # Đếm tokens cho tiếng Việt: ~2 chars/token (UTF-8 chars > 1 byte)
    vietnamese_chars = len(text) - english_chars - sum(1 for c in text if c.isspace())

    # Rough estimate: English ~4 chars/token, Vietnamese ~2 chars/token
    return int(english_chars / 4 + vietnamese_chars / 2 + len(text.split()) / 1.5)


def tiktoken_token_count(text: str, model: str = "cl100k_base") -> int:
    """Đếm token chính xác hơn bằng tiktoken (OpenAI tokenizer).

    Args:
        text: Text cần đếm
        model: tiktoken encoding model
              - cl100k_base: GPT-4, GPT-3.5, Claude (recommended)
              - p50k_base: Codex models
              - r50k_base: GPT-3 models

    Returns:
        Số token
    """
    try:
        import tiktoken
        encoding = tiktoken.get_encoding(model)
        return len(encoding.encode(text))
    except ImportError:
        print("⚠️ tiktoken chưa được cài đặt. Cài đặt với: pip install tiktoken")
        return approximate_token_count(text)


def count_file(file_path: str, use_tiktoken: bool = True) -> tuple[int, int]:
    """Đếm token trong một file.

    Returns:
        (token_count, line_count)
    """
    path = Path(file_path)
    if not path.exists():
        print(f"❌ File không tồn tại: {file_path}")
        return 0, 0

    content = path.read_text(encoding="utf-8")
    lines = content.count('\n') + 1

    if use_tiktoken:
        tokens = tiktoken_token_count(content)
    else:
        tokens = approximate_token_count(content)

    return tokens, lines


def count_directory(dir_path: str, extensions: list[str] = None, use_tiktoken: bool = True) -> dict:
    """Đếm token trong tất cả file trong thư mục.

    Args:
        dir_path: Đường dẫn thư mục
        extensions: Danh sách extension cần đếm (vd: ['.py', '.md'])
        use_tiktoken: Dùng tiktoken hay approximate

    Returns:
        Dict với thông tin chi tiết
    """
    if extensions is None:
        extensions = ['.py', '.js', '.ts', '.tsx', '.jsx', '.md', '.txt', '.sql']

    path = Path(dir_path)
    if not path.exists() or not path.is_dir():
        print(f"❌ Thư mục không tồn tại: {dir_path}")
        return {}

    results = {
        "total_tokens": 0,
        "total_lines": 0,
        "total_files": 0,
        "files": []
    }

    for ext in extensions:
        for file_path in path.rglob(f"*{ext}"):
            # Bỏ qua node_modules, .venv, __pycache__, v.v.
            skip_dirs = ['node_modules', '.venv', '__pycache__', '.git', '.pytest_cache', 'dist', 'build']
            if any(skip in str(file_path) for skip in skip_dirs):
                continue

            tokens, lines = count_file(str(file_path), use_tiktoken)
            if tokens > 0:
                results["files"].append({
                    "path": str(file_path.relative_to(path)),
                    "tokens": tokens,
                    "lines": lines
                })
                results["total_tokens"] += tokens
                results["total_lines"] += lines
                results["total_files"] += 1

    # Sort by tokens descending
    results["files"].sort(key=lambda x: x["tokens"], reverse=True)

    return results


def format_token_cost(tokens: int, model: str = "claude-opus-5") -> str:
    """Format chi phí token thành text.

    Args:
        tokens: Số token
        model: Model name để tính giá

    Returns:
        String với chi phí ước lượng
    """
    # Giá OpenRouter cho các model phổ biến (per 1M tokens)
    prices = {
        "claude-opus-5": {"input": 15, "output": 75},
        "claude-sonnet-5": {"input": 3, "output": 15},
        "claude-3.5-sonnet": {"input": 3, "output": 15},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "gpt-4o": {"input": 5, "output": 15},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gemma-2-9b": {"input": 0.20, "output": 0.20},  # Free on OpenRouter
        "llama-3-8b": {"input": 0.20, "output": 0.20},  # Free on OpenRouter
    }

    if model not in prices:
        return f"~{tokens:,} tokens (giá model không có trong danh sách)"

    price = prices[model]
    input_cost = tokens * price["input"] / 1_000_000
    output_cost = tokens * price["output"] / 1_000_000

    return f"~{tokens:,} tokens | ~${input_cost:.6f} input | ~${output_cost:.6f} output"


def print_results(results: dict, use_tiktoken: bool, title: str = "Results"):
    """In kết quả đẹp."""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    print(f"📁 Tổng files: {results['total_files']}")
    print(f"📝 Tổng lines: {results['total_lines']:,}")
    print(f"🔢 Tổng tokens: {results['total_tokens']:,}")
    print(f"📊 Tokenizer: {'tiktoken (chính xác)' if use_tiktoken else 'approximate'}")
    print(f"{'='*60}")

    # Top files
    print("\n🔝 Top 10 files nhiều token nhất:")
    print("-" * 60)
    print(f"{'File':<45} {'Tokens':>10} {'Lines':>8}")
    print("-" * 60)

    for i, file_info in enumerate(results["files"][:10], 1):
        rel_path = file_info["path"]
        # Truncate long paths
        if len(rel_path) > 42:
            rel_path = "..." + rel_path[-42:]
        print(f"{i:>2}. {rel_path:<45} {file_info['tokens']:>10,} {file_info['lines']:>8,}")

    # Chi phí
    print(f"\n{'='*60}")
    print("💰 Ước lượng chi phí (OpenRouter):")
    print(f"{'='*60}")

    models_to_check = ["gemma-2-9b", "claude-3-haiku", "claude-3.5-sonnet", "gpt-4o-mini"]
    for model in models_to_check:
        cost_str = format_token_cost(results["total_tokens"], model)
        emoji = "🆓" if "Free" in cost_str or "0.00" in cost_str else "💵"
        print(f"   {emoji} {model:<20} {cost_str}")


def main():
    parser = argparse.ArgumentParser(
        description="Đếm token cho code và text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python scripts/count_tokens.py --file src/agents/nodes/respond_node.py
  python scripts/count_tokens.py --dir src/ --extensions .py .md
  python scripts/count_tokens.py --text "Xin chào, tôi muốn tìm căn hộ"
  python scripts/count_tokens.py --approx src/agents/

Gợi ý: Cài đặt tiktoken để đếm chính xác hơn:
  pip install tiktoken
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", type=str, help="File cần đếm token")
    group.add_argument("--dir", "-d", type=str, help="Thư mục cần đếm token")
    group.add_argument("--text", "-t", type=str, help="Text cần đếm token")

    parser.add_argument(
        "--extensions", "-e", nargs="+", default=['.py', '.js', '.ts', '.tsx', '.md', '.txt'],
        help="Extensions cần đếm (mặc định: .py .js .ts .tsx .md .txt)"
    )
    parser.add_argument(
        "--approx", "-a", action="store_true",
        help="Dùng phương pháp approximate (không cần tiktoken)"
    )
    parser.add_argument(
        "--no-cache", action="store_true",
        help="Không dùng cache"
    )

    args = parser.parse_args()

    use_tiktoken = not args.approx

    if args.text:
        # Đếm token cho text
        text = args.text
        if use_tiktoken:
            tokens = tiktoken_token_count(text)
        else:
            tokens = approximate_token_count(text)

        print(f"\n📝 Input text:")
        print(f"   \"{text}\"")
        print(f"\n🔢 Tokens: {tokens:,}")
        print(f"📊 Chi phí ước lượng:")
        print(f"   {format_token_cost(tokens, 'gemma-2-9b')}")
        print(f"   {format_token_cost(tokens, 'claude-3-haiku')}")
        print(f"   {format_token_cost(tokens, 'gpt-4o-mini')}")

    elif args.file:
        # Đếm token cho một file
        tokens, lines = count_file(args.file, use_tiktoken)
        if tokens > 0:
            print(f"\n📄 File: {args.file}")
            print(f"📝 Lines: {lines:,}")
            print(f"🔢 Tokens: {tokens:,}")
            print(f"📊 Chi phí:")
            print(f"   {format_token_cost(tokens, 'gemma-2-9b')}")
            print(f"   {format_token_cost(tokens, 'claude-3-haiku')}")

    elif args.dir:
        # Đếm token cho thư mục
        results = count_directory(args.dir, args.extensions, use_tiktoken)
        if results:
            print_results(results, use_tiktoken, f"Directory: {args.dir}")


if __name__ == "__main__":
    main()
