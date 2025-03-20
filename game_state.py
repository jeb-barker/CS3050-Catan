from enum import Enum

class TurnState(Enum):
    BEFORE_ROLL = "before_roll"
    AFTER_ROLL = "after_roll"
    BUILDING = "building"
    END_TURN = "end_turn"