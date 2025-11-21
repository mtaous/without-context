# Pointers in C

## What are Pointers?

A pointer is a variable that stores the memory address of another variable. Instead of holding a direct value, a pointer "points to" the location in memory where the actual data is stored.

## Declaration and Initialization

```c
int x = 10;        // Regular variable
int *ptr = &x;     // Pointer to int, stores address of x
```

The `*` denotes a pointer type, and `&` is the "address-of" operator that returns a variable's memory address.

## Dereferencing

To access the value at the address a pointer holds, use the `*` operator (dereferencing):

```c
int value = *ptr;  // Gets the value at the address (10)
*ptr = 20;         // Modifies the value at that address
```

## Why Use Pointers?

- **Dynamic Memory**: Allocate memory at runtime using `malloc()` and `free()`
- **Efficient Data Passing**: Pass large structures by reference instead of copying
- **Arrays and Strings**: Array names are pointers to their first element
- **Data Structures**: Essential for linked lists, trees, and graphs

## Common Pitfalls

- **Uninitialized Pointers**: Always initialize pointers before use
- **Null Pointers**: Check for NULL before dereferencing
- **Memory Leaks**: Free dynamically allocated memory when done
- **Dangling Pointers**: Avoid using pointers after the memory they point to has been freed
