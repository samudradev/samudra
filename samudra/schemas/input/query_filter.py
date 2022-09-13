from typing import List, Optional

import pydantic as pyd


class QueryFilter(pyd.BaseModel):
    limit: Optional[int]
    cakupan: Optional[List[str]]
    kata_asing: Optional[List[str]]
