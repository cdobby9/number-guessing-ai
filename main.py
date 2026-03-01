import matplotlib.pyplot as plt
from torch import clamp


previous_numbers = []
previous_number_of_guesses = []
final_confidence_per_game = []

weights = {
    1:129, 2:115, 3:113, 4:105, 5:105, 6:85, 7:182, 8:116, 9:129, 10:59,
    11:98, 12:95, 13:89, 14:79, 15:73, 16:90, 17:94, 18:82, 19:76, 20:88,
    21:64, 22:103, 23:89, 24:76, 25:100, 26:64, 27:101, 28:63, 29:62, 30:63,
    31:70, 32:74, 33:89, 34:55, 35:60, 36:94, 37:119, 38:66, 39:63, 40:65,
    41:61, 42:89, 43:78, 44:106, 45:81, 46:68, 47:74, 48:74, 49:89, 50:92,
    51:69, 52:80, 53:76, 54:64, 55:81, 56:76, 57:99, 58:67, 59:73, 60:59,
    61:64, 62:58, 63:62, 64:100, 65:53, 66:102, 67:75, 68:75, 69:317, 70:55,
    71:66, 72:87, 73:74, 74:77, 75:82, 76:81, 77:186, 78:69, 79:57, 80:65,
    81:86, 82:73, 83:58, 84:61, 85:48, 86:68, 87:73, 88:102, 89:74, 90:78,
    91:81, 92:85, 93:69, 94:81, 95:78, 96:76, 97:73, 98:87, 99:102, 100:129
}

def weighted_guess(lower_bound, upper_bound, weights):
    nearest_weighted_number = None
    nearest_weighted_weight = -1

    for number, weight in weights.items():
        if lower_bound <= number <= upper_bound and weight > nearest_weighted_weight:
            nearest_weighted_number = number
            nearest_weighted_weight = weight

    return nearest_weighted_number


def main():
    lower_bound = 0
    upper_bound = 100
    number_of_guesses = 1
    contradictions = 0
    confidence = 0
    confidence_history = [confidence]

    while lower_bound <= upper_bound:

        guess = weighted_guess(lower_bound, upper_bound, weights)
        if guess is None:
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
    