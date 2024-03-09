from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position, Base
from ..util import get_direction, position_equals, clamp

from typing import Optional, List


class ShortestToBotV2Logic(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        # self.goal_obj: Optional[GameObject] = None
        
    def get_direction_y(self,current_x, current_y, dest_x, dest_y):
        delta_x = clamp(dest_x - current_x, -1, 1)
        delta_y = clamp(dest_y - current_y, -1, 1)
        if delta_y != 0:
            delta_x = 0
        return (delta_x, delta_y)
    
    def calcRange(self, pos_from, pos_to, teleporter1, teleporter2, range_before):
        range_tel_1 =  abs(teleporter1.x - pos_from.x) + abs(teleporter1.y - pos_from.y)
        range_tel_2 =  abs(teleporter2.x - pos_to.x) + abs(teleporter2.y - pos_to.y)
        tot_range_1 = range_tel_1 + range_tel_2
        range_tel_2 =  abs(teleporter2.x - pos_from.x) + abs(teleporter2.y - pos_from.y)
        range_tel_1 =  abs(teleporter1.x - pos_to.x) + abs(teleporter1.y - pos_to.y)
        tot_range_2 = range_tel_1 + range_tel_2
        
        if (tot_range_1 < tot_range_2):
            if (tot_range_1 < range_before):
                    range = tot_range_1
                    teleporter_from = teleporter1
                    teleporter_to = teleporter2
            else:
                if (tot_range_2 < range_before):
                    range = tot_range_2
                    teleporter_from = teleporter2
                    teleporter_to = teleporter1 
        
        return (range, teleporter_from, teleporter_to)
    
    def isTimeEnough(self, time_left, range_to, range_back):
        return time_left < (range_to + range_back + 1.3) * (1000)

    def next_move(self, board_bot: GameObject, board: Board):
        try:
            
            current_position: Position = board_bot.position

            teleporters_arr: List[GameObject] = []
            teleporters = {}

            #Menyimpan data semua teleporter
            for ob in board.game_objects:
                if (ob.type == "TeleportGameObject"):
                    if teleporters.get(ob.properties.pair_id) == None:
                        teleporters[ob.properties.pair_id] = [ob] 
                    else :
                        teleporters[ob.properties.pair_id].append(ob) 

                    teleporters_arr.append(ob) 
                    
            base: Base = board_bot.properties.base
            goal_position_base = base
            range_base = abs(base.x - current_position.x) + abs(base.y - current_position.y)
            for teleporter_id in  teleporters.keys():
                [teleporter1, teleporter2] = teleporters[teleporter_id]
                range_tel_1 =  abs(teleporter1.position.x - current_position.x) + abs(teleporter1.position.y - current_position.y)
                range_tel_2 =  abs(teleporter2.position.x - base.x) + abs(teleporter2.position.y - base.y)
                tot_range_1 = range_tel_1 + range_tel_2
                range_tel_2 =  abs(teleporter2.position.x - current_position.x) + abs(teleporter2.position.y - current_position.y)
                range_tel_1 =  abs(teleporter1.position.x - base.x) + abs(teleporter1.position.y - base.y)
                tot_range_2 = range_tel_1 + range_tel_2
                if (tot_range_1 < tot_range_2):
                    if (tot_range_1 < range_base):
                        goal_position_base = teleporter1.position
                        range_base = tot_range_1
                else:
                    if (tot_range_2 < range_base):   
                        goal_position_base = teleporter2.position
                        range_base = tot_range_2

                
            #Kembali ke base jika sudah membawa banyak diamand yang diinginkan
            if board_bot.properties.diamonds >= board_bot.properties.inventory_size:
                self.goal_position = goal_position_base;
                
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )


                if board.is_valid_move(current_position, delta_x, delta_y):
                    return delta_x, delta_y
                else:
                    raise Exception("invalid move")       
            #Mencari diamond atau red button terdekat dari bot
            else:
                
                #Menghitung jarak dari bot ke objek tujuan dengan melibatkan teleporter
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
                        
                #Diamond terakhir yang akan dibawa akan dicari berdasarkan total jarak 
                #dari bot ke diamond + jarak dari diamond ke base yang terpendek 
                if (board_bot.properties.inventory_size - board_bot.properties.diamonds == 1):
                    diamonds.sort(key=lambda x: x[1] + x[4], reverse=True)
                else:
                    diamonds.sort(key=lambda x: x[1], reverse=True)
                
                diamonds_temp = diamonds.copy() 
                
                
                #Diamond yang diambil sebisa mungkin berada dekat dengan base yaitu <= 8 langkah dari base
                #Jika tidak ada diamond yang dekat dengan base maka akan diperbolehkan mencari yang jauh dari base
                diamonds = list(filter(lambda x: x[4] <= 8, diamonds))
                
                if (len(diamonds) == 0):
                    diamonds = diamonds_temp.copy()
                
                diamond = diamonds.pop()
                
                is_back = False;
                
                #Kembali ke base jika sisa diamond 1 dan di dekat bot hanya ada diamond merah
                #Kembali ke base jika inventory >= 3 dan jarak ke base lebih dekat dari jarak diamond terdekat
                if (board_bot.properties.diamonds == board_bot.properties.inventory_size - 1 and diamond[0].properties.points == 2) or (board_bot.properties.diamonds >= 3 and range_base < diamond[1]):
                    # print("seleksi ")
                    is_back = True
                else:
                    is_back = False
                            
                        
                #Mengecek apakah waktu yang tersisa cukup untuk mengambil diamond lagi atau tidak
                if not is_back:
                    if (board_bot.properties.milliseconds_left < (diamond[1] + diamond[4] + 1.3) * (1000)) and (board_bot.properties.diamonds >= 1):
                        # print("waktu")
                        is_back = True

                    else:
                        is_back = False
                        
            if is_back:
                # print("back")
                self.goal_position = goal_position_base
            else:
                if (diamond[2] != None and diamond[3] != None):
                    self.goal_position = diamond[2].position
                else:
                    self.goal_position = diamond[0].position

            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

           
            if board.is_valid_move(current_position, delta_x, delta_y):
                return delta_x, delta_y
            else:
                raise Exception("invalid move")
        except:
            if board_bot.position.x == 0:
                return 1, 0
            else:
                return -1,0
            