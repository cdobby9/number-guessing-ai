import matplotlib.pyplot as plt
from torch import clamp


previous_numbers = []
previous_number_of_guesses = []
final_confidence_per_game = []

def main():
    lower_bound = 0
    upper_bound = 100
    number_of_guesses = 1
    contradictions = 0
    confidence = 0
    confidence_history = [confidence]

    while lower_bound <= upper_bound:
        guess = (lower_bound + upper_bound) // 2
       
        
        print(f"Upper bound: {upper_bound}")
        print(f"Lower bound: {lower_bound}")
        print(f"number of guesses: {number_of_guesses}")
        print(f"Confidence: {confidence:.1f}%")
        print(f"Is your number {guess}?")

        response = input("Enter 'h' if your number is higher, 'l' if it is lower, or 'c' if it is correct: ")
        
        if response != 'c':
            number_of_guesses += 1

        if response == 'h':
            lower_bound = guess + 1
        elif response == 'l':
            upper_bound = guess - 1

        elif response == 'c':
            previous_numbers.append(guess)
            previous_number_of_guesses.append(number_of_guesses)
            final_confidence_per_game.append(confidence)            
            average_guesses = sum(previous_number_of_guesses) / len(previous_number_of_guesses)

            print(f"\n\n\nYour number is {guess}")
            print(f"Number of guesses: {number_of_guesses}")

            print("\nPerformance Report:")
            print(f"Final confidence: {confidence:.1f}%")            
            print(f"Number of contractions: {contradictions}")
            print(f"Average Number of Guesses: {average_guesses:.2f}")
            print(f"Previous numbers guessed: {previous_numbers}\n\n\n\n")
            

            plot(previous_number_of_guesses)
            return
        
        if lower_bound > upper_bound:
            contradictions += 1
            confidence = clamp(confidence - 20, 1, 99)
            confidence_history.append(confidence)
            print("There was an error with your answers. No number guessable.")

        else:
            print("Invalid input. Please enter 'h', 'l', or 'c'.")

        confidence_history.append(confidence)

def plot(previous_number_of_guesses):
    plt.figure()
    plt.title("Guesses per Game")
    plt.xlabel("Game #")
    plt.ylabel("Guesses")
    plt.plot(range(1, len(previous_number_of_guesses) + 1), previous_number_of_guesses)
    plt.show()

while True:
    main()
    