# SPN2 (Save Page Now 2) archiving script for unarchived cited URLs
# Requires Internet Archive API keys (access key + secret key)
# Get keys from: https://archive.org/account/s3.php
# Usage: Set env vars IA_ACCESS_KEY and IA_SECRET_KEY, then run this script

param(
    [string]$UrlsFile = "unarchived_urls.txt",
    [int]$DelayMs = 5000
)

$accessKey = $env:IA_ACCESS_KEY
$secretKey = $env:IA_SECRET_KEY

if (-not $accessKey -or -not $secretKey) {
    Write-Error "Set IA_ACCESS_KEY and IA_SECRET_KEY environment variables first."
    Write-Host "Get keys from: https://archive.org/account/s3.php"
    exit 1
}

$urls = Get-Content $UrlsFile
$headers = @{
    "User-Agent" = "otowa-ankyoscape-link-audit/1.0"
    "Authorization" = "LOW ${accessKey}:${secretKey}"
}

$results = @()
$i = 0
$total = $urls.Count

foreach ($url in $urls) {
    $i++
    $jobId = ""
    $status = ""
    $retries = 0
    $maxRetries = 3
    
    while ($retries -lt $maxRetries) {
        try {
            $body = "url=$([System.Uri]::EscapeDataString($url))&if_not_archived_within=30d"
            $resp = Invoke-RestMethod -Uri "https://web.archive.org/save/" -Method POST -Headers $headers -Body $body -ContentType "application/x-www-form-urlencoded" -TimeoutSec 60 -ErrorAction Stop
            $jobId = $resp.job_id
            $status = $resp.status
            break
        } catch {
            $code = $_.Exception.Response.StatusCode.Value__
            if ($code -eq 429) {
                $retries++
                $wait = 10 * $retries
                Write-Host "Rate limited on $url, waiting ${wait}s..."
                Start-Sleep -Seconds $wait
            } else {
                $status = "ERROR:$code"
                break
            }
        }
    }
    
    $results += [PSCustomObject]@{
        URL = $url
        JobId = $jobId
        Status = $status
    }
    
    if ($i % 10 -eq 0) {
        Write-Host "Processed $i / $total (last: $status)"
    }
    
    Start-Sleep -Milliseconds $DelayMs
}

$results | Export-Csv -Path "spn2_results.csv" -NoTypeInformation -Encoding UTF8
Write-Host "Done. Total: $total"
$success = ($results | Where-Object { $_.Status -ne "" -and $_.Status -notlike "ERROR*" }).Count
Write-Host "Submitted: $success"
Write-Host ""
Write-Host "To check capture status, poll: https://web.archive.org/save/status/<JOB_ID>"
Write-Host "With Authorization: LOW ${accessKey}:${secretKey}"
