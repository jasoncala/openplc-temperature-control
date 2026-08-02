$ContainerName = "openplc-v3"

Write-Host "=== Container ==="
docker ps -a --filter "name=^/$ContainerName$"

Write-Host ""
Write-Host "=== Recent logs ==="
docker logs --tail 50 $ContainerName

Write-Host ""
Write-Host "=== Web port ==="
Test-NetConnection -ComputerName 127.0.0.1 -Port 8080

Write-Host ""
Write-Host "=== Modbus port ==="
Test-NetConnection -ComputerName 127.0.0.1 -Port 1502