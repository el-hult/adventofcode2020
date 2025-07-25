from util import read_input


def processA(input,to_report=2020):
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
    return processA(input, to_report=30000000)


def main():
    true_input = read_input(15)
    ansA = processA(true_input)
    assert ansA == 610

    ansB = processB(true_input)
    assert ansB == 1407


if __name__ == "__main__":
    main()
