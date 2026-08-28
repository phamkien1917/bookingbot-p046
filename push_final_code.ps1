# Xóa các file script tạm (nếu có trên git hoặc local)
git rm --cached push_code.ps1 test_all_scenarios.py -f 2>$null
Remove-Item push_code.ps1, test_all_scenarios.py -ErrorAction SilentlyContinue

# Thêm tất cả thay đổi vào Git
git add .

# Loại bỏ file issues.md khỏi danh sách chuẩn bị commit
git reset HEAD issues.md 2>$null

# Commit các thay đổi (Sửa lỗi context và LLM bypass)
git commit -m "Fix AI context loss and LLM bypass for out-of-scope intents"

# Đẩy code lên nhánh develop của cả 2 repo
git push origin develop
git push personal develop
