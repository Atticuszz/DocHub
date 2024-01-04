### **kill** the process by PID
```ps
taskkill /PID <PID> /F
```


### find out the process occupied the **port**
*the last line of output is PID*
```ps
netstat -ano | findstr :<port>
```

### find out the process  occupied the **file**
[Sysinternals Suite - Microsoft Apps](https://www.microsoft.com/store/productId/9P7KNL5RWT25?ocid=pdpshare)
```ps
handle.exe <file path>
```
