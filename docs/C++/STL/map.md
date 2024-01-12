## Initialization

- **Empty Map**:
  ```cpp
  std::map<int, std::string> myMap;

      std::unordered_map<int, std::string> myMap = {
      {1, "one"},
      {2, "two"},
      {3, "three"}

  };
  ```

## Insert Elements

- **Insert Single Element**:

  ```cpp
  myMap[1] = "one";  // Insert key-value pair
  // or
  myMap.insert(std::make_pair(1, "one"));  // Insert key-value pair

  myMap.emplace(1, "one"); // create key-value pair directly
  ```

## Access Elements

- **Access Value by Key**:

  ```cpp
  std::string value = myMap[1];  // Access value by key, returns std::string
  ```

- **Find Element**:
  ```cpp
  auto it = myMap.find(1);  // Returns iterator to the element if key exists, otherwise returns myMap.end()
  ```

## Removing Elements

- **Remove Element by Key**:
  ```cpp
  myMap.erase(1);  // Removes element with key 1, returns number of elements removed (size_t)
  ```

## Query Attributes

- **Get Map Size**:

  ```cpp
  size_t size = myMap.size();  // Returns the number of elements in the map (size_t)
  ```

- **Check if Map is Empty**:
  ```cpp
  bool isEmpty = myMap.empty();  // Returns true if the map is empty, otherwise false (bool)
  ```

## Iterating through Map

- **Using Iterator**:

  ```cpp
  for (auto it = myMap.begin(); it != myMap.end(); ++it) {
      // it->first: key
      // it->second: value
  }
  ```

- **Using Range-based For Loop**:
  ```cpp
  for (const auto& [key, value] : myMap) {
      // key: key
      // value: value
  }
  ```

## Other Common Operations

- **Clear Map**:
  ```cpp
  myMap.clear();  // Removes all elements from the map
  ```
