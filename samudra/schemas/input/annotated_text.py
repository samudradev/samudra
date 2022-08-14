import re
from collections import defaultdict
from typing import List, Dict, Optional, Union

import pydantic as pyd

from samudra.schemas.input.accepted_fields import AcceptedFields

EXPECTED_FIELDS = ["meta", "lang"]
EXPECTED_SECOND_FIELDS = ["gol", "en"]

REGEX_PATTERN = r"""(?xm)
    (?P<field>      {[_a-zA-Z]{,4}\.[_a-zA-Z]{,3}:\w+}) |
    (?P<tag>        \#[_a-zA-Z0-9\-.]+ ) |
    (               \s{1}) |
    (?P<content>    [\w\d\s,.?!$`_*/&~\\\+\-%()=]+) |
    """


class AnnotatedText(pyd.BaseModel):
    """Uses regex to annotate text

    Example body:
        "This is a string #tag_1 #tag-2 {lang.en:new} {meta.gol:nama}"
    """

    body: str

    @property
    def _tokens(self) -> Dict[str, Union[list, str]]:
        to_return = defaultdict(list)
        for match in re.finditer(REGEX_PATTERN, self.body):
            if match.lastgroup:
                to_return[match.lastgroup].append(match[0])
        if len(to_return["content"]) > 1:
            raise SyntaxError(
                {
                    "message": "Returns {} texts. Expects 1. Unexpected character(s) causes the text to be parsed incorrectly.".format(
                        len(to_return)
                    ),
                    "content": "<?> ".join(to_return["content"]),
                    "body": self.body,
                    "tags": to_return.get("tag"),
                    "fields": to_return.get("field"),
                }
            )
        to_return["content"]: str = to_return["content"][0].strip()
        return to_return

    @property
    def fields(self) -> dict:
        to_eval: Optional[str] = self._tokens.get("field", None)
        to_return = defaultdict(dict)
        for eval_str in to_eval:
            key, value = eval_str.strip("{").strip("}").split(":")
            key_1, key_2 = key.split(".")
            if key_1 not in AcceptedFields.__members__:
                raise SyntaxError(
                    f"Field '{key_1}' not expected. Only {AcceptedFields.__members__} are expected."
                )
            elif key_2 not in AcceptedFields[key_1].value:
                raise SyntaxError(
                    f"Field '{key_2}' not expected. Only {AcceptedFields[key_1].value} are expected."
                )
            if AcceptedFields[key_1] is AcceptedFields.lang:
                if to_return[AcceptedFields.lang.name].get(key_2):
                    to_return[AcceptedFields.lang.name][key_2].append(value)
                else:
                    to_return[AcceptedFields.lang.name] = {key_2: [value]}
            elif key_2 == "gol":
                to_return[key_1] = {key_2: value}
            else:
                to_return[key_1] = {key_2: [value]}
        return to_return

    @property
    def tags(self) -> List[str]:
        to_return = list()
        for tag in self._tokens.get("tag", []):
            to_return.append(tag.strip("#").replace("_", " "))
        return to_return

    @property
    def content(self) -> str:
        return self._tokens["content"]
