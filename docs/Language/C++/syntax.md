## basic

- **"a"->string, 'a'->char**

# value range

### 有符号整数类型

| 类型        | 最小值                     | 最大值                    | 备注                   |
| ----------- | -------------------------- | ------------------------- | ---------------------- |
| `char`      | -128                       | 127                       | 至少 8 位              |
| `short`     | -32,768                    | 32,767                    | 至少 16 位             |
| `int`       | -2,147,483,648             | 2,147,483,647             | 通常是 32 位           |
| `long`      | -2,147,483,648             | 2,147,483,647             | 至少 32 位，但可能更长 |
| `long long` | -9,223,372,036,854,775,808 | 9,223,372,036,854,775,807 | 至少 64 位             |

### 无符号整数类型（非负数）

| 类型                 | 最小值 | 最大值                     | 备注                   |
| -------------------- | ------ | -------------------------- | ---------------------- |
| `unsigned char`      | 0      | 255                        | 至少 8 位              |
| `unsigned short`     | 0      | 65,535                     | 至少 16 位             |
| `unsigned int`       | 0      | 4,294,967,295              | 通常是 32 位           |
| `unsigned long`      | 0      | 4,294,967,295              | 至少 32 位，但可能更长 |
| `unsigned long long` | 0      | 18,446,744,073,709,551,615 | 至少 64 位             |

## Uniform Initialization
```cpp
int a{5}; // 直接初始化
std::vector<int> v{1, 2, 3}; // 统一初始化

```
## Auto Keyword for Type Inference

```cpp
auto x = 42;  // int
auto y = 42.0;  // double
```

## Range-based For Loops

```cpp
for (const auto& elem : vec) {
    // Do something with elem
}
```

## Lambda Expressions

```cpp
auto add = [](int a, int b) -> int {
    return a + b;
};
```

## Smart Pointers

```cpp
std::unique_ptr<int> p1(new int(42));
std::shared_ptr<int> p2 = std::make_shared<int>(42);
```

## Template Functions

```cpp
template <typename T>
T getMax(T a, T b) {
    return (a > b) ? a : b;
}
```

## Move Semantics

```cpp
std::vector<int> vec1 = {1, 2, 3};
std::vector<int> vec2 = std::move(vec1);  // Moves data from vec1 to vec2
```

## Structured Binding (C++17)

```cpp
std::pair<int, std::string> p = {1, "one"};
auto [num, word] = p;
```

## Variadic Templates

```cpp
template<typename... Args>
void printAll(Args... args) {
    // Do something
}
```

## pattern match

### switch

```cpp
int value = /* some value */;
switch (value) {
    case 1:
        // do something
        break;
    case 2:
        // do something else
        break;
    default:
        // default case
        break;
}
```

### unordered_map

```cpp
unordered_map<string, function<int(int, int)>> operations = {
            {"+", [](int a, int b) { return a + b; }},
            {"-", [](int a, int b) { return a - b; }},
            {"*", [](int a, int b) { return a * b; }},
            {"/", [](int a, int b) { return a / b; }}
        };
```
