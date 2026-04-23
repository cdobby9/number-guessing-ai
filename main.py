import json
import math
import os
from collections import Counter
import matplotlib.pyplot as plt

# number data
weights = {
    1:129, 2:115, 3:113, 4:105, 5:105, 6:85, 7:182, 8:116, 9:129, 10:59,
    11:98, 12:95, 13:89, 14:79, 15:73, 16:90, 17:94, 18:82, 19:76, 20:88,
    21:64, 22:103, 23:89, 24:76, 25:100, 26:64, 27:101, 28:63, 29:62, 30:63,
    31:70, 32:74, 33:89, 34:55, 35:60, 36:94, 17:94, 50:92, 16:90, 49:89,
    42:89, 33:89, 23:89, 13:89, 20:88, 98:87, 72:87, 81:86, 92:85, 6:85,
    75:82, 18:82, 94:81, 91:81, 76:81, 55:81, 45:81, 52:80, 14:79, 95:78,
    90:78, 43:78, 74:77, 96:76, 56:76, 53:76, 24:76, 19:76, 68:75, 67:75,
    89:74, 73:74, 48:74, 47:74, 32:74, 97:73, 87:73, 82:73, 59:73, 15:73,
    31:70, 93:69, 78:69, 51:69, 86:68, 46:68, 58:67, 71:66, 38:66, 80:65,
    40:65, 61:64, 54:64, 26:64, 21:64, 39:63, 30:63, 28:63, 63:62, 29:62,
    84:61, 41:61, 35:60, 60:59, 10:59, 83:58, 62:58, 79:57, 70:55, 34:55,
    65:53, 85:48, 36:94, 37:119, 44:106, 5:105, 4:105, 22:103, 99:102,
    88:102, 66:102, 27:101, 64:100, 25:100, 57:99, 11:98, 12:95, 69:317,
    77:186, 100:129, 9:129, 1:129, 8:116, 2:115, 3:113, 7:182
}

# sorted
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

total_weight = sum(weights.values())
global_probs = {n: weights[n] / total_weight for n in range(1, 101)}

profile_file = "user_profile.json"

# storage
chosen_before = []
guess_counts = []
correct_this_session = []
current_probs = global_probs.copy()
model_info = {}


def clamp(x, low, high):
    if x < low:
        return low
    if x > high:
        return high
    return x


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    limit = int(n ** 0.5)
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


square_nums = {i * i for i in range(1, 11)}
double_digit_nums = {11, 22, 33, 44, 55, 66, 77, 88, 99}


def get_tens_group(n):
    if n == 100:
        return 10
    return n // 10


number_info = {}
for n in range(1, 101):
    digits = [int(ch) for ch in str(n)]
    number_info[n] = {
        "digits": digits,
        "tens_group": get_tens_group(n),
        "is_prime": 1 if is_prime(n) else 0,
        "is_square": 1 if n in square_nums else 0,
        "is_multiple_5": 1 if n % 5 == 0 else 0,
        "is_multiple_10": 1 if n % 10 == 0 else 0,
        "is_repeated_digit": 1 if n in double_digit_nums else 0,
        "is_single_digit": 1 if n < 10 else 0,
        "is_edge": 1 if n in (1, 100) else 0,
        "is_central": 1 if 40 <= n <= 60 else 0,
        "is_even": 1 if n % 2 == 0 else 0,
    }


tag_names = [
    "is_prime",
    "is_square",
    "is_multiple_5",
    "is_multiple_10",
    "is_repeated_digit",
    "is_single_digit",
    "is_edge",
    "is_central",
    "is_even",
]

base_rates = {
    "digit_occ": {d: 0.0 for d in range(10)},
    "tens": {g: 0.0 for g in range(11)},
    "tags": {tag: 0.0 for tag in tag_names},
}

for n in range(1, 101):
    info = number_info[n]
    for d in info["digits"]:
        base_rates["digit_occ"][d] += 1 / 100
    base_rates["tens"][info["tens_group"]] += 1 / 100
    for tag in tag_names:
        base_rates["tags"][tag] += info[tag] / 100


# loads any old data if it exists

