- std::set is an associative container that contains a sorted set of unique objects. It is usually implemented as a red-black tree.

### Initialization

- **Empty Set**:
    ```cpp
    std::set<int> mySet;
    ```

### Insert Elements

- **Insert Single Element** (Average case O(log n)):
    ```cpp
    mySet.insert(10); // Insert an element
    ```

- **Emplace Element** (Average case O(log n)):
    ```cpp
    mySet.emplace(10); // Construct and insert element
    ```

### Access Elements

- **Find Element** (Average case O(log n)):
    ```cpp
    auto it = mySet.find(10); // Returns iterator to the element if found, otherwise returns mySet.end()
    ```

### Removing Elements

- **Remove Element by Value** (Average case O(log n)):
    ```cpp
    mySet.erase(10); // Erases element with value 10
    ```

### Query Attributes

- **Get Set Size** (O(1)):
    ```cpp
    size_t size = mySet.size(); // Returns the number of elements
    ```

- **Check if Set is Empty** (O(1)):
    ```cpp
    bool isEmpty = mySet.empty(); // Returns true if set is empty, otherwise false
    ```

### Iterating through Set

- **Using Iterator** (O(n)):
    ```cpp
    for (auto it = mySet.begin(); it != mySet.end(); ++it) {
        // Access the element as *it
    }
    ```

- **Using Range-based For Loop** (O(n)):
    ```cpp
    for (const auto& elem : mySet) {
        // Access the element directly as elem
    }
    ```

### Other Common Operations

- **Clear Set** (O(n)):
    ```cpp
    mySet.clear(); // Removes all elements from the set
    ```

