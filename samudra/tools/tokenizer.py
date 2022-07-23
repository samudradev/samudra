import re
from collections import defaultdict
from typing import Dict, Union

REGEX_PATTERN = r"""(?xm)
    (?P<field>      {[_a-zA-Z]{,4}\.[_a-zA-Z]{,3}:\w+}) |
    (?P<tag>        \#[_a-zA-Z0-9\-.]+ ) |
    (               \s{1}) |
    (?P<content>    [\w\d\s,.?!$`_*/&~\\\+\-%()=]+) |
    """


def tokenize(text: str) -> Dict[str, Union[list, str]]:
    to_return = defaultdict(list)
    for match in re.finditer(REGEX_PATTERN, text):
        if match.lastgroup:
            to_return[match.lastgroup].append(match[0])
    if len(to_return['content']) > 1:
        raise SyntaxError({
            "message": "Returns {} texts. Expects 1.".format(len(to_return)),
            "content": "<?> ".join(to_return['content']),
            "body": text
        })
    to_return['content']: str = to_return['content'][0].strip()
    return to_return
