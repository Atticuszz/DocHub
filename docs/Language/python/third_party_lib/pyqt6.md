### [load resource](https://zhuanlan.zhihu.com/p/590358586)

- generate

```bash
pyside6-rcc -o compiled_resources.py resource.qrc
```

- add the following into your compiled_resources.py

```python
from PyQt6 import QtCore
```

- usage

```python
imoprt compiled_resources
Qlabel(":images/test.png")
```
