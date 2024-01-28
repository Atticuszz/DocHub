### api
`#include<string>`
#### init

```C++
std::string str = "Hello, world!";  //
```
#### slice
`str.substr(start：int，step:int)`
```c++
std::string sub = str.substr(0, 5);  // sub = "Hello"
```
#### type conversion
```c++
int num = 43;
std::string sNum = to_string(num);
```
#### find element
`string.find(s:string|char)->size_t`
```c++
# 查找元素
String.find()->size_t
// 找到的第一个字符或者字串的index或者没找到就是string::npos
std::string myString = "Hello, world!";
size_t position = myString.find("world");// 无符号整数类型
```
#### compare
`string.compare(s:string)->bool`
```c++
std::string a="abcd";
std::string b="efgh";
int res = a.compare(b);
```