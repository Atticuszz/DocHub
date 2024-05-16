### C++ 智能指针简介

智能指针是现代 C++ 中用于自动管理内存的对象，通过封装原始指针，它们帮助程序员避免内存泄漏并提供异常安全。C++11 标准引入了几种智能指针类型，使得资源管理更加简单和安全。

#### 智能指针类型

1. **`std::unique_ptr`**
   - **特性**：提供对内存的独占所有权，即同一时间内只有一个 `std::unique_ptr` 可以拥有资源。
   - **典型用途**：用于需要明确单一所有权的情况，例如在函数内部创建临时对象。
   - **不可复制**：只能移动，确保所有权的唯一性。
   - **引入版本**：C++11。

2. **`std::shared_ptr`**
   - **特性**：支持多重所有权概念，即多个 `std::shared_ptr` 对象可以共享同一个资源。
   - **典型用途**：用于对象生命周期需要由多个所有者共同管理的情况，例如在多个数据结构之间共享数据。
   - **引入版本**：C++11。

3. **`std::weak_ptr`**
   - **特性**：提供一种非拥有性的智能指针，用来观察 `std::shared_ptr`，但不影响其引用计数。
   - **典型用途**：用于解决 `std::shared_ptr` 可能导致的循环引用问题。
   - **引入版本**：C++11。

```cpp
#include <iostream>
#include <memory>

class Child;
class Parent;

class Parent : public std::enable_shared_from_this<Parent> {
public:
    std::shared_ptr<Child> child;
    ~Parent() { std::cout << "Parent destroyed\n"; }

    void setChild(std::shared_ptr<Child> c) {
        child = c;
        child->setParent(shared_from_this());  // 使用 shared_from_this() 获取当前对象的 shared_ptr
    }
};

class Child {
public:
    std::weak_ptr<Parent> parent;  // 使用 weak_ptr 避免循环引用
    ~Child() { std::cout << "Child destroyed\n"; }
    
    void setParent(std::shared_ptr<Parent> p) {
        parent = p;  // 设置 parent 为传入的 shared_ptr
    }
};

int main() {
    std::shared_ptr<Parent> p = std::make_shared<Parent>();
    std::shared_ptr<Child> c = std::make_shared<Child>();
    p->setChild(c);

    std::cout << "Parent use count: " << p.use_count() << std::endl;  // 输出会是 2，因为 child 也持有 parent 的 shared_ptr
    std::cout << "Child use count: " << c.use_count() << std::endl;   // 输出 1
}

```
#### 创建和使用智能指针

- **`std::make_shared`**
  - **描述**：用于构造 `std::shared_ptr` 的优选方法，因为它可以在单一操作中分配内存，提高效率并减少异常风险。
  - **引入版本**：C++11。

- **`std::make_unique`**
  - **描述**：用于构造 `std::unique_ptr` 的方法。类似于 `std::make_shared`，但专为 `std::unique_ptr` 设计。
  - **引入版本**：C++14。

- **`shared_from_this`**
  - **描述**：当类继承自 `std::enable_shared_from_this` 时，你可以安全地在类内部获取一个指向自己的 `std::shared_ptr`。
  - **引入版本**：C++11。

`shared_from_this()` 只能在 `std::shared_ptr` 已经拥有该对象时才能安全调用。如果在任何 `std::shared_ptr` 拥有对象之前调用它，程序将抛出 `std::bad_weak_ptr` 异常。

### 代码示例

```cpp
#include <memory>
#include <iostream>

class MyClass : public std::enable_shared_from_this<MyClass> {
public:
    void show() {
        auto sharedPtr = shared_from_this();
        std::cout << "MyClass instance has " << sharedPtr.use_count() << " references\n";
    }
};

int main() {
    auto myObject = std::make_shared<MyClass>();
    myObject->show();  // 显示引用计数
}
```
