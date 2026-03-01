previous_numbers = []
previous_number_of_guesses = []

def main():
    lower_bound = 0
    upper_bound = 100
    number_of_guesses = 1
    contradictions = 0

    while lower_bound <= upper_bound:
        guess = (lower_bound + upper_bound) // 2
       
        
        print(f"Upper bound: {upper_bound}")
        print(f"Lower bound: {lower_bound}")
        print(f"number of guesses: {number_of_guesses}")
        print(f"Is your number {guess}?")
        response = input("Enter 'h' if your number is higher, 'l' if it is lower, or 'c' if it is correct: ")
        
        if response != 'c':
            number_of_guesses = number_of_guesses + 1

        if upper_bound - lower_bound <= 1 and response != 'c':
            contradictions += 1

        if response == 'h':
            lower_bound = guess + 1
        elif response == 'l':
            upper_bound = guess - 1
        elif response == 'c':
            previous_numbers.append(guess)
            previous_number_of_guesses.append(number_of_guesses)
            average_guesses = sum(previous_number_of_guesses) / len(previous_number_of_guesses)

            print(f"Your number is {guess}")
            print(f"Performance Report:")
            print(f"Number of contractions: {contradictions}")
            print(f"Previous numbers guessed: {previous_numbers}")
            print(f"Number of guesses: {number_of_guesses}")
            print(f"Average Number of Guesses: {average_guesses}")
            print(f"Confidence this was correct: {100 / (upper_bound - lower_bound + 1):.2f}%")

            return
        else:
            print("Invalid input. Please enter 'h', 'l', or 'c'.")

while True:
    main()
    