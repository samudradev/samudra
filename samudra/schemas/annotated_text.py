from collections import defaultdict
from typing import List, Dict, Optional, Any

import pydantic as pyd

from samudra.tools.tokenizer import tokenize


class AnnotatedText(pyd.BaseModel):
    body: str

    @property
    def tokenized(self) -> Dict[str, list]:
        return tokenize(self.body)

    @property
    def annotations(self) -> dict:
        to_eval: Optional[str] = self.tokenized.get('annotation', None)
        to_return = defaultdict(dict)
        for eval_str in to_eval:
            key, value = eval_str.strip('{').strip('}').split(':')
            key_1, key_2 = key.split('.')
            to_return[key_1] = {key_2: value}
        return to_return

    @property
    def tags(self) -> List[str]:
        to_return = list()
        for tag in self.tokenized.get('tags', []):
            to_return.append(tag.strip('#').replace('_', ' '))
        return to_return

    @property
    def content(self) -> str:
        return self.tokenized['content']


class AnnotatedTextResponse(pyd.BaseModel):
    body: str
    message: str
    content: str
    annotations: List[Dict[str, Any]]
    tags: List[str]
