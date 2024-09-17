def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else: 
        return fibonacci(n-1) + fibonacci(n-2)

def factorial(n):
    if n == 0:
        return 1
    else: 
        return n * factorial(n-1)

def menu():
    while True: 
        try:
            n = int(input("\nInput n: "))
        except ValueError:
            print("Please enter a valid integer.")
            continue

        print("""\nChoose an operation to be done: 
        1. Fibonacci
        2. Factorial
        3. Exit""")

        try:
            operation = int(input("\nYour option (1/2/3): "))
        except ValueError:
            print("Please enter a valid option.")
            continue

        if operation == 1:
            print(f"Fibonacci of n={n} is {fibonacci(n)}")
        elif operation == 2:
            print(f"Factorial of {n}! is {factorial(n)}")
        elif operation == 3:
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    menu()
