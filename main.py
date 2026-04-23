import matplotlib.pyplot as plt

# data from the write-up
weights = {
    69: 317, 77: 186, 7: 182, 100: 129, 9: 129, 1: 129, 37: 119, 8: 116, 2: 115, 3: 113,
    44: 106, 5: 105, 4: 105, 22: 103, 99: 102, 88: 102, 67: 102, 27: 101, 64: 100, 25: 100,
    57: 99, 11: 98, 12: 95, 36: 94, 17: 94, 50: 92, 16: 90, 49: 89, 42: 89, 33: 89,
    23: 89, 13: 89, 20: 88, 98: 87, 72: 87, 81: 86, 92: 85, 6: 85, 75: 82, 18: 82,
    94: 81, 91: 81, 76: 81, 55: 81, 45: 81, 52: 80, 14: 79, 95: 78, 90: 78, 43: 78,
    74: 77, 96: 76, 56: 76, 53: 76, 24: 76, 19: 76, 68: 75, 66: 75, 89: 74, 73: 74,
    48: 74, 47: 74, 32: 74, 97: 73, 87: 73, 82: 73, 59: 73, 15: 73, 31: 70, 93: 69,
    78: 69, 51: 69, 86: 68, 46: 68, 58: 67, 71: 66, 38: 66, 80: 65, 40: 65, 61: 64,
    54: 64, 26: 64, 21: 64, 39: 63, 30: 63, 28: 63, 63: 62, 29: 62, 84: 61, 41: 61,
    35: 60, 60: 59, 10: 59, 83: 58, 62: 58, 79: 57, 70: 55, 34: 55, 65: 53, 85: 48
}

TOTAL_WEIGHT = sum(weights.values())

# storing stats from previous games
previous_numbers = []
previous_number_of_guesses = []
previous_modes = []


# finds the middle number in the current range
def midpoint_guess(lower_bound, upper_bound):
    return (lower_bound + upper_bound) // 2


# picks the number with the biggest weight that hasn't been guessed yet
def weighted_guess(lower_bound, upper_bound, guessed_set):
    best_number = None
    best_weight = -1

    for number, weight in weights.items():
        if lower_bound <= number <= upper_bound and number not in guessed_set:
            if weight > best_weight:
                best_weight = weight
                best_number = number

    return best_number


# gets all the numbers left in the range that haven't been guessed
def remaining_numbers(lower_bound, upper_bound, guessed_set):
    return [n for n in range(lower_bound, upper_bound + 1) if n not in guessed_set]


# checks if the remaining numbers are clearly biased
def remaining_is_clearly_biased(lower_bound, upper_bound, guessed_set):
    """
    only switch if:
    - there are less than 15 numbers left
    - the top weight is at least 1.25 times the average
    """
    nums = remaining_numbers(lower_bound, upper_bound, guessed_set)

    if len(nums) == 0:
        return False

    if len(nums) >= 15:
        return False

    remaining_weights = [weights[n] for n in nums]
    top_weight = max(remaining_weights)
    average_weight = sum(remaining_weights) / len(remaining_weights)

    return top_weight >= 1.25 * average_weight


# normal binary search
def choose_guess_binary(lower_bound, upper_bound, guessed_set, midpoint_guesses_made):
    return midpoint_guess(lower_bound, upper_bound), "binary"


# always chooses the best weighted option first
def choose_guess_greedy_weighted(lower_bound, upper_bound, guessed_set, midpoint_guesses_made):
    guess = weighted_guess(lower_bound, upper_bound, guessed_set)

    if guess is None:
        guess = midpoint_guess(lower_bound, upper_bound)

    return guess, "greedy_weighted"


# first 3 midpoint guesses, then weighted guesses
def choose_guess_fixed_switch(lower_bound, upper_bound, guessed_set, midpoint_guesses_made):
    if midpoint_guesses_made < 3:
        return midpoint_guess(lower_bound, upper_bound), "midpoint"
    else:
        guess = weighted_guess(lower_bound, upper_bound, guessed_set)

        if guess is None:
            guess = midpoint_guess(lower_bound, upper_bound)

        return guess, "weighted"


# dynamic version from the write-up
def choose_guess_dynamic_switch(lower_bound, upper_bound, guessed_set, midpoint_guesses_made):
    if midpoint_guesses_made < 3:
        return midpoint_guess(lower_bound, upper_bound), "midpoint"

    if (upper_bound - lower_bound + 1) < 15 and remaining_is_clearly_biased(lower_bound, upper_bound, guessed_set):
        guess = weighted_guess(lower_bound, upper_bound, guessed_set)

        if guess is None:
            guess = midpoint_guess(lower_bound, upper_bound)

        return guess, "weighted"

    return midpoint_guess(lower_bound, upper_bound), "midpoint"


