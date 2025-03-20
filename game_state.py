from enum import Enum

class TurnState(Enum):
    BEFORE_ROLL = "before_roll"
    AFTER_ROLL = "after_roll"
    BUILDING = "building"
    END_TURN = "end_turn"

class GameState:
    def __init__(self, players):
        self.players = players
        self.current_player_index = 0
        self.state = TurnState.BEFORE_ROLL