$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$packRoot = $PSScriptRoot
$destination = Join-Path $packRoot 'pdf'
New-Item -ItemType Directory -Force -Path $destination | Out-Null
$items = Get-Content -Raw -Encoding UTF8 (Join-Path $packRoot 'sources.json') | ConvertFrom-Json
foreach ($item in $items) {
    $target = Join-Path $destination $item.file
    $partial = $target + '.part'
    try {
        Invoke-WebRequest -UseBasicParsing -Uri $item.url -OutFile $partial -TimeoutSec 180
        $stream = [IO.File]::OpenRead($partial)
        try {
            $head = New-Object byte[] 5
            $count = $stream.Read($head, 0, 5)
        } finally { $stream.Dispose() }
        if ($count -ne 5 -or [Text.Encoding]::ASCII.GetString($head) -ne '%PDF-') { throw 'Response is not a PDF' }
        Move-Item -Force $partial $target
        Write-Host ('OK: ' + $item.file)
    } catch {
        if (Test-Path $partial) { Remove-Item $partial }
        Write-Host ('FAILED: ' + $item.file + ' - ' + $_.Exception.Message)
    }
}
Read-Host 'Finished. Press Enter to close'