# works out how many guesses a strategy needs for a target number
def guesses_needed_for_target(target, choose_guess_function):
    lower_bound = 1
    upper_bound = 100
    guessed_set = set()
    midpoint_guesses_made = 0
    number_of_guesses = 0

    while lower_bound <= upper_bound:
        guess, mode = choose_guess_function(lower_bound, upper_bound, guessed_set, midpoint_guesses_made)

        if guess in guessed_set:
            raise RuntimeError("Repeated guess detected.")

        guessed_set.add(guess)
        number_of_guesses += 1

        if mode in ("binary", "midpoint"):
            midpoint_guesses_made += 1

        if guess == target:
            return number_of_guesses
        elif target > guess:
            lower_bound = guess + 1
        else:
            upper_bound = guess - 1

    raise RuntimeError("No valid number could be guessed.")


# finds the expected average number of guesses for a strategy
def expected_average_guesses(choose_guess_function):
    total = 0

    for target in range(1, 101):
        probability = weights[target] / TOTAL_WEIGHT
        guesses = guesses_needed_for_target(target, choose_guess_function)
        total += probability * guesses

    return total


# shows the averages for all strategies and plots them
def show_strategy_analysis():
    binary_average = expected_average_guesses(choose_guess_binary)
    greedy_average = expected_average_guesses(choose_guess_greedy_weighted)
    fixed_switch_average = expected_average_guesses(choose_guess_fixed_switch)
    dynamic_switch_average = expected_average_guesses(choose_guess_dynamic_switch)

    print("\n--- Strategy Analysis ---")
    print(f"Total data count used by this code: {TOTAL_WEIGHT}")
    print(f"Binary search expected average: {binary_average:.4f}")
    print(f"Greedy weighted expected average: {greedy_average:.4f}")
    print(f"Fixed switch after 3 midpoint guesses expected average: {fixed_switch_average:.4f}")
    print(f"Dynamic switch expected average: {dynamic_switch_average:.4f}")

    plt.figure()
    names = ["Binary", "Greedy\nWeighted", "3 Midpoints\nThen Weighted", "Dynamic\nSwitch"]
    values = [binary_average, greedy_average, fixed_switch_average, dynamic_switch_average]
    plt.bar(names, values)
    plt.title("Expected Average Guesses by Strategy")
    plt.ylabel("Expected Average Guesses")
    plt.show()


# lets the user play the game
def play_game():
    lower_bound = 1
    upper_bound = 100
    guessed_set = set()
    midpoint_guesses_made = 0
    number_of_guesses = 0
    contradictions = 0
    mode_history = []

    print("\nThink of a human-chosen number from 1 to 100.")
    print("I will use the final dynamic strategy from your write-up.")

    while lower_bound <= upper_bound:
        guess, mode = choose_guess_dynamic_switch(lower_bound, upper_bound, guessed_set, midpoint_guesses_made)

        if guess is None:
            print("No valid guess could be found.")
            return

        if guess in guessed_set:
            print("A repeated guess was detected. Stopping.")
            return

        guessed_set.add(guess)

        if mode == "midpoint":
            midpoint_guesses_made += 1

        print(f"\nLower bound: {lower_bound}")
        print(f"Upper bound: {upper_bound}")
        print(f"Guess number: {number_of_guesses + 1}")
        print(f"Search mode: {mode}")
        print(f"Is your number {guess}?")

        response = input("Enter 'h' for higher, 'l' for lower, or 'c' for correct: ").strip().lower()

        if response not in ("h", "l", "c"):
            print("Invalid input. Please enter 'h', 'l', or 'c'.")
            guessed_set.remove(guess)

            if mode == "midpoint":
                midpoint_guesses_made -= 1

            continue

        number_of_guesses += 1
        mode_history.append(mode)

        if response == "c":
            previous_numbers.append(guess)
            previous_number_of_guesses.append(number_of_guesses)
            previous_modes.append(mode_history)

            average_guesses = sum(previous_number_of_guesses) / len(previous_number_of_guesses)

            print(f"\nYour number is {guess}")
            print("\nPerformance Report:")
            print(f"Number of guesses this round: {number_of_guesses}")
            print(f"Average number of guesses across rounds: {average_guesses:.2f}")
            print(f"Contradictions: {contradictions}")
            print(f"Mode history this round: {mode_history}")
            print(f"Previous numbers guessed correctly: {previous_numbers}")

            plot_guesses_per_game()
            return

        elif response == "h":
            lower_bound = guess + 1
        elif response == "l":
            upper_bound = guess - 1

        if lower_bound > upper_bound:
            contradictions += 1
            print("\nThere was a contradiction in the answers. No number fits that pattern.")
            return


# plots how many guesses each game took
def plot_guesses_per_game():
    if len(previous_number_of_guesses) == 0:
        return

    plt.figure()
    plt.title("Guesses per Game")
    plt.xlabel("Game #")
    plt.ylabel("Guesses")
    plt.plot(range(1, len(previous_number_of_guesses) + 1), previous_number_of_guesses, marker="o")
    plt.show()


# main menu
def main():
    while True:
        print("\n--- Number Guessing Project ---")
        print("1. Play the final dynamic-switch version")
        print("2. Show strategy analysis")
        print("3. Quit")

        choice = input("Choose 1, 2 or 3: ").strip()

        if choice == "1":
            play_game()
        elif choice == "2":
            show_strategy_analysis()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()