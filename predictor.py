import random


def update_counts(data):
    for i in range(3, len(data)):
        if data[i] == "0":
            counts_dict[data[i-3:i]]["0"] += 1
        elif data[i] == "1":
            counts_dict[data[i-3:i]]["1"] += 1


def predict(test, ratio):
    """Based on the test string and frequencies in the data string
    builds a prediction string and returns the number of symbols guessed correctly"""
    prediction = "".join(random.choices("01", cum_weights=(ratio, 1), k=3))
    right_guesses = 0
    for index, symbol in enumerate(test[3:], 3):
        # look up in the counts dictionary for the triad before
        # predict the more frequent outcome or choose randomly
        triad = test[index-3:index]
        if counts_dict[triad]["0"] > counts_dict[triad]["1"]:
            predicted_symbol = "0"
        elif counts_dict[triad]["0"] < counts_dict[triad]["1"]:
            predicted_symbol = "1"
        else:
            predicted_symbol = random.choices("01", cum_weights=(ratio, 1), k=1)[0]
        prediction += predicted_symbol
        if symbol == predicted_symbol:
            right_guesses += 1
    print("prediction:")
    print(prediction)
    print()
    return right_guesses


def evaluate_prediction(right_guesses, total):
    """Depending on the number of right guesses and the total number of symbols in the test string
    calculates the accuracy and returns the change affecting the balance"""
    accuracy = round(right_guesses * 100 / total, 2)
    print("Computer guessed right {0} out of {1} symbols ({2} %)".format(right_guesses, total, accuracy))
    return total - right_guesses * 2


# initialize the variables data, balance, triads and the dictionary of counts
data = ""
balance = 1000
triads = ["000", "001", "010", "011", "100", "101", "110", "111"]
counts_dict = {triad: {"0": 0, "1": 0} for triad in triads}

# Print the opening sentence
print("Please give AI some data to learn... ")

# Collect the data
while len(data) < 100:
    print("The current data length is {0}, {1} symbols left".format(len(data), 100-len(data)))
    value = input("Print a random string containing 0 or 1:\n")
    for symbol in value:
        if symbol == "0" or symbol == "1":
            data += symbol

update_counts(data)

# Print the collected data and the rule of the game
print("Final data string:")
print(data)
print()
print("""You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!""")

# game loop
while True:
    # accept test string
    test_raw = input("Print a random string containing 0 or 1:\n")

    # finish the game if it is enough
    if test_raw == "enough":
        print("Game over!")
        break

    # clean the test string
    test = "".join(symbol for symbol in test_raw if symbol == "0" or symbol == "1")

    # ask for a new test string if it has too few data
    if len(test) < 4:
        continue

    # ratio of zeros in data
    ratio_zeros = data.count("0") / len(data)

    right_guesses = predict(test, ratio_zeros)

    # update the balance
    balance += evaluate_prediction(right_guesses, len(test) - 3)
    print("Your balance is now ${0}".format(balance))
    if balance < 1:
        print("Game over!")
        break

    update_counts(test)

