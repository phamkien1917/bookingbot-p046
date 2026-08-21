$ErrorActionPreference = "Stop"

if (-not $env:BOOKINGBOT_TEST_EMAIL -or -not $env:BOOKINGBOT_TEST_PASSWORD) {
    throw "Set BOOKINGBOT_TEST_EMAIL and BOOKINGBOT_TEST_PASSWORD for a disposable CUSTOMER account."
}

$apiBase = if ($env:BOOKINGBOT_API_BASE) { $env:BOOKINGBOT_API_BASE.TrimEnd("/") } else { "http://127.0.0.1:8000/api/v1" }
$sessionId = [guid]::NewGuid().ToString()
$webSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession

$loginBody = "username=$([uri]::EscapeDataString($env:BOOKINGBOT_TEST_EMAIL))&password=$([uri]::EscapeDataString($env:BOOKINGBOT_TEST_PASSWORD))"
$login = Invoke-RestMethod -Method Post -Uri "$apiBase/auth/login" -ContentType "application/x-www-form-urlencoded" -Body $loginBody -WebSession $webSession
if ($login.user.role -ne "CUSTOMER") { throw "The test account must have CUSTOMER role" }

function Send-AuthenticatedChat([string]$Message) {
    $body = @{ message = $Message } | ConvertTo-Json
    return Invoke-RestMethod `
        -Method Post `
        -Uri "$apiBase/chat" `
        -Headers @{ "X-Session-ID" = $sessionId } `
        -ContentType "application/json; charset=utf-8" `
        -Body ([Text.Encoding]::UTF8.GetBytes($body)) `
        -WebSession $webSession
}

$search = Send-AuthenticatedChat "Tim can ho 2 phong ngu o Quan 7, toi da 8 ty"
if (@($search.properties).Count -lt 1) { throw "No seeded property available for booking test" }

$slots = Send-AuthenticatedChat "Chon can so 1, dat lich 14 gio thu Bay tuan sau"
if ($slots.response -notmatch "\*\*1\.") { throw "No available slot returned" }

$created = Send-AuthenticatedChat "1"
$requestCode = [regex]::Match($created.response, "TR-[A-Z0-9]+").Value
if (-not $requestCode) { throw "Chat did not return a real tour request code" }

$all = Invoke-RestMethod -Uri "$apiBase/bookings/my" -WebSession $webSession
$request = $null
foreach ($item in $all) {
    if ($item.request_code -eq $requestCode) { $request = $item; break }
}
if (-not $request) { throw "Created request is missing from /bookings/my" }
if ($request.status -ne "WAITING_APPROVAL") { throw "Expected WAITING_APPROVAL, got $($request.status)" }

$status = Send-AuthenticatedChat "Trang thai $requestCode"
if ($status.response -notmatch "WAITING_APPROVAL") { throw "Chat status is not grounded in the booking record" }

$null = Send-AuthenticatedChat "Huy lich $requestCode"
$cancelled = Send-AuthenticatedChat "xac nhan"
if ([string]::IsNullOrWhiteSpace($cancelled.response)) { throw "Chat returned an empty cancellation response" }

$after = Invoke-RestMethod -Uri "$apiBase/bookings/$($request.id)" -WebSession $webSession
if ($after.status -ne "CANCELLED") { throw "Cleanup failed; request remains $($after.status)" }

Write-Output "PASS: $requestCode moved SEARCH -> SLOT -> WAITING_APPROVAL -> STATUS -> CANCELLED."
