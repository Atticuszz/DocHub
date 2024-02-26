# 定义Clash安装路径
$clashPath = "C:\Program Files\Clash for Windows\Clash for Windows.exe"
$clashConfigDir = "C:\Users\$env:USERNAME\.config\clash\profiles"

# 资源路径
$sourceUrl = "https://github.com/SupaVision/DocHub/releases/tag/clash"
$clashDownloadUrl = "https://github.com/SupaVision/DocHub/releases/download/clash/Clash.for.Windows.Setup.0.20.34.exe"
$clashDownloadPath = "C:\Users\$env:USERNAME\Downloads\clash_setup.exe"
$clashConfigUrl = "https://github.com/SupaVision/DocHub/releases/download/clash/clash_proxies_config.yml"

Write-Output "this is powershell script of auto install and update config clash from $sourceUrl"


# 检查Clash是否安装
if (-not (Test-Path $clashPath)) {
    Write-Output "Clash is not installed. Downloading Clash from $clashDownloadUrl ..."

    # 下载Clash
    Invoke-WebRequest -Uri $clashDownloadUrl -OutFile $clashDownloadPath
    # 安装clash
    Write-Output "Attempting to install Clash automatically..."
    Start-Process -FilePath $clashDownloadPath -Args "/S" -NoNewWindow -Wait
    Write-Output "Clash installation attempted. Please check if installation was successful."

} else {
    Write-Output "Clash is already installed."
}

# 确保配置目录存在
if (-not (Test-Path $clashConfigDir)) {
    New-Item -ItemType Directory -Path $clashConfigDir
    Write-Output "Clash config directory created at $clashConfigDir."
    exit
}

# 自动下载配置
$userChoice = Read-Host "Do you want to automatically download the configuration file? (Y/N)"
if ($userChoice -eq "Y") {
    $existingConfigPath = Get-ChildItem -Path $clashConfigDir | Select-Object -First 1 -ExpandProperty FullName
    if (-not (Test-Path $existingConfigPath)){
        Write-Output "no existing configs in $clashConfigDir !"
        Write-Output "Please manually download the configuration file from: $clashConfigUrl"
    }
    Invoke-WebRequest -Uri $clashConfigUrl -OutFile $existingConfigPath
    Write-Output "Clash configuration file downloaded and saved to $existingConfigPath."
} else {
    Write-Output "Please manually download the configuration file from: $clashConfigUrl"
}

if (Test-Path -Path $clashDownloadPath) {
    Remove-Item -Path $clashDownloadPath
    Write-Output "Downloaded installation file has been cleaned up."
}
Write-Output "Clash configuration update script has completed."

# 提示用户重启Clash应用
Write-Output "Please restart Clash for the new configuration to take effect."
