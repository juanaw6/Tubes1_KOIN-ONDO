from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

import random
from typing import Optional

#DiamondGameObject
#DiamondButtonGameObject
#BotGameObject
#TeleportGameObject
#BaseGameObject
class MyAlgo(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        
        

    def next_move(self, board_bot: GameObject, board: Board):
        # props = board_bot.properties
        # print(board_bot)
        # print(list(map(lambda x: x.type, board.game_objects)))
        # print(list(map(lambda x: x.properties.points, board.game_objects)))
        # Analyze new state
        if board_bot.properties.diamonds == board_bot.properties.inventory_size:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = None

        current_position = board_bot.position
        
        
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            
            diamonds = []
            teleporters = {}
            teleporters_arr = []
        
            for ob in board.game_objects:
                if (ob.type == "DiamondGameObject" or ob.type == "DiamondButtonGameObject"):
                    range = abs(ob.position.x - current_position.x) + abs(ob.position.y - current_position.y)
                    diamonds.append((ob, range))
                
                if (ob.type == "TeleportGameObject"):
                    # print(teleporters.get(ob.properties.pair_id))
                
                    if teleporters.get(ob.properties.pair_id) == None:
                        teleporters[ob.properties.pair_id] = [ob] 
                    else :
                        teleporters[ob.properties.pair_id].append(ob) 
                        
                    teleporters_arr.append(ob)                  

            diamonds.sort(key=lambda x: x[1], reverse=True)  
            
            # print(diamonds)  

            diamond = diamonds.pop()
            
            if (board_bot.properties.inventory_size - board_bot.properties.diamonds <= 1):
                if (diamond.properties.points == 2):
                    diamond = diamonds.pop()

            self.goal_position = diamond[0].position
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
            
        next_x = delta_x + current_position.x
        next_y = delta_y + current_position.y
        filtered_teleporter = list(filter(lambda a: a.position.x == next_x and a.position.y == next_y, teleporters_arr))
        
        if (len(filtered_teleporter) > 0):
            if (delta_x != 0):
                if current_position.x == 0:
                    delta_x = 0
                    delta_y = -1
                else:
                    delta_x = 0
                    delta_y = 1
            elif (delta_y != 0):
                if current_position.y == 0:
                    delta_y = 0
                    delta_x = -1
                else:
                    delta_y = 0
                    delta_x = 1

        
        return delta_x, delta_y