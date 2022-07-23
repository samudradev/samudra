from collections import defaultdict
from typing import List, Dict, Optional, Any

import pydantic as pyd

from samudra.tools.tokenizer import tokenize


class AnnotatedText(pyd.BaseModel):
    """Uses regex to annotate text

    Example body:
        "This is a string #tag_1 #tag-2 {lang.en:new} {meta.gol:nama}"
    """
    body: str

    @property
    def tokenized(self) -> Dict[str, list]:
        return tokenize(self.body)

    @property
    def fields(self) -> dict:
        to_eval: Optional[str] = self.tokenized.get('field', None)
        to_return = defaultdict(dict)
        for eval_str in to_eval:
            key, value = eval_str.strip('{').strip('}').split(':')
            key_1, key_2 = key.split('.')
            if to_return[key_1].get(key_2):
                to_return[key_1][key_2].append(value)
            elif key_2 == 'gol':
                to_return[key_1] = {key_2: value}
            else:
                to_return[key_1] = {key_2: [value]}
        return to_return

    @property
    def tags(self) -> List[str]:
        to_return = list()
        for tag in self.tokenized.get('tag', []):
            to_return.append(tag.strip('#').replace('_', ' '))
        return to_return

    @property
    def content(self) -> str:
        return self.tokenized['content']
