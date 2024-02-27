import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def calculate_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

class EnriqueLogic(BaseLogic):

    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.selected_checkpoints =[]



    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        base = props.base
        boardGame = board.game_objects
        current_position = board_bot.position   

        distances = []

        
        if props.diamonds > 3:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                base.x,
                base.y,
            )
            return delta_x, delta_y
        elif  len(self.selected_checkpoints) > 1:
            if calculate_distance(current_position.x, current_position.y,self.selected_checkpoints[0][1]['x'],self.selected_checkpoints[0][1]['y']) > 10 and props.diamonds > 2:
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    base.x,
                    base.y,
                )

        objects = []

        for obj in boardGame:
            if obj.type=="DiamondGameObject" or obj.type == "DiamondButtonGameObject":
                objects.append({'x':obj.position.x, 'y':obj.position.y})


        for obj in objects:
            distance = calculate_distance(current_position.x, current_position.y, obj["x"], obj["y"])
            distances.append((distance, obj))

        distances.sort(key=lambda x: x[0])
        
        self.selected_checkpoints = distances[:3]
    
        print(self.selected_checkpoints)
        print(current_position)
        
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.selected_checkpoints[0][1]['x'],
            self.selected_checkpoints[0][1]['y'],
        )
        self.selected_checkpoints.pop(0)
        print(delta_x, delta_y)

        
        return delta_x, delta_y
