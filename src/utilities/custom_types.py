from typing import Optional
from pydantic import BaseModel


from dataclasses import dataclass
from typing import List

@dataclass
class Meta:
    id: str
    uuid: str
    sort: int
    src: str
    section: str
    stems: List[str]
    offensive: bool

@dataclass
class Hwi:
    hw: str

@dataclass
class Definition:
    text: str

@dataclass
class DictionaryResponse:
    meta: Meta
    hwi: Hwi
    fl: str
    shortdef: List[str]
    date: str
    definitions: List[Definition]



class WordObj(BaseModel):
    word: str
    points: int = 0
    isogram: Optional[bool] = False
    definition: Optional[list[str]] = None

class DayModel(BaseModel):
    daylist_id: str
    centerLetter: str;
    isograms: list[WordObj];
    total_points: int;
    letters: list[str];
    validWords: list[WordObj];