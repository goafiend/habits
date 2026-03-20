COLORS_DICT = {
    "black": 30,
    "red": 31,
    "green": 32,
    "brown": 33,
    "blue": 34,
    "purple": 35,
    "teal": 36,
    "grey": 37,
    "white": 38
}

hide = set()
hide.add(35)


def colorprint(color, text):
    """prints a text in a color in the console:
    args: colorname, text
    debugging purposes:
    red: combat
    black: death
    purple: widget not found
    brown: imports


    """
    num = COLORS_DICT[color.lower()]
    if num in hide:
        return 0
    print(f"\033[{num}m{text}\033[38m")


def test():
    while True:
        c = input("what color?")
        colorprint(c, "this is an example text")
