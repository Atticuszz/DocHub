- std::unordered_set is an associative container that contains a set of unique objects. Search, insertion, and removal operations have average constant-time complexity.

### Initialization

- **Empty Unordered Set**:
  ```cpp
  std::unordered_set<int> myUnorderedSet;
  ```

### Insert Elements

- **Insert Single Element** (Average case O(1)):

  ```cpp
  myUnorderedSet.insert(10); // Insert an element
  ```

- **Emplace Element** (Average case O(1)):
  ```cpp
  myUnorderedSet.emplace(10); // Construct and insert element
  ```

### Access Elements

- **Find Element** (Average case O(1)):
  ```cpp
  auto it = myUnorderedSet.find(10);
  // Returns iterator to the element if found, otherwise returns myUnorderedSet.end()
  ```

### Removing Elements

- **Remove Element by Value** (Average case O(1)):
  ```cpp
  myUnorderedSet.erase(10); // Erases element with value 10
  ```

### Query Attributes

- **Get Unordered Set Size** (O(1)):

  ```cpp
  size_t size = myUnorderedSet.size(); // Returns the number of elements
  ```

- **Check if Unordered Set is Empty** (O(1)):
  ```cpp
  bool isEmpty = myUnorderedSet.empty(); // Returns true if unordered set is empty, otherwise false
  ```

### Iterating through Unordered Set

- **Using Iterator** (O(n)):

  ```cpp
  for (auto it = myUnorderedSet.begin(); it != myUnorderedSet.end(); ++it) {
      // Access the element as *it
  }
  ```

- **Using Range-based For Loop** (O(n)):
  ```cpp
  for (const auto& elem : myUnorderedSet) {
      // Access the element directly as elem
  }
  ```

### Other Common Operations

- **Clear Unordered Set** (O(n)):
  ```cpp
  myUnorderedSet.clear(); // Removes all elements from the unordered set
  ```
