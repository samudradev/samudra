import re
from collections import defaultdict
from typing import Dict

import pydantic

REGEX_PATTERN = r"""(?xm)
    (?P<annotation> {[a-zA-Z]{,2}:[_a-zA-Z]+}) |
    (?P<tag>        \#[_a-zA-Z0-9\-.]+ ) |
    (               \s{1}) |
    (?P<text>       [\w\d\s,.?!$`_*/&~\\\+\-%()=]+) |
    """


def tokenize(text: str) -> Dict[str, list]:
    to_return = defaultdict(list)
    for match in re.finditer(REGEX_PATTERN, text):
        if match.lastgroup:
            to_return[match.lastgroup].append(match[0])
    if len(to_return['text']) > 1:
        raise SyntaxError(
            "Returns {} texts. Expects 1. "
            "Look for offending characters below\n"
            "---\n"
            "Parsed\t\t:{}\n"
            "Received\t:{}"
            .format(len(to_return['text']), '<?> '.join(to_return['text']), text))
    print(to_return)
    to_return['text'][0] = to_return['text'][0].strip()
    return to_return
