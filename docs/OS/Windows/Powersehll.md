### **kill** the process by PID

```ps
taskkill /PID <PID> /F
```

### find out the process occupied the **port**

_the last line of output is PID_

```ps
netstat -ano | findstr :<port>
```

### find out the process occupied the **file**

[Sysinternals Suite - Microsoft Apps](https://www.microsoft.com/store/productId/9P7KNL5RWT25?ocid=pdpshare)

```ps
handle.exe <file path>
```

### get command .exe path

```ps
(Get-Command poetry).Source
```

`->C:\Users\18317\AppData\Roaming\Python\Scripts\poetry.exe`

### add Path

_admin_

```powershell
# 获取当前系统路径
$currentPath = [Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)

# 要添加的新路径
$newPath = "C:\Program Files\xpdf-tools-win-4.05\bin64"

# 检查新路径是否已经存在于系统路径中
if ($currentPath -notcontains $newPath) {
    # 如果不存在，则添加新路径
    $updatedPath = $currentPath + ";" + $newPath

    # 设置新的系统路径
    [Environment]::SetEnvironmentVariable("Path", $updatedPath, [System.EnvironmentVariableTarget]::Machine)

    Write-Output "Path added successfully."
} else {
    Write-Output "Path already exists in the system PATH."
}
# check path
# 输出当前系统路径
[Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)

```

### combine project files such as .py

```powershell
# 设置需要递归搜索的目录路径
$directoryPath = "C:\path\to\your\python\files"

# 指定合并后的文件名和路径
$combinedFileName = "combined.py"
$combinedFilePath = Join-Path -Path $directoryPath -ChildPath $combinedFileName

# 创建或清空之前的合并文件
"" | Out-File -FilePath $combinedFilePath

# 递归地获取所有Python文件
$pythonFiles = Get-ChildItem -Path $directoryPath -Filter *.py -Recurse

# 循环遍历每个文件并追加到combined.py
foreach ($file in $pythonFiles) {
    # 确保不处理目标文件本身
    if ($file.FullName -ne $combinedFilePath) {
        # 为每个文件添加一个简单的注释行
        ("# Contents of " + $file.FullName) | Out-File -FilePath $combinedFilePath -Append

        # 追加文件内容到combined.py
        Get-Content -Path $file.FullName | Out-File -FilePath $combinedFilePath -Append

        # 添加换行以分隔不同的文件内容
        "`n" | Out-File -FilePath $combinedFilePath -Append
    }
}

# 输出结果提示
Write-Host "All Python files have been combined into $combinedFilePath"

```
