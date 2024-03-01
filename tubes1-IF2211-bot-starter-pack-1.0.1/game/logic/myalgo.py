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
class MyAlgo(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.goal_obj: Optional[GameObject] = None
        self.is_use_teleporter: bool = False
        self.time_reset_teleporter: Optional[int] = None
        self.next_position_dodge: List[Position] = []
        self.is_dodge = False
        # self.around = [(1, 0), (0, 1), (-1, 0), (0, -1), (1,1), (-1, -1), (1, -1), (-1, 1)]
        # self.is_attack_before = False
        # self.second_goal_position: Optional[Position] = None

    def next_move(self, board_bot: GameObject, board: Board):
        try:
            # start_time = time.time()

            # if (self.time_reset_teleporter == None):
            #     [feature] = [d for d in board.features if d.name == "TeleportRelocationProvider"]
            #     self.time_reset_teleporter = feature.config.seconds
            
            current_position: Position = board_bot.position

            teleporters_arr: List[GameObject] = []
            teleporters = {}


            for ob in board.game_objects:
                if (ob.type == "TeleportGameObject"):
                    if teleporters.get(ob.properties.pair_id) == None:
                        teleporters[ob.properties.pair_id] = [ob] 
                    else :
                        teleporters[ob.properties.pair_id].append(ob) 

                    teleporters_arr.append(ob) 
                    
            if self.is_dodge:
                print(self.next_position_dodge)
                if len(self.next_position_dodge) > 0:
                    pos: Position = self.next_position_dodge.pop(0)
                    if board.is_valid_move(current_position, pos.x, pos.y):
                        return pos.x, pos.y  
                    else:
                        raise Exception("invalid move")
                else:
                    self.is_dodge = False
            
            # if board_bot.properties.diamonds != board_bot.properties.inventory_size:
            #     if self.is_attack_before:
            #         self.is_attack_before = False
            #     else:
            #         enemy_bot = None
                    
            #         for s in self.around:
            #             (x, y) = s
            #             plus_x = current_position.x + x
            #             plus_y = current_position.y + y
            #             for ob in board.game_objects:
            #                 if ob.type == "BotGameObject" and position_equals(Position(plus_y, plus_x), ob.position):
            #                     enemy_bot = ob
            #                     break
                            
            #             if (enemy_bot != None):
            #                 break
                    
            #         if (enemy_bot != None):     
            #             enemy_position = enemy_bot.position
            #             delta_x, delta_y = get_direction(
            #                 current_position.x,
            #                 current_position.y,
            #                 enemy_position.x,
            #                 enemy_position.y
            #             )
            #             self.is_attack_before = True
            #             return delta_x, delta_y    
 

            max_inventory_size = board_bot.properties.inventory_size
            
            if board_bot.properties.milliseconds_left < 20:
                max_inventory_size = round(max_inventory_size / 2)
                
            if board_bot.properties.diamonds >= max_inventory_size:
                base: Base = board_bot.properties.base
                self.goal_position = base
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
                        
                diamonds.sort(key=lambda x: x[1] + x[4], reverse=True)  
                diamond = diamonds.pop()
                if (board_bot.properties.inventory_size - board_bot.properties.diamonds <= 1):
                    if (diamond[0].properties.points == 2):
                        diamond = diamonds.pop()
                
                # check = list(filter(lambda x: x[4] < 10, diamonds))
                # if (len(check) > 0):
                #     while diamond[4] > 10:
                #         diamond = diamond.pop()
                        
                # print(diamond)
                if (board_bot.properties.milliseconds_left < (diamond[1] + diamond[4] + 1) * (board.minimum_delay_between_moves * 2)) and (board_bot.properties.diamonds >= 1):
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
                        self.is_use_teleporter = True
                    else:
                        self.goal_position = diamond[0].position
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
                    print("Halo cokkkkkkkkkkkkkkkkkkkkk")
                    self.is_dodge = True
                    if (delta_x != 0):
                        delta_next_x = delta_x
                        
                        if current_position.y == 0:
                            delta_x = 0
                            delta_y = 1
                            
                            self.next_position_dodge.append(Position(0, delta_next_x))
                            self.next_position_dodge.append(Position(0, delta_next_x))
                        else:
                            delta_x = 0
                            delta_y = -1
                            self.next_position_dodge.append(Position(0, delta_next_x))
                            self.next_position_dodge.append(Position(0, delta_next_x))
                    elif (delta_y != 0):
                        delta_next_y = delta_y
                        if current_position.x == 0:
                            delta_y = 0
                            delta_x = 1
                            self.next_position_dodge.append(Position(delta_next_y, 0))
                            self.next_position_dodge.append(Position(delta_next_y, 0))
                        else:
                            delta_y = 0
                            delta_x = -1
                            self.next_position_dodge.append(Position(delta_next_y, 0))
                            self.next_position_dodge.append(Position(delta_next_y, 0))

            # end_time = time.time()
            # print(end_time-start_time)
            if board.is_valid_move(current_position, delta_x, delta_y):
                return delta_x, delta_y
            else:
                raise Exception("invalid move")
        except:
            if board_bot.position.x == 0:
                return 1, 0
            else:
                return -1,0
            