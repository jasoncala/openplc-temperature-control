$ErrorActionPreference = "Stop"

$ContainerName = "openplc-v3"

docker stop $ContainerName

Write-Host "OpenPLC Runtime stopped."