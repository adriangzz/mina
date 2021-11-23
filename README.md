# Mina

Mina is a compiler made entirely with Python using PLY (Python Lex-Yacc).
The compiler uses a virtual machine to keep track of memory use.

## Installation

To use the compiler, Python 3 must be installed in the system

## Usage

Run:

```bash
python3 main.py <filename>
```

## Manual

Program Structure

```
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

    // Read from console into variable a
    read(a);

    // If statement
    if (5 > 3) {
        print("This is true!");
    }

    // If-else statement
    if (5 < 3) {
        print("This will not print :( ");
    } else {
        print("This will print!", "Also this!");
    }

    // While loop
    while (a < 5) {
        print("This will print until a is less than 5!");
        a = a + 1;
    }

    // For loop
    for (a = 1 to 6) {
        print("This will print 5 times");
    }
}
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
