# Generate Aggregate CSV from JTL results
$jtlPath = Join-Path $PSScriptRoot "results\results.jtl"
$outputPath = Join-Path $PSScriptRoot "results\aggregate.csv"

$jtl = Import-Csv $jtlPath
$labels = $jtl | Group-Object -Property label
$results = @()

foreach ($group in $labels) {
    $times = $group.Group | ForEach-Object { [int]$_.elapsed } | Sort-Object
    $count = $times.Count
    $avg = [math]::Round(($times | Measure-Object -Average).Average, 0)
    $min = ($times | Measure-Object -Minimum).Minimum
    $max = ($times | Measure-Object -Maximum).Maximum
    $median = $times[[math]::Floor($count * 0.5)]
    $p90 = $times[[math]::Floor($count * 0.90)]
    $p95 = $times[[math]::Floor($count * 0.95)]
    $p99 = $times[[math]::Floor($count * 0.99)]
    $errors = ($group.Group | Where-Object { $_.success -eq 'false' }).Count
    $errorPct = [math]::Round(($errors / $count) * 100, 2)
    $startTime = [int64]($group.Group[0].timeStamp)
    $endTime = [int64]($group.Group[-1].timeStamp)
    $duration = ($endTime - $startTime) / 1000
    if ($duration -le 0) { $duration = 1 }
    $throughput = [math]::Round($count / $duration, 2)
    $results += [PSCustomObject]@{
        Label = $group.Name
        Samples = $count
        Average = $avg
        Median = $median
        P90 = $p90
        P95 = $p95
        P99 = $p99
        Min = $min
        Max = $max
        ErrorPct = $errorPct
        ThroughputPerSec = $throughput
        Errors = $errors
    }
}

# Add TOTAL row
$allTimes = $jtl | ForEach-Object { [int]$_.elapsed } | Sort-Object
$totalCount = $allTimes.Count
$totalAvg = [math]::Round(($allTimes | Measure-Object -Average).Average, 0)
$totalMin = ($allTimes | Measure-Object -Minimum).Minimum
$totalMax = ($allTimes | Measure-Object -Maximum).Maximum
$totalMedian = $allTimes[[math]::Floor($totalCount * 0.5)]
$totalP90 = $allTimes[[math]::Floor($totalCount * 0.90)]
$totalP95 = $allTimes[[math]::Floor($totalCount * 0.95)]
$totalP99 = $allTimes[[math]::Floor($totalCount * 0.99)]
$totalErrors = @($jtl | Where-Object { $_.success -eq 'false' }).Count
$totalErrorPct = [math]::Round(($totalErrors / $totalCount) * 100, 2)
$totalStart = [int64]($jtl[0].timeStamp)
$totalEnd = [int64]($jtl[-1].timeStamp)
$totalDuration = ($totalEnd - $totalStart) / 1000
if ($totalDuration -le 0) { $totalDuration = 1 }
$totalThroughput = [math]::Round($totalCount / $totalDuration, 2)

$results += [PSCustomObject]@{
    Label = 'TOTAL'
    Samples = $totalCount
    Average = $totalAvg
    Median = $totalMedian
    P90 = $totalP90
    P95 = $totalP95
    P99 = $totalP99
    Min = $totalMin
    Max = $totalMax
    ErrorPct = $totalErrorPct
    ThroughputPerSec = $totalThroughput
    Errors = $totalErrors
}

$results | Export-Csv -Path $outputPath -NoTypeInformation
$results | Format-Table -AutoSize

Write-Host "`nAggregate CSV saved to: $outputPath"
