with open("./Input/Names/invited_names.txt", mode='r') as invited_names:
    names = invited_names.read().splitlines()

with open("./Input/Letters/starting_letter.txt", mode='r') as starting_letter:
    letter = starting_letter.read()
    for name in names:
        with open(f"./Output/letter_for_{name}.txt", mode='w') as letter_to_send:
            replaced_name_letter = letter.replace("[name]", name)
            letter_to_send.write(replaced_name_letter)
