import sys


def confirmation_prompt(prompt, default=True):
    valid = {"y": True, "yes": True, "n": False, "no": False}

    if default:
        option = " [Y/n] "
    else:
        option = " [y/N] "

    while True:
        sys.stdout.write(prompt + option)
        inp = input().lower().strip()

        if inp == "":
            return default
        elif inp in valid:
            return valid[inp]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'\n")
