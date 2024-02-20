# 检查Obsidian是否安装
$obsidianPath = "C:\Users\$env:USERNAME\AppData\Local\Programs\Obsidian\Obsidian.exe"
if (-not (Test-Path $obsidianPath)) {
    Write-Output "Obsidian is not installed. Please install Obsidian manually: https://obsidian.md/download"
}else{
	Write-Output "Obsidian has installed!"
}


# 检查Git是否安装
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Output "Git is not installed. Please install Git first: https://git-scm.com/download/win"
    exit
}

# 定义仓库和目录
$repoUrl = "https://github.com/SupaVision/DocHub.git"
$cloneDir = "$PWD\DocHub"

# 检查目录是否存在
if (Test-Path $cloneDir) {
    $response = Read-Host "The clone directory already exists. Do you want to force sync with the cloud? [Y/N]"
    if ($response -eq 'Y') {
        Push-Location -Path $cloneDir
        git fetch origin
        git reset --hard origin/main
        git clean -fd
        Pop-Location
        Write-Output "Repository synced successfully."
    }
} else {
    git clone $repoUrl $cloneDir
    Write-Output "Repository cloned successfully."
}

# 打印克隆的目录路径
Write-Output "Clone directory path:$cloneDir"

# 询问是否更新插件zip
$zipUrl = "https://github.com/SupaVision/DocHub/releases/download/v0.0.2/obsidian.zip"
$zipPath = "$cloneDir\obsidian.zip"
$updateZipResponse = Read-Host "Do you want to update the plugin zip? [Y/N]"
if ($updateZipResponse -eq 'Y') {
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
    # 确保下载完成
    if (Test-Path $zipPath) {
        # 解压压缩文件
        $extractPath = "$cloneDir\.obsidian"
        Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
        Write-Output "Plugin zip updated and extracted successfully."
	
	# 移除下载的zip文件
        Remove-Item -Path $zipPath -Force
        Write-Output "Downloaded zip file removed."

    } else {
        Write-Output "Download failed for $zipUrl, please check the URL and try again."
    }
}
