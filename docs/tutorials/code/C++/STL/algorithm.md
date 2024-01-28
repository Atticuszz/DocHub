### reverse

`std::reverse(it.begin(),it.end()`

```c++
#include <algorithm> // for std::reverse
#include <string>

int main() {
    std::string str = "Hello";
    std::reverse(str.begin(), str.end());
    std::cout << str << std::endl;  // 输出 "olleH"
```

### char digit to int

`std::stoi/l/ll(s:string)->int|long|long long`

```c++
#include <string>
int main() {
    std::string digit_char = "42";
    int num_1 = std::stoi(digit_char);
    long num_2 = std::stol(digit_char);
    long long num_3 = std::stoll(digit_char);
    // single char
	char digitChar = '4';
	int digit = digitChar - '0';
    return 0;
}
```

### sort

`O(NlogN)`
