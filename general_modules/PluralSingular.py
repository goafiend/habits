
def adapt_ending(str, amount):
    if str[-1] != "s":
        if amount > 1:
            new_str = f"{str}s"
            return new_str
    return str