$root = "D:\PROJET_ALFRED\ALFRED_PC"

Write-Host "🧹 Nettoyage Alfred..." -ForegroundColor Cyan

Get-ChildItem $root -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem $root -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "✅ Clean terminé"