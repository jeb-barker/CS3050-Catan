"""Classes pertaining to managing what state the game is in."""
from enum import Enum

class TurnState(Enum):
    """Represents which phase of the turn the GameState is currently in"""
    BEFORE_ROLL = "before_roll"
    AFTER_ROLL = "after_roll"
    BUILDING = "building"
    END_TURN = "end_turn"

class GameState:
    """Represents what state the game is currently in."""
    def __init__(self, players):
        self.players = players
        self.current_player_index = 0
        self.state = TurnState.BUILDING
        self.tags = {'city': False,
                     'settlement': False,
                     'road': False,
                     'road_v1': None,
                     'settlements_placed_turn': 0,
                     'settlements_placed': 0,
                     'settlement_pos': -1}
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

    def end_turn_start_phase(self):
        """End a turn in the start phase.
        Ends the start phase if every player has played 2 settlements.
        Players take turns clockwise, then counterclockwise.
        returns True if this was the player's second settlement"""
        # reset tags
        self.tags['settlements_placed_turn'] = 0
        # if the number of settlements placed is 2 per player, end the start phase.
        if self.tags['settlements_placed'] == 2 * len(self.players):
            self.is_start = False
            self.state = TurnState.BEFORE_ROLL
            return True
        # if the settlements placed is more than the number of players return True
        if self.tags['settlements_placed'] > len(self.players):
            # move the turn counter backwards if this is the second time around
            self.current_player_index = (self.current_player_index - 1) % len(self.players)
            return True
        # move the turn counter forwards if this is the first time around
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
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
