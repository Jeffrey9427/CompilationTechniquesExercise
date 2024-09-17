import keyword

def print_per_character(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

def print_keyword(filename):
    keywords = []
    with open(filename, 'r') as file:
        text = file.read()  # read the entire file content
        words = text.split()  # split the text into words based on whitespace
        for word in words:
            if keyword.iskeyword(word):  # check if each word is a keyword
                keywords.append(word)

    return '\n'.join(keywords)

filename = "exercise1.py"

def menu():
    while True: 
        print("""\nChoose an operation to be done: 
        1. PRINT PER CHARACTER 
        2. PRINT ALL THE KEYWORDS
        3. Exit""")

        try:
            operation = int(input("\nYour option (1/2/3): "))
        except ValueError:
            print("Please enter a valid option.")
            continue

        if operation == 1:
            print(print_per_character(filename))
        elif operation == 2:
            print(print_keyword(filename))
        elif operation == 3:
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    menu()