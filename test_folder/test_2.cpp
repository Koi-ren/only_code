#include <iostream>

int main() {
    int a, b, c;
    
    std::cout << "세 개의 숫자를 공백으로 구분하여 입력하세요: ";
    std::cin >> a >> b >> c;

    int largest, middle, smallest;

    // 큰 수 찾기
    if (a >= b && a >= c) {
        largest = a;
    } else if (b >= a && b >= c) {
        largest = b;
    } else {
        largest = c;
    }

    // 작은 수 찾기
    if (a <= b && a <= c) {
        smallest = a;
    } else if (b <= a && b <= c) {
        smallest = b;
    } else {
        smallest = c;
    }

    // 중간 수 찾기
    if ((a != largest && a != smallest) || (a == b && b == c)) {
        middle = a;
    } else if ((b != largest && b != smallest) || (a == b && b == c)) {
        middle = b;
    } else {
        middle = c;
    }

    std::cout << "큰 수: " << largest << "\n";
    std::cout << "중간 수: " << middle << "\n";
    std::cout << "작은 수: " << smallest << "\n";

    return 0;
}
