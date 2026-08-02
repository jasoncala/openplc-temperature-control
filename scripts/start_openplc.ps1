$ErrorActionPreference = "Stop"

$ContainerName = "openplc-v3"
$ImageName = "openplc-v3-local"
$VolumeName = "openplc-v3-data"

$ExistingContainer = docker ps -a `
    --filter "name=^/$ContainerName$" `
    --format "{{.Names}}"

if ($ExistingContainer -eq $ContainerName) {
    Write-Host "Starting existing container: $ContainerName"
    docker start $ContainerName
}
else {
    Write-Host "Creating and starting container: $ContainerName"

    docker run -d `
        --name $ContainerName `
        -p 127.0.0.1:8080:8080 `
        -p 127.0.0.1:1502:502 `
        -v "${VolumeName}:/docker_persistent" `
        $ImageName
}

Write-Host ""
Write-Host "Container status:"
docker ps --filter "name=^/$ContainerName$"

Write-Host ""
Write-Host "OpenPLC web interface: http://127.0.0.1:8080"
Write-Host "OpenPLC Modbus endpoint: 127.0.0.1:1502"