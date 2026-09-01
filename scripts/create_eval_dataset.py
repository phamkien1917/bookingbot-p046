"""Script tạo evaluation dataset từ dữ liệu thực.
Chạy: python scripts/create_eval_dataset.py
"""
import json
from pathlib import Path


def create_eval_dataset():
    """Tạo eval dataset từ FAQ hoặc tài liệu."""
    dataset = {
        "question": [],
        "contexts": [],
        "answer": [],
        "ground_truth": [],
    }

    # Thêm các câu hỏi test — nên đa dạng:
    # - Câu hỏi trực tiếp (factual)
    # - Câu hỏi yêu cầu tổng hợp (multi-hop)
    # - Câu hỏi ngoài phạm vi (out-of-scope)
    # - Câu hỏi mơ hồ (ambiguous)

    test_cases = [
        {
            "question": "Giá vàng SJC hôm nay?",
            "contexts": ["Giá vàng SJC 5.150.000 - 5.200.000đ."],
            "ground_truth": "5.150.000 - 5.200.000đ",
            "category": "factual",
        },
        {
            "question": "So sánh lãi suất gửi tiết kiệm 3 tháng và 6 tháng?",
            "contexts": [
                "Lãi suất 3 tháng: 4.5%/năm.",
                "Lãi suất 6 tháng: 5.0%/năm.",
            ],
            "ground_truth": "3 tháng 4.5%, 6 tháng 5.0% — chênh 0.5%",
            "category": "multi_hop",
        },
        {
            "question": "Thời tiết hôm nay thế nào?",
            "contexts": [],
            "ground_truth": "Không có thông tin về thời tiết.",
            "category": "out_of_scope",
        },
    ]

    for tc in test_cases:
        dataset["question"].append(tc["question"])
        dataset["contexts"].append(tc["contexts"])
        dataset["ground_truth"].append(tc["ground_truth"])
        # Answer sẽ được generate bằng agent thật

    output_path = Path(__file__).resolve().parent.parent / "eval_dataset.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Created dataset with {len(test_cases)} test cases at {output_path}")


if __name__ == "__main__":
    create_eval_dataset()
