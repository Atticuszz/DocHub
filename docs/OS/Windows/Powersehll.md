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
*admin*
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