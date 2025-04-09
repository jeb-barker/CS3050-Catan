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
        self.tags = {'city': False,
                     'settlement': False,
                     'road': False,
                     'road_v1': None}
        self.is_start = True

    def get_current_player(self):
        """Returns the player whose turn it is."""
        return self.players[self.current_player_index]

    def roll_dice(self):
        """Transition from BEFORE_ROLL to AFTER_ROLL."""
        if self.state == TurnState.BEFORE_ROLL:
            self.state = TurnState.AFTER_ROLL
            return True
        return False

    def start_building_phase(self):
        """Transition from AFTER_ROLL to BUILDING."""
        if self.state == TurnState.AFTER_ROLL:
            self.state = TurnState.BUILDING
            return True
        return False

    def end_turn(self):
        """End the turn and move to the next player."""
        if self.state == TurnState.BUILDING:
            self.next_turn()
            return True
        return False

    def next_turn(self):
        """Cycle to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.state = TurnState.BEFORE_ROLL

    def is_build_allowed(self):
        """returns truthy if current player can build a settlement or city right now"""
        if self.state is TurnState.BUILDING:
            return True
        return False
    
    def is_start_phase(self):
        """returns truthy if the game is in the setup/start phase"""
        return self.is_start
    
    def end_start_phase(self):
        """transition from the start phase to the main game loop"""
        self.is_start = False

    def get_ui_state(self):
        """Returns which buttons should be active."""
        return {
            "roll_dice": self.state == TurnState.BEFORE_ROLL,
            "build": self.state == TurnState.AFTER_ROLL,
            "end_turn": self.state == TurnState.BUILDING
        }
