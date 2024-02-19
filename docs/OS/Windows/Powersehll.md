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
