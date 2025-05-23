from typing import Optional
from pydantic import BaseModel




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