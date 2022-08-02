"""
Find the first keyword following a prefix
"""


def parse_keyword(s: str, prefix: str) -> str | None:
    """:returns the first string that follows a prefix, else None if none was found"""

    # Searching for the prefix
    index = s.find(prefix)

    if index == -1:  # Prefix not found
        return None

    length = len(s)

    # Scanning next word
    # Skip through 's' until the next letter (skips symbols, spaces, ...)
    index += 1
    while not s[index].isalpha():
        index += 1
        if index >= length:  # Reached end of string
            return None

    # Find end of word
    end_index = index + 1
    while s[end_index].isalpha():

        end_index += 1

        if end_index == length:
            break

    return s[index:end_index].lower()  # lowercase for easier matching


def next_alpha(s: str, begin: int) -> int:
    """Returns the index of the next alphabet letter in s.
    If the end of string is reached, returns -1.
    Index begin is not included."""

    i = begin + 1

    if i >= len(s):
        return -1

    while not s[i].isalpha():
        i += 1
        if i == len(s):
            return -1
    return i


def next_end_of_word(s: str, begin: int) -> int:
    """Returns the next index of the first character that is not a letter.
    If the end of the string is reached, returns -1"""
    assert s[begin].isalpha(), "Error : the starting char is not a letter"

    i = begin + 1
    while s[i].isalpha():
        i += 1
        if i == len(s):
            return -1
    return i


def scan_next_word(s: str, begin: int) -> tuple[str | None, int]:
    """Returns the next word after s[begin] char, not included. Returns None if none was found.
    Also returns the index of the words' last char"""
    begin = next_alpha(s, begin)

    if begin == -1:
        return None, -1

    end = next_end_of_word(s, begin)

    return (s[begin:len(s)], len(s) - 1) if end == -1 else (s[begin:end], end - 1)


def parse_keywords(s: str, prefix: str, n: int = 1) -> [str]:
    """parse_keyword, but returns the 'n' following words"""

    # Searching for the prefix
    index = s.find(prefix)

    if index == -1:  # No prefix found
        return []

    # Scanning next words
    out = []
    end = index

    for i in range(n):
        word, end = scan_next_word(s, end)
        if word is None:
            return out

        out.append(word)
    return out


def value_count(history: dict[str, str]) -> dict[str, int]:
    """Counts all value in the dict
    @:returns dict[value: str, count: int]"""
    out: dict[str, int] = {}

    for value in history.values():
        if value in out:
            out[value] += 1
        else:
            out[value] = 1

    return out


def summary_msg(history: dict[str, str], values: set[str]) -> str:
    """Returns a summary message of the value count
    for the bot to display"""

    counts = value_count(history)
    sum_count = sum(counts.values())

    msg = ""

    for value in values:
        if value in counts:
            msg += f"{value} : {counts[value]}   ({int(1000 * counts[value] / sum_count) / 10 if sum_count != 0 else 0}%)\n"
        else:
            msg += f"{value} : 0   (0.0%)\n"

    msg += f"\nTOTAL : {sum_count}\n"

    return msg


if __name__ == "__main__":
    # Testing

    test_str = "ex : 1)/ - sport I chose"

    print(parse_keyword(s=test_str, prefix='1'))

    test_str_2 = "ex : 1)/ foot le hand truc"

    print(parse_keywords(test_str_2, '1', 3))

    test_str_3 = "ex : 1 truc"

    print(parse_keywords(test_str_3, '1', 10))
