$ErrorActionPreference = "Stop"

$apiBase = if ($env:BOOKINGBOT_API_BASE) { $env:BOOKINGBOT_API_BASE.TrimEnd("/") } else { "http://127.0.0.1:8000/api/v1" }
$sessionId = [guid]::NewGuid().ToString()
$message = "Vo chong toi sap co em be, hay tim o Thanh Xuan mot cho yen tinh co 2 phong ngu, tai chinh khong qua 4,6 ty va tien di lam o Nga Tu So."
$body = @{ message = $message } | ConvertTo-Json
$watch = [Diagnostics.Stopwatch]::StartNew()
$response = Invoke-RestMethod `
    -Method Post `
    -Uri "$apiBase/chat" `
    -Headers @{ "X-Session-ID" = $sessionId } `
    -ContentType "application/json; charset=utf-8" `
    -Body ([Text.Encoding]::UTF8.GetBytes($body))
$watch.Stop()

if ($response.ai_mode -ne "llm_grounded") { throw "Expected llm_grounded, got $($response.ai_mode): $($response.ai_fallback_reason)" }
if ([string]::IsNullOrWhiteSpace($response.ai_model)) { throw "Response did not disclose the model" }
if ($response.ai_latency_ms -lt 1) { throw "Response did not report provider latency" }
if ($response.insights.district -notlike "*Thanh Xu*") { throw "LLM did not extract Thanh Xuan" }
if ($response.insights.min_bedrooms -ne 2) { throw "LLM did not extract two bedrooms" }
if ($response.insights.max_price -ne 4600000000) { throw "LLM did not normalize 4.6 billion VND" }
if (@($response.insights.soft_preferences).Count -lt 1) { throw "LLM ignored qualitative preferences" }
if ($response.insights.commute_landmark -notlike "*Nga Tu So*" -and $response.insights.commute_landmark -notlike "*Ng* T* S*") {
    throw "LLM ignored the commute landmark"
}
if (@($response.properties).Count -lt 1) { throw "Grounded search returned no seeded property" }
if (@($response.properties | Where-Object district -notlike "*Thanh Xu*").Count -gt 0) { throw "Search leaked another district" }

Write-Output "PASS: real model=$($response.ai_model), provider_ms=$($response.ai_latency_ms), wall_ms=$([math]::Round($watch.Elapsed.TotalMilliseconds)), grounded properties=$(@($response.properties).Count)."
