from typing import Optional, Literal
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import clamp

#Filer
class NoLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.attack_other_bots = False
        self.time_based_retreat = True

    def next_move(self, board_bot: GameObject, board: Board):
        return 0,0