$ErrorActionPreference = "Stop"

if (-not $env:BOOKINGBOT_TEST_EMAIL -or -not $env:BOOKINGBOT_TEST_PASSWORD) {
    throw "Set BOOKINGBOT_TEST_EMAIL and BOOKINGBOT_TEST_PASSWORD for a disposable CUSTOMER account."
}

$apiBase = if ($env:BOOKINGBOT_API_BASE) { $env:BOOKINGBOT_API_BASE.TrimEnd("/") } else { "http://127.0.0.1:8000/api/v1" }
$salePassword = if ($env:BOOKINGBOT_SALE_PASSWORD) { $env:BOOKINGBOT_SALE_PASSWORD } else { "123456" }
$sessionId = [guid]::NewGuid().ToString()
$customerSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$saleSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$bookingId = $null
$passMessage = $null

function Login([Microsoft.PowerShell.Commands.WebRequestSession]$WebSession, [string]$Email, [string]$Password) {
    $body = "username=$([uri]::EscapeDataString($Email))&password=$([uri]::EscapeDataString($Password))"
    return Invoke-RestMethod -Method Post -Uri "$apiBase/auth/login" -ContentType "application/x-www-form-urlencoded" -Body $body -WebSession $WebSession
}

function Send-CustomerChat([string]$Message) {
    $body = @{ message = $Message } | ConvertTo-Json
    return Invoke-RestMethod `
        -Method Post `
        -Uri "$apiBase/chat" `
        -Headers @{ "X-Session-ID" = $sessionId } `
        -ContentType "application/json; charset=utf-8" `
        -Body ([Text.Encoding]::UTF8.GetBytes($body)) `
        -WebSession $customerSession
}

try {
    $customerLogin = Login $customerSession $env:BOOKINGBOT_TEST_EMAIL $env:BOOKINGBOT_TEST_PASSWORD
    if ($customerLogin.user.role -ne "CUSTOMER") { throw "The test account must have CUSTOMER role" }

    $search = Send-CustomerChat "Tim can ho 2 phong ngu o Quan 7, toi da 8 ty"
    if (@($search.properties).Count -lt 1) { throw "No seeded property available for approval test" }

    $slots = Send-CustomerChat "Chon can so 1, dat lich 14 gio thu Bay tuan sau"
    if ($slots.response -notmatch "\*\*1\.") { throw "No available slot returned" }

    $created = Send-CustomerChat "1"
    $requestCode = [regex]::Match($created.response, "TR-[A-Z0-9]+").Value
    if (-not $requestCode) { throw "Chat did not return a tour request code" }

    $bookings = Invoke-RestMethod -Uri "$apiBase/bookings/my" -WebSession $customerSession
    $booking = $bookings | Where-Object { $_.request_code -eq $requestCode } | Select-Object -First 1
    if (-not $booking) { throw "Created request is missing from /bookings/my" }
    if (-not $booking.sale.email) { throw "Booking has no assigned Sale account" }
    $bookingId = $booking.id

    $saleLogin = Login $saleSession $booking.sale.email $salePassword
    if ($saleLogin.user.role -ne "SALE") { throw "Assigned account is not a SALE" }

    $accepted = Invoke-RestMethod -Method Post -Uri "$apiBase/sale/requests/$bookingId/accept" -WebSession $saleSession
    if ($accepted.status -ne "BOOKED") { throw "Expected BOOKED after Sale approval, got $($accepted.status)" }
    if (-not $accepted.appointment.booking_code) { throw "Sale approval did not create an appointment" }

    $status = Send-CustomerChat "Trang thai $requestCode"
    if ($status.response -notmatch "BOOKED") { throw "Chat did not report the approved booking state" }
    if ($status.response -notmatch $accepted.appointment.booking_code) { throw "Chat omitted the real booking code" }

    $passMessage = "PASS: $requestCode was approved by $($booking.sale.email) as $($accepted.appointment.booking_code), chat reported BOOKED, and cleanup returned CANCELLED."
}
finally {
    if ($bookingId) {
        $null = Invoke-RestMethod -Method Post -Uri "$apiBase/bookings/$bookingId/cancel" -ContentType "application/json" -Body '{"reason":"Automated end-to-end test cleanup"}' -WebSession $customerSession
        $cleaned = Invoke-RestMethod -Uri "$apiBase/bookings/$bookingId" -WebSession $customerSession
        if ($cleaned.status -ne "CANCELLED") { throw "Cleanup failed; request remains $($cleaned.status)" }
    }
}

if ($passMessage) { Write-Output $passMessage }
