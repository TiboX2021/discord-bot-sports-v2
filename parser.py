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
    while end_index < length - 1 and s[end_index].isalpha():
        end_index += 1

    return s[index:end_index].lower()  # lowercase for easier matching


if __name__ == "__main__":
    # Testing

    test_str = "ex : 1)/ - sport I chose"

    print(parse_keyword(s=test_str, prefix='1'))
