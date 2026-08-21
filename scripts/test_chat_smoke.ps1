$ErrorActionPreference = "Stop"

$apiBase = if ($env:BOOKINGBOT_API_BASE) { $env:BOOKINGBOT_API_BASE.TrimEnd("/") } else { "http://127.0.0.1:8000/api/v1" }
$sessionId = [guid]::NewGuid().ToString()
$results = @()

function Send-Chat([string]$Message) {
    $body = @{ message = $Message } | ConvertTo-Json
    $watch = [Diagnostics.Stopwatch]::StartNew()
    $response = Invoke-RestMethod `
        -Method Post `
        -Uri "$apiBase/chat" `
        -Headers @{ "X-Session-ID" = $sessionId } `
        -ContentType "application/json; charset=utf-8" `
        -Body ([Text.Encoding]::UTF8.GetBytes($body))
    $watch.Stop()
    $script:results += [pscustomobject]@{
        message = $Message
        elapsed_ms = [math]::Round($watch.Elapsed.TotalMilliseconds)
        properties = @($response.properties).Count
        response_empty = [string]::IsNullOrWhiteSpace($response.response)
    }
    if ([string]::IsNullOrWhiteSpace($response.response)) {
        throw "Chat returned an empty response for: $Message"
    }
    return $response
}

$health = Invoke-RestMethod -Uri ($apiBase -replace "/api/v1$", "/health")
if ($health.status -ne "ok") { throw "Backend health check failed" }

$search = Send-Chat "Toi can can ho 2 phong ngu o Quan 7, ngan sach toi da 8 ty"
if (@($search.properties).Count -lt 1) { throw "Expected at least one seeded Quan 7 property" }
if (@($search.properties | Where-Object property_kind -ne "APARTMENT").Count -gt 0) {
    throw "Search returned a non-apartment property"
}

$slots = Send-Chat "Toi chon can so 1. Dat lich xem luc 14 gio thu Bay tuan sau"
if ($slots.response -notmatch "\*\*1\.") { throw "Multi-turn property reference was not preserved" }
if ($slots.insights.property_kind -ne "APARTMENT") { throw "Booking phrase corrupted property_kind" }

$guest = Send-Chat "1"
if (-not $guest.auth_required) { throw "Guest booking must require authentication" }

$status = Send-Chat "Kiem tra lich cua toi"
if (-not $status.auth_required) { throw "Guest status lookup must require authentication" }

# A new natural-language search must replace stale location/type/detail filters.
$sessionId = [guid]::NewGuid().ToString()
$hanoi = Send-Chat "tim nha duoi 5 ty o thanh xuan"
if ($hanoi.insights.district -notlike "*Thanh Xu*") { throw "Bare Thanh Xuan district was not recognized" }
if ($hanoi.insights.min_area -or $hanoi.insights.min_bedrooms -or $hanoi.insights.property_kind) {
    throw "A fresh search inherited stale area, bedroom, or property-kind filters"
}
if (@($hanoi.properties).Count -lt 1) { throw "Expected seeded properties in Thanh Xuan" }
if (@($hanoi.properties | Where-Object district -notlike "*Thanh Xu*").Count -gt 0) {
    throw "Thanh Xuan search leaked results from another district"
}

$refined = Send-Chat "3 phong ngu"
if ($refined.insights.min_bedrooms -ne 3) { throw "Bedroom follow-up was not applied" }
if ($refined.insights.district -notlike "*Thanh Xu*") { throw "Bedroom follow-up lost the selected district" }

$results | Format-Table -AutoSize
Write-Output "PASS: durable multi-turn chat smoke test completed with no database side effects."