def load_profile():
    global chosen_before, guess_counts

    if not os.path.exists(profile_file):
        chosen_before = []
        guess_counts = []
        return

    try:
        with open(profile_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        loaded_choices = data.get("user_history", [])
        loaded_guess_counts = data.get("guess_history", [])

        chosen_before = [int(x) for x in loaded_choices if 1 <= int(x) <= 100]
        guess_counts = [int(x) for x in loaded_guess_counts if int(x) >= 1]

    except Exception:
        chosen_before = []
        guess_counts = []


def save_profile():
    data = {
        "user_history": chosen_before,
        "guess_history": guess_counts,
    }

    with open(profile_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# makes recent choices matter a bit more than older ones

def get_weighted_history(history, decay=0.92):
    weighted = []
    length = len(history)

    for i, num in enumerate(history):
        w = decay ** (length - 1 - i)
        weighted.append((num, w))

    return weighted


# rebuild the personalised probabilities after each round

def rebuild_model():
    global current_probs, model_info

    if len(chosen_before) == 0:
        current_probs = global_probs.copy()
        model_info = {
            "alpha": 0.0,
            "consistency": 0.0,
            "training_factor": 0.0,
            "repeater_signal": 0.0,
            "history_length": 0,
            "last_choice": None,
            "top_digits": [],
            "favourite_numbers": [],
        }
        return

    weighted_history = get_weighted_history(chosen_before, decay=0.92)
    total_w = sum(w for _, w in weighted_history)

    raw_counts = Counter(chosen_before)
    has_repeat = any(count >= 2 for count in raw_counts.values())

    exact_counts = {n: 0.0 for n in range(1, 101)}
    digit_counts = {d: 0.0 for d in range(10)}
    tens_counts = {g: 0.0 for g in range(11)}
    tag_counts = {tag: 0.0 for tag in tag_names}
    even_total = 0.0
    odd_total = 0.0

    for num, w in weighted_history:
        exact_counts[num] += w

        info = number_info[num]

        for d in info["digits"]:
            digit_counts[d] += w

        tens_counts[info["tens_group"]] += w

        for tag in tag_names:
            if info[tag]:
                tag_counts[tag] += w

        if num % 2 == 0:
            even_total += w
        else:
            odd_total += w

    exact_share = {n: exact_counts[n] / total_w for n in range(1, 101)}
    digit_rate = {d: digit_counts[d] / total_w for d in range(10)}
    tens_rate = {g: tens_counts[g] / total_w for g in range(11)}
    tag_rate = {tag: tag_counts[tag] / total_w for tag in tag_names}

    repeater_signal = 0.0

    if len(chosen_before) >= 2:
        pair_total = 0.0
        pair_score = 0.0
        length = len(chosen_before)

        for i in range(1, length):
            a = chosen_before[i - 1]
            b = chosen_before[i]
            dist = abs(b - a)

            w = 0.92 ** (length - 1 - i)
            close_score = max(0.0, 1 - dist / 15)
            far_score = min(dist / 30, 1.0)
            same_tens = 1.0 if get_tens_group(a) == get_tens_group(b) else 0.0
            exact_repeat = 1.0 if a == b else 0.0

            pair_score += w * (
                0.55 * close_score
                + 0.30 * same_tens
                + 0.40 * exact_repeat
                - 0.55 * far_score
            )
            pair_total += w

        if pair_total > 0:
            repeater_signal = clamp(pair_score / pair_total, -1.0, 1.0)

    unique_ratio = len(set(chosen_before)) / len(chosen_before)
    favourite_share = max(exact_share.values())
    digit_favourite = max(digit_rate.values()) / 2.0
    tens_favourite = max(tens_rate.values())

    repeat_ratio = 0.0
    if len(chosen_before) >= 2:
        repeats = 0
        for i in range(1, len(chosen_before)):
            if chosen_before[i] == chosen_before[i - 1]:
                repeats += 1
        repeat_ratio = repeats / (len(chosen_before) - 1)

    consistency = clamp(
        0.40 * favourite_share * 3.5
        + 0.20 * (1 - unique_ratio)
        + 0.20 * tens_favourite * 2.0
        + 0.10 * digit_favourite * 2.5
        + 0.10 * repeat_ratio,
        0.0,
        1.0,
    )

    training_factor = min(len(chosen_before) / 25, 1.0)
    alpha = clamp(training_factor * (0.25 + 0.75 * consistency), 0.0, 0.85)

    last_choice = chosen_before[-1]
    personal_raw = {}

    for n in range(1, 101):
        info = number_info[n]
        score = 0.0

        # likes exact numbers that come up a lot for this person
        score += 2.6 * (exact_share[n] * 100 - 1.0) / 10.0

        # strongly avoid old exact choices until the user proves they repeat
        if not has_repeat:
            if n in raw_counts:
                score -= 2.9
                if n == last_choice:
                    score -= 0.8
        else:
            if raw_counts.get(n, 0) >= 2:
                score += 0.9 * min(raw_counts[n] - 1, 3)

        # favourite digits
        digit_score = 0.0
        for d in info["digits"]:
            digit_score += digit_rate[d] - base_rates["digit_occ"][d]
        score += 1.7 * digit_score

        # favourite tens group
        score += 1.5 * (tens_rate[info["tens_group"]] - base_rates["tens"][info["tens_group"]])

        # number patterns like prime / square / etc
        for tag in tag_names:
            if info[tag]:
                score += 1.1 * (tag_rate[tag] - base_rates["tags"][tag])

        # odd / even leaning
        if info["is_even"]:
            score += 0.35 * ((even_total / total_w) - 0.5)
        else:
            score += 0.35 * ((odd_total / total_w) - 0.5)

        # whether they stay near old picks or move away from them
        dist = abs(n - last_choice)
        near_bonus = max(0.0, 1 - dist / 15.0)
        far_bonus = min(dist / 30.0, 1.0)

        if repeater_signal >= 0:
            recency_score = repeater_signal * (
                0.85 * near_bonus + 0.35 * (1.0 if n == last_choice else 0.0)
            )
        else:
            recency_score = (-repeater_signal) * (0.75 * far_bonus - 0.15 * near_bonus)

        score += recency_score

        # small extra bits
        if len(chosen_before) >= 6 and n not in chosen_before[-6:]:
            score += 0.08

        if len(chosen_before) >= 6 and n == last_choice and repeater_signal < 0:
            score -= 0.30

        if not has_repeat and n in raw_counts and len(chosen_before) >= 3:
            score -= 0.6

        score = clamp(score, -3.5, 3.5)
        personal_raw[n] = math.exp(score)

    total_personal = sum(personal_raw.values())
    personal_probs = {n: personal_raw[n] / total_personal for n in range(1, 101)}

    current_probs = {}
    for n in range(1, 101):
        current_probs[n] = (1 - alpha) * global_probs[n] + alpha * personal_probs[n]

    total_now = sum(current_probs.values())
    for n in range(1, 101):
        current_probs[n] = current_probs[n] / total_now

    # if they have never repeated a number before, push old exact numbers right down
    if not has_repeat and len(chosen_before) > 0:
        for old_num in set(chosen_before):
            current_probs[old_num] *= 0.02

        total_now = sum(current_probs.values())
        for n in range(1, 101):
            current_probs[n] = current_probs[n] / total_now

    top_digits = sorted(digit_rate.items(), key=lambda x: x[1], reverse=True)[:3]
    favourite_numbers = sorted(exact_share.items(), key=lambda x: x[1], reverse=True)[:5]

    model_info = {
        "alpha": alpha,
        "consistency": consistency,
        "training_factor": training_factor,
        "repeater_signal": repeater_signal,
        "history_length": len(chosen_before),
        "last_choice": last_choice,
        "top_digits": top_digits,
        "favourite_numbers": favourite_numbers,
        "repeat_observed": has_repeat,
    }


def update_after_game(correct_num, guesses_used):
    chosen_before.append(correct_num)
    guess_counts.append(guesses_used)
    save_profile()
    rebuild_model()


# search / guessing part

def midpoint_guess(low, high):
    return (low + high) // 2


def has_repeat_in_history():
    return len(set(chosen_before)) < len(chosen_before)


# midpoint, but avoid old choices if the person has never repeated yet

def novelty_midpoint_guess(low, high, guessed):
    mid = midpoint_guess(low, high)

    if has_repeat_in_history():
        return mid

    old_choices = set(chosen_before)

    if mid not in old_choices:
        return mid

    max_offset = high - low

    for offset in range(1, max_offset + 1):
        left = mid - offset
        right = mid + offset

        if left >= low and left not in guessed and left not in old_choices:
            return left

        if right <= high and right not in guessed and right not in old_choices:
            return right

    return mid


def weighted_guess(low, high, guessed, prob_table):
    best_num = None
    best_prob = -1.0

    for num in range(low, high + 1):
        if num not in guessed:
            if prob_table[num] > best_prob:
                best_prob = prob_table[num]
                best_num = num

    return best_num


def numbers_left(low, high, guessed):
    nums = []
    for num in range(low, high + 1):
        if num not in guessed:
            nums.append(num)
    return nums


def is_clearly_biased(low, high, guessed, prob_table):
    nums = numbers_left(low, high, guessed)

    if len(nums) == 0:
        return False

    if len(nums) >= 15:
        return False

    probs_left = [prob_table[num] for num in nums]
    top_prob = max(probs_left)
    average_prob = sum(probs_left) / len(probs_left)

    return top_prob >= 1.25 * average_prob


# 3 midpoint guesses first, then switch to weighted if the range is small and biased

def choose_guess(low, high, guessed, midpoint_count, prob_table):
    if midpoint_count < 3:
        return novelty_midpoint_guess(low, high, guessed), "midpoint"

    if (high - low + 1) < 15:
        if is_clearly_biased(low, high, guessed, prob_table):
            guess = weighted_guess(low, high, guessed, prob_table)
            if guess is None:
                guess = novelty_midpoint_guess(low, high, guessed)
            return guess, "weighted"

    return novelty_midpoint_guess(low, high, guessed), "midpoint"


def guess_confidence(guess, low, high, guessed, prob_table):
    total_left = 0.0

    for num in range(low, high + 1):
        if num not in guessed:
            total_left += prob_table[num]

    if total_left == 0:
        return 0.0

    return 100 * prob_table[guess] / total_left


# analysis bits

def guesses_needed_for_target(target, prob_table):
    low = 1
    high = 100
    guessed = set()
    midpoint_count = 0
    guesses_used = 0

    while low <= high:
        guess, mode = choose_guess(low, high, guessed, midpoint_count, prob_table)

        if guess in guessed:
            raise RuntimeError("Repeated guess detected during analysis.")

        guessed.add(guess)
        guesses_used += 1

        if mode == "midpoint":
            midpoint_count += 1

        if guess == target:
            return guesses_used

        if target > guess:
            low = guess + 1
        else:
            high = guess - 1

    raise RuntimeError("Analysis failed to find a valid target.")


def expected_average_guesses(prob_table):
    total = 0.0

    for target in range(1, 101):
        total += prob_table[target] * guesses_needed_for_target(target, prob_table)

    return total


# graphs

def plot_guesses_per_game():
    if len(guess_counts) == 0:
        print("No games played yet.")
        return

    plt.figure()
    plt.title("Guesses per Game")
    plt.xlabel("Game #")
    plt.ylabel("Guesses")
    plt.plot(range(1, len(guess_counts) + 1), guess_counts, marker="o")
    plt.show()


def plot_top_personalised_numbers():
    top_nums = sorted(current_probs.items(), key=lambda x: x[1], reverse=True)[:15]
    nums = [item[0] for item in top_nums]
    probs = [item[1] * 100 for item in top_nums]

    plt.figure()
    plt.title("Top 15 Personalised Number Probabilities")
    plt.xlabel("Number")
    plt.ylabel("Probability (%)")
    plt.bar([str(n) for n in nums], probs)
    plt.show()


def plot_strategy_comparison():
    global_avg = expected_average_guesses(global_probs)
    current_avg = expected_average_guesses(current_probs)

    plt.figure()
    plt.title("Expected Average Guesses")
    plt.ylabel("Expected Average")
    plt.bar(["Global only", "Current personalised"], [global_avg, current_avg])
    plt.show()


# info screens

def show_learning_state():
    rebuild_model()

    print("\n--- Personalised Learning State ---")
    print(f"Rounds stored: {model_info['history_length']}")
    print(f"Training factor: {model_info['training_factor']:.3f}")
    print(f"Consistency score: {model_info['consistency']:.3f}")
    print(f"Personalisation strength (alpha): {model_info['alpha']:.3f}")
    print(f"Repeater vs avoider signal: {model_info['repeater_signal']:.3f}")
    print(f"Exact repeat observed yet: {model_info['repeat_observed']}")
    print(f"Last chosen number: {model_info['last_choice']}")

    fav_nums = model_info["favourite_numbers"]
    top_digits = model_info["top_digits"]

    print("\nFavourite numbers so far:")
    if len(fav_nums) == 0:
        print("None yet.")
    else:
        for num, share in fav_nums:
            if share > 0:
                print(f"{num}: {share * 100:.2f}% of weighted history")

    print("\nTop digits so far:")
    if len(top_digits) == 0:
        print("None yet.")
    else:
        for digit, rate in top_digits:
            print(f"{digit}: {rate:.3f} weighted occurrences per choice")

    print("\nTop personalised numbers right now:")
    top_now = sorted(current_probs.items(), key=lambda x: x[1], reverse=True)[:10]
    for num, prob in top_now:
        print(f"{num}: {prob * 100:.3f}%")

    if len(guess_counts) > 0:
        print(f"\nAverage guesses across all stored games: {sum(guess_counts) / len(guess_counts):.2f}")


def show_strategy_analysis():
    rebuild_model()

    global_avg = expected_average_guesses(global_probs)
    current_avg = expected_average_guesses(current_probs)

    print("\n--- Strategy Analysis ---")
    print(f"Global-only expected average: {global_avg:.4f}")
    print(f"Current personalised expected average: {current_avg:.4f}")

    if model_info["history_length"] == 0:
        print("No personalised data yet, so both are effectively the same.")
    else:
        difference = global_avg - current_avg
        print(f"Improvement from personalisation: {difference:.4f} guesses")

    plot_strategy_comparison()


# main game

def play_game():
    rebuild_model()

    low = 1
    high = 100
    guessed = set()
    midpoint_count = 0
    guesses_used = 0
    contradictions = 0
    mode_history = []

    print("\nThink of a HUMAN-CHOSEN number from 1 to 100.")
    print("This version uses:")
    print("- 3 midpoint guesses first")
    print("- then a dynamic weighted switch")
    print("- plus personalised post-game learning")

    while low <= high:
        guess, mode = choose_guess(low, high, guessed, midpoint_count, current_probs)

        if guess is None:
            print("No valid guess could be found.")
            return

        confidence = guess_confidence(guess, low, high, guessed, current_probs)

        print(f"\nLower bound: {low}")
        print(f"Upper bound: {high}")
        print(f"Guess number: {guesses_used + 1}")
        print(f"Mode: {mode}")
        print(f"Current personalisation strength: {model_info['alpha']:.3f}")
        print(f"Current confidence in this guess: {confidence:.2f}%")
        print(f"Is your number {guess}?")

        response = input("Enter 'h' for higher, 'l' for lower, or 'c' for correct: ").strip().lower()

        if response not in ("h", "l", "c"):
            print("Invalid input. Please enter 'h', 'l', or 'c'.")
            continue

        if guess in guessed:
            print("A repeated guess was detected. Stopping.")
            return

        guessed.add(guess)
        guesses_used += 1
        mode_history.append(mode)

        if mode == "midpoint":
            midpoint_count += 1

        if response == "c":
            correct_this_session.append(guess)
            update_after_game(guess, guesses_used)

            average_guesses = sum(guess_counts) / len(guess_counts)

            print(f"\nYour number is {guess}")
            print("\nPerformance Report:")
            print(f"Guesses this round: {guesses_used}")
            print(f"Average guesses across all stored rounds: {average_guesses:.2f}")
            print(f"Contradictions: {contradictions}")
            print(f"Mode history this round: {mode_history}")
            print(f"Rounds stored in personal model: {len(chosen_before)}")

            return

        if response == "h":
            low = guess + 1
        elif response == "l":
            high = guess - 1

        if low > high:
            contradictions += 1
            print("\nThere was a contradiction in the answers. No number fits that pattern.")
            return


# wipe saved learning if needed

def reset_personal_learning():
    global chosen_before, guess_counts, current_probs, model_info

    confirm = input("Type 'RESET' to wipe all personalised learning data: ").strip()

    if confirm == "RESET":
        chosen_before = []
        guess_counts = []
        current_probs = global_probs.copy()
        model_info = {}
        save_profile()
        rebuild_model()
        print("All personalised learning data was reset.")
    else:
        print("Reset cancelled.")


def main():
    load_profile()
    rebuild_model()

    while True:
        print("\n--- Adaptive Number Guessing Project ---")
        print("1. Play the full personalised version")
        print("2. Show personalised learning state")
        print("3. Show strategy analysis")
        print("4. Plot guesses per game")
        print("5. Plot top personalised numbers")
        print("6. Reset personalised learning")
        print("7. Quit")

        choice = input("Choose 1-7: ").strip()

        if choice == "1":
            play_game()
        elif choice == "2":
            show_learning_state()
        elif choice == "3":
            show_strategy_analysis()
        elif choice == "4":
            plot_guesses_per_game()
        elif choice == "5":
            plot_top_personalised_numbers()
        elif choice == "6":
            reset_personal_learning()
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
