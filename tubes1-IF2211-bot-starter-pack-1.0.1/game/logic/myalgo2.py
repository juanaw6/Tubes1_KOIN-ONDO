from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position, Base
from ..util import get_direction, position_equals

import random
from typing import Optional, List
import time

#DiamondGameObject
#DiamondButtonGameObject
#BotGameObject
#TeleportGameObject
#BaseGameObject
class MyAlgo2(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.goal_obj: Optional[GameObject] = None
        self.is_use_teleporter: bool = False
        self.time_reset_teleporter: Optional[int] = None
        # self.second_goal_position: Optional[Position] = None

    def next_move(self, board_bot: GameObject, board: Board):
        # try:
            # start_time = time.time()
            current_position: Position = board_bot.position
            
            

            # if (self.time_reset_teleporter == None):
            #     [feature] = [d for d in board.features if d.name == "TeleportRelocationProvider"]
            #     self.time_reset_teleporter = feature.config.seconds

            teleporters_arr: List[GameObject] = []
            teleporters = {}


            for ob in board.game_objects:
                if (ob.type == "TeleportGameObject"):
                    if teleporters.get(ob.properties.pair_id) == None:
                        teleporters[ob.properties.pair_id] = [ob] 
                    else :
                        teleporters[ob.properties.pair_id].append(ob) 

                    teleporters_arr.append(ob) 
                    
            is_change = True
                    
            if (self.goal_position != None):
                for ob in board.game_objects:
                    if (position_equals(ob.position, self.goal_position)):
                        if self.goal_obj == None:
                            if ob.type == "BaseGameObject" and ob.properties.name == board_bot.properties.name:
                                is_change = False
                        else:
                            if ob.type == self.goal_obj.type and ob.id == self.goal_obj.id:
                                is_change = False
            
            if is_change:
                self.goal_position = None
                self.goal_obj = None
                

            
            if (self.goal_position != None):
                if (position_equals(self.goal_position, current_position)):
                    if self.goal_obj != None and self.goal_obj.type == "TeleportGameObject":
                        [teleporter1, teleporter2] = teleporters[self.goal_obj.properties.pair_id]
                        if (position_equals(self.goal_obj.position, teleporter1.position)) and (position_equals(current_position, teleporter2.position)):
                            self.goal_position = None
                            self.goal_obj = None
                        elif (position_equals(self.goal_obj.position, teleporter2.position)) and (position_equals(current_position, teleporter1.position)):
                            self.goal_position = None
                            self.goal_obj = None
                    else:    
                        self.goal_position = None
                        self.goal_obj = None

            if self.goal_position:
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
            else:
                
                if board_bot.properties.diamonds >= board_bot.properties.inventory_size:
                    base: Base = board_bot.properties.base
                    self.goal_position = base
                    self.goal_obj = None
                    self.is_use_teleporter = True
                    range = abs(base.x - current_position.x) + abs(base.y - current_position.y)

                    teleporter_from = None
                    teleporter_to = None
                    for teleporter_id in  teleporters.keys():
                        [teleporter1, teleporter2] = teleporters[teleporter_id]
                        range_tel_1 =  abs(teleporter1.position.x - current_position.x) + abs(teleporter1.position.y - current_position.y)
                        range_tel_2 =  abs(teleporter2.position.x - base.x) + abs(teleporter2.position.y - base.y)
                        tot_range_1 = range_tel_1 + range_tel_2

                        range_tel_2 =  abs(teleporter2.position.x - current_position.x) + abs(teleporter2.position.y - current_position.y)
                        range_tel_1 =  abs(teleporter1.position.x - base.x) + abs(teleporter1.position.y - base.y)
                        tot_range_2 = range_tel_1 + range_tel_2

                        if (tot_range_1 < tot_range_2):
                            if (tot_range_1 < range):
                                self.goal_position = teleporter1.position
                                self.goal_obj = teleporter1
                                self.is_use_teleporter = True
                        else:
                            if (tot_range_2 < range):   
                                self.goal_position = teleporter2.position
                                self.goal_obj = teleporter2
                                self.is_use_teleporter = True
                else: 

                    diamonds: List[GameObject] = []

                    for ob in board.game_objects:
                        if (ob.type == "DiamondGameObject" or ob.type == "DiamondButtonGameObject"):
                            range = abs(ob.position.x - current_position.x) + abs(ob.position.y - current_position.y)
                            range_to_base = abs(ob.position.x - board_bot.properties.base.x) + abs(ob.position.y - board_bot.properties.base.y)
                            teleporter_from = None
                            teleporter_from_2 = None                            
                            teleporter_to = None
                            for teleporter_id in  teleporters.keys():
                                [teleporter1, teleporter2] = teleporters[teleporter_id]
                                range_tel_1 =  abs(teleporter1.position.x - current_position.x) + abs(teleporter1.position.y - current_position.y)
                                range_tel_2 =  abs(teleporter2.position.x - ob.position.x) + abs(teleporter2.position.y - ob.position.y)
                                tot_range_1 = range_tel_1 + range_tel_2

                                range_tel_2 =  abs(teleporter2.position.x - current_position.x) + abs(teleporter2.position.y - current_position.y)
                                range_tel_1 =  abs(teleporter1.position.x - ob.position.x) + abs(teleporter1.position.y - ob.position.y)
                                tot_range_2 = range_tel_1 + range_tel_2

                                if (tot_range_1 < tot_range_2):
                                    if (tot_range_1 < range):
                                        range = tot_range_1
                                        teleporter_from = teleporter1
                                        teleporter_to = teleporter2
                                else:
                                    if (tot_range_2 < range):   
                                        range = tot_range_2
                                        teleporter_from = teleporter2
                                        teleporter_to = teleporter1
                                        
                                range_tel_1 =  abs(teleporter1.position.x - board_bot.properties.base.x) + abs(teleporter1.position.y - board_bot.properties.base.y)
                                range_tel_2 =  abs(teleporter2.position.x - ob.position.x) + abs(teleporter2.position.y - ob.position.y)
                                tot_range_1 = range_tel_1 + range_tel_2
                                range_tel_2 =  abs(teleporter2.position.x - board_bot.properties.base.x) + abs(teleporter2.position.y - board_bot.properties.base.y)
                                range_tel_1 =  abs(teleporter1.position.x - ob.position.x) + abs(teleporter1.position.y - ob.position.y)
                                tot_range_2 = range_tel_1 + range_tel_2
                                if (tot_range_1 < tot_range_2):
                                    if (tot_range_1 < range_to_base):
                                        range_to_base = tot_range_1
                                        teleporter_from_2 = teleporter1
                                else:
                                    if (tot_range_2 < range_to_base):   
                                        range_to_base = tot_range_2
                                        teleporter_from_2 = teleporter2

                                diamonds.append((ob, range, teleporter_from, teleporter_to, range_to_base, teleporter_from_2))  


                    diamonds.sort(key=lambda x: x[1], reverse=True)  

                    diamond = diamonds.pop()

                    if (board_bot.properties.inventory_size - board_bot.properties.diamonds <= 1):
                        if (diamond[0].properties.points == 2):
                            diamond = diamonds.pop()


                    if (board_bot.properties.milliseconds_left < (diamond[1] + diamond[4] + 1.2) * 1000) and (board_bot.properties.diamonds >= 1):
                        self.goal_obj = None
                        if diamond[5] != None:
                            self.goal_position = diamond[5].position
                            self.is_use_teleporter = True

                        else:
                            self.goal_position = board_bot.properties.base
                            self.is_use_teleporter = False

                        delta_x, delta_y = get_direction(
                            current_position.x,
                            current_position.y,
                            self.goal_position.x,
                            self.goal_position.y,
                        )
                            # end_time = time.time()
                            # print(end_time-start_time)
                    else:
                        if (diamond[2] != None and diamond[3] != None):
                            self.goal_position = diamond[2].position
                            self.goal_obj = diamond[2]
                            self.is_use_teleporter = True
                        else:
                            self.goal_position = diamond[0].position
                            self.goal_obj = diamond[0]
                            self.is_use_teleporter = False

                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )

            if (self.is_use_teleporter == False):
                next_x = delta_x + current_position.x
                next_y = delta_y + current_position.y
                filtered_teleporter = list(filter(lambda a: a.position.x == next_x and a.position.y == next_y, teleporters_arr))

                if (len(filtered_teleporter) > 0):
                    if (delta_x != 0):
                        if current_position.y == 0:
                            delta_x = 0
                            delta_y = 1
                        else:
                            delta_x = 0
                            delta_y = -1
                    elif (delta_y != 0):
                        if current_position.x == 0:
                            delta_y = 0
                            delta_x = 1
                        else:
                            delta_y = 0
                            delta_x = -1

            # end_time = time.time()
            # print(end_time-start_time)

            return delta_x, delta_y
        # except:
        #     if board_bot.position.x == 0:
        #         return 1, 0
        #     else:
        #         return -1,0
            