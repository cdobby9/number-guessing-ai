def main():
    lower_bound = 0
    upper_bound = 100
    previous_numbers = []

    while lower_bound <= upper_bound:
        guess = (lower_bound + upper_bound) // 2
        previous_numbers.append(guess)
        print(f"Is your number {guess}?")
        response = input("Enter 'h' if your number is higher, 'l' if it is lower, or 'c' if it is correct: ")

        if response == 'h':
            lower_bound = guess + 1
        elif response == 'l':
            upper_bound = guess - 1
        elif response == 'c':
            print(f"Your number is {guess}!")
            print(f"Previous numbers guessed: {previous_numbers}")
            return
        else:
            print("Invalid input. Please enter 'h', 'l', or 'c'.")

while True:
    main()
    