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
            msg += f"{value} : {counts[value]}   ({int(1000) * counts[value] / (sum_count * 10) if sum_count != 0 else 0}%)\n"
        else:
            msg += f"{value} : 0   (0.0%)\n"

    msg += f"\nTOTAL : {sum_count}\n"

    return msg


if __name__ == "__main__":
    # Testing

    test_str = "ex : 1)/ - sport I chose"

    print(parse_keyword(s=test_str, prefix='1'))
