# Mina

Mina is a compiler made entirely with Python using PLY (Python Lex-Yacc).
The compiler uses a virtual machine to keep track of memory use.

## Installation

To use the compiler, Python 3 must be installed in the system

## Usage

In the root directory run:

```bash
python3 main.py <filename>
```

## Manual

Program Structure

```cpp
program <name>;

// This is a comment!

//Global variable declaration
// Allowed types for variables are int, float, bool and char
var <type> <name>, <name2>;

//Function declaration
// Allowed types for function returns are int, float, bool, char and void
function <type> <name>(<type> <name, <type <name2>) {
    return <name + <name2>;
}

// Main function, will run at the start
main() {

    // Variable declaration
    var <type> <name>, <name2>;

    // Array declaration
    var <type> <name>[<size>];

    // Print variables, strings and expressions
    print(a, "This will also print", 5+5);

    // Read from console into variable a
    read(a);

    // Read from console into variable a and then read from console into b
    read(a, b);

    // If statement
    if (5 > 3) {
        print("This is true!");
    }

    // If-else statement
    if (5 < 3) {
        print("This will not print :( ");
    } else {
        print("This will print!");
    }

    // While loop
    while (a < 5) {
        print("This will print until 'a' is more than 5!");
        a = a + 1;
    }

    // Do-while loop
    do {
        print("This will print until 'a' is more than 5!");
        a = a + 1;
    } while (a < 5)

    // For loop
    for (a = 1 to 6) {
        print("This will print 5 times");
    }

    // Statistical functions
    // Several statistical functions are included, they take the name of
    // an array as a parameter
    // mean(arr)
    // median(arr)
    // mode(arr)
    // variance(arr)
    // plot(arr1, arr2)
}
```

Declare variables

```cpp
var int a, arr[5];
var float f;
```

Declare functions

```cpp
function int add(int a, int b) {
    return a + b;
}

function void printNum(int a) {
    print(a);
}
```

Read to variable

```cpp
var int a;
read(a);
```

Loops

```cpp
for (i = 0 to 5) {
    print(i);
}

while (i < 5) {
    print(i);
    i = i + 1;
}

do {
    print(i);
    i = i + 1;
} while (i < 5)

```

## License

[MIT](https://choosealicense.com/licenses/mit/)
