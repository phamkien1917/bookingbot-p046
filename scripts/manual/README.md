# Kịch bản kiểm thử thủ công

Các script trong thư mục này gọi thẳng API đang chạy (`http://localhost:8000` hoặc
production), nên chúng **không phải** test tự động và cố ý nằm ngoài `tests/`.

Trước đây chúng nằm ở thư mục gốc với tên `test_*.py`, khiến `pytest` thu thập
`test_map.py::test_chat` và treo 120 giây chờ một server không chạy.

Chạy khi cần đối chiếu hành vi thật:

```bash
python scripts/manual/check_map_distance.py      # một lượt hỏi có ràng buộc khoảng cách
python scripts/manual/check_chat_scenarios.py    # bộ kịch bản hội thoại nhiều lượt
python scripts/manual/check_chat_batch.py        # chạy hàng loạt, in bảng tổng hợp
```
