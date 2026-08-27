# Xóa các file rác
Remove-Item -Path "cleanup_temp_files.py" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "issues.md" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "remove_files.py" -Force -ErrorAction SilentlyContinue

# Thêm/Cập nhật các remote repositories
git remote remove origin 2>$null
git remote add origin https://github.com/AI20K-Build-Phase-Cohort-3/P-046.git
git remote remove personal 2>$null
git remote add personal https://github.com/phamkien1917/bookingbot-p046.git

# Chuyển sang nhánh develop
git checkout -B develop

# Thêm tất cả thay đổi
git add .

# Commit
git commit -m "fix: resolve mentor issues (#1 to #6)"

# Push lên cả hai repo nhánh develop
Write-Host "Đang push lên repo chính..."
git push origin develop --force

Write-Host "Đang push lên repo cá nhân..."
git push personal develop --force

Write-Host "Hoàn tất!"
