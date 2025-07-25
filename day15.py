from util import read_input


def processA(input,to_report=2020):
    """
    You catch the airport shuttle and try to book a new flight to your vacation island. 
    Due to the storm, all direct flights have been cancelled, but a route is available to get around the storm. You take it.

    While you wait for your flight, you decide to check in with the Elves back at the North Pole. 
    They're playing a memory game and are ever so excited to explain the rules!

    In this game, the players take turns saying numbers. 
    They begin by taking turns reading from a list of starting numbers (your puzzle input). 
    Then, each turn consists of considering the most recently spoken number:

    - If that was the first time the number has been spoken, the current player says 0.
    - Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.

    So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or an age (if the last number is a repeat).

    (The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)

    Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be 436.
    """
    starting_numbers = tuple(map(int, input.split(',')))
    last_turn_this_was_spoken = {num: idx + 1 for idx, num in enumerate(starting_numbers[:-1])} # dont include the last number. it gets special treatment.
    prev_unumber = starting_numbers[-1]

    # first round is special
    current_turn = len(starting_numbers) + 1
    while current_turn <= to_report:
        if prev_unumber in last_turn_this_was_spoken:
            # spoken before, calculate age
            last_turn = last_turn_this_was_spoken[prev_unumber]
            current_number = current_turn - last_turn - 1 
        else:
            # first time spoken
            current_number = 0
        
        # update the last turn this number was spoken
        last_turn_this_was_spoken[prev_unumber] = current_turn -1
        
        # prepare for next turn
        prev_unumber = current_number
        current_turn += 1
        
      

    return current_number


def processB(input):
    """
    Impressed, the Elves issue you a challenge: determine the 30000000th number spoken. For example, given the same starting numbers as above:

    Given 0,3,6, the 30000000th number spoken is 175594.
    Given 1,3,2, the 30000000th number spoken is 2578.
    Given 2,1,3, the 30000000th number spoken is 3544142.
    Given 1,2,3, the 30000000th number spoken is 261214.
    Given 2,3,1, the 30000000th number spoken is 6895259.
    Given 3,2,1, the 30000000th number spoken is 18.
    Given 3,1,2, the 30000000th number spoken is 362.

    Given your starting numbers, what will be the 30000000th number spoken?
    """
    return processA(input, to_report=30000000)


def main():
    true_input = read_input(15)
    ansA = processA(true_input)
    assert ansA == 610

    ansB = processB(true_input)
    assert ansB == 1407


if __name__ == "__main__":
    main()
