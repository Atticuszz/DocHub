## Initialization

- **Empty Vector**: 
    ```cpp
    std::vector<int> vec;
    ```
- **Pre-allocate Size**: 
    ```cpp
    std::vector<int> vec(10);  // Contains 10 elements, all initialized to 0
    ```
- **Pre-allocate Size with Value**: 
    ```cpp
    std::vector<int> vec(10, 1);  // Contains 10 elements, all initialized to 1
    ```
- **Initialize from Array**: 
    ```cpp
    int arr[] = {1, 2, 3};
    std::vector<int> vec(arr, arr + sizeof(arr) / sizeof(int));
    ```
- **Initialize from Another Vector**: 
    ```cpp
    std::vector<int> vec2(vec);
    ```

## Adding Elements

- **Append to End**: 
    ```cpp
    vec.push_back(4);
    ```
- **Insert at Beginning**: 
    ```cpp
    vec.insert(vec.begin(), 4);
    ```
- **Insert at Specific Position**: 
    ```cpp
    vec.insert(vec.begin() + 1, 4);
    ```

## Access Elements

- **Access Last Element**: 
    ```cpp
    int last = vec.back();
    ```
- **Access First Element**: 
    ```cpp
    int first = vec.front();
    ```
- **Access i-th Element (0-based)**: 
    ```cpp
    int elem = vec[i];
    ```

## Removing Elements

- **Remove Last Element**: 
    ```cpp
    vec.pop_back();    ->void
    ```
- **Remove i-th Element**: 
    ```cpp
    vec.erase(vec.begin() + i);
    ```
- **Remove a Range of Elements**: 
    ```cpp
    vec.erase(vec.begin() + i, vec.begin() + j);  // Removes elements from i to j-1
    ```

## Query Attributes

- **Get Vector Size**: 
    ```cpp
    size_t size = vec.size();
    ```
- **Check if Vector is Empty**: 
    ```cpp
    bool isEmpty = vec.empty();
    ```

## Other Common Operations

- **Clear Vector**: 
    ```cpp
    vec.clear();
    ```
- **Resize Vector**: 
    ```cpp
    vec.resize(20);  // New elements are initialized to 0
    ```
- **Find Element Position**: 
    ```cpp
    std::find(vec.begin(), vec.end(), value) != vec.end()
    ```
- **Sort Vector**: 
    ```cpp
    std::sort(vec.begin(), vec.end());
    ```



# examples

```c++

#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> vec = {3, 1, 4, 1, 5, 9, 2, 6, 5};

    // 使用 std::min_element 和 lambda 函数找到最小正整数
    auto it = std::min_element(vec.begin(), vec.end(), [](int a, int b) {
        if (a <= 0) return false;
        if (b <= 0) return true;
        return a < b;
    });

    if (it != vec.end() && *it > 0) {
        std::cout << "最小正整数是：" << *it << std::endl;
    } else {
        std::cout << "没有找到正整数" << std::endl;
    }

    return 0;
}
```


```c++
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> vec = {1, 2, 2, 3, 4, 4, 5};

    // 先排序
    std::sort(vec.begin(), vec.end());

    // 使用 std::unique 去重
    auto last = std::unique(vec.begin(), vec.end());

    // 删除多余元素
    vec.erase(last, vec.end());

    // 输出去重后的向量
    for (const auto& elem : vec) {
        std::cout << elem << " ";
    }
    std::cout << std::endl;

    return 0;
}

```