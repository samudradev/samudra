import re
from collections import defaultdict
from typing import Dict

import pydantic

REGEX_PATTERN = r"""(?xm)
    (?P<annotation> {[_a-zA-Z]{,4}\.[_a-zA-Z]{,3}:\w+}) |
    (?P<tag>        \#[_a-zA-Z0-9\-.]+ ) |
    (               \s{1}) |
    (?P<content>    [\w\d\s,.?!$`_*/&~\\\+\-%()=]+) |
    """


def tokenize(text: str) -> Dict[str, list]:
    to_return = defaultdict(list)
    for match in re.finditer(REGEX_PATTERN, text):
        if match.lastgroup:
            to_return[match.lastgroup].append(match[0])
    if len(to_return['content']) > 1:
        raise SyntaxError(
            "Returns {} texts. Expects 1. "
            "Look for offending characters below\n"
            "---\n"
            "Parsed\t\t:{}\n"
            "Received\t:{}"
            .format(len(to_return['content']), '<?> '.join(to_return['content']), text))
    to_return['content'] = to_return['content'][0].strip()
    return to_return


def process_annotation(text: str) -> dict:
    key, value = text.strip("{").strip("}").split(":")
    return {key: value}


def process_tag(text: str) -> str:
    tag = text.strip('#').replace('_', ' ')
    return tag


def process_text(text: str) -> str:
    return text


process = {
    "text": process_text,
    "tag": process_tag,
    "annotation": process_annotation,
}


def parse_annotated_text(text: str) -> Dict[str, list]:
    annotation = tokenize(text)
    to_return = defaultdict(list)
    for key in annotation:
        for value in annotation[key]:
            to_return[key].append(process[key](value))
    return to_return
