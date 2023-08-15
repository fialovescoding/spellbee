from __future__ import annotations
from pydantic import BaseModel as PydanticBaseModel
from enum import Enum
from pydantic import Field, validator
from typing import List, Optional, Dict, Any

class WordType(Enum):
    NEW = 0
    RETEST = 1
    INCORRECT = 2
    CORRECT = 3

class Word(PydanticBaseModel):
    data: str
    student_id: str
    last_seen: Optional[int] = None
    type: WordType
