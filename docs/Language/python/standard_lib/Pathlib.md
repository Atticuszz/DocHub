- **_现代的 面向对象 的系统 路径 管理库_**

*classmethod* Path.cwd()[](https://docs.python.org/zh-cn/3/library/pathlib.html#pathlib.Path.cwd "永久链接至目标")
返回一个新的表示当前目录的路径对象（和 [`os.getcwd()`](https://docs.python.org/zh-cn/3/library/os.html#os.getcwd "os.getcwd") 返回的相同，也是脚本被调用的地方
Path(\_\_file\_\_)是脚本文件所在的路径，和被调用者无关

# class attributes

1. PurePath.parents[](https://docs.python.org/zh-cn/3/library/pathlib.html#pathlib.PurePath.parents "永久链接至目标")
   提供访问此路径的逻辑祖先的不可变序列:

```python
>>> p = Path('some path dir....')
>>> p.parent == p.parents[0]
True
>>> p.Parent.parent = p.parents[1]
True
......以此类推
""" python 3.10 支持 负数 索引和 切片"""
```

1. PurePath.name
   - 最后一个组件，即dir最深处的file_name（with suffix）or folder_name

```python
>>> PurePosixPath('my/library/setup.py').name
'setup.py'
```

1. PurePath.suffix[¶](https://docs.python.org/zh-cn/3/library/pathlib.html#pathlib.PurePath.suffix "永久链接至目标")
   - 即PurePath.name的后缀str

```python

>>> PurePosixPath('my/library/setup.py').suffix
'.py'
>>> PurePosixPath('my/library.tar.gz').suffix
'.gz'
>>> PurePosixPath('my/library').suffix
''
```
