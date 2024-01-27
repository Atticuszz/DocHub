A queue is a container adaptor that provides a FIFO (First-In-First-Out) data structure. The standard library's `std::queue` is defined in the header `<queue>`.

## Initialization

- **Empty Queue**:
  ```cpp
  std::queue<int> q;
  ```

## Adding Elements

- **Append to End**:
  ```cpp
  q.push(4);
  ```

## Access Elements

- **Access Next Element**:

  ```cpp
  int next = q.front();
  ```

- **Access Last Element**:
  ```cpp
  int last = q.back();
  ```

## Removing Elements

- **Remove Next Element**:
  ```cpp
  q.pop();  // Removes the element at the front of the queue
  ```

## Query Attributes

- **Get Queue Size**:

  ```cpp
  size_t size = q.size();
  ```

- **Check if Queue is Empty**:
  ```cpp
  bool isEmpty = q.empty();
  ```

## Other Common Operations

- **Swap Contents**:
  ```cpp
  std::queue<int> q1, q2;
  q1.swap(q2);  // Swaps the contents of q1 and q2
  ```

# Examples

-

```cpp
#include <iostream>
#include <queue>

int main() {
    std::queue<int> q;

    // Adding elements to the queue
    q.push(1);
    q.push(2);
    q.push(3);

    // Accessing elements
    std::cout << "Front: " << q.front() << std::endl; // Outputs 1
    std::cout << "Back: " << q.back() << std::endl;  // Outputs 3

    // Removing elements
    q.pop();  // Now the front is 2

    // Checking size and if empty
    std::cout << "Size: " << q.size() << std::endl; // Outputs 2
    std::cout << "Is empty: " << (q.empty() ? "Yes" : "No") << std::endl;  // Outputs No

    return 0;
}
```
