from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def calculate_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def handle_not_moving(current_position: Position, board_width: int, board_height: int) -> tuple[int, int]:
        if current_position.x == 0:
            if current_position.y == 0:
                return 1, 0
            elif current_position.y == board_height - 1:
                return 0, -1
            else:
                return 0, -1 
        elif current_position.x == board_width - 1:
            if current_position.y == 0:
                return 0, 1
            elif current_position.y == board_height - 1:
                return -1, 0
            else:
                return 0, 1
        elif current_position.y == 0:
            return 1, 0
        elif current_position.y == board_height - 1:
            return -1, 0
        else:
            return 1, 0

def is_teleporting_closer(bot_position: Position, target_position: Position, teleporter_pairs: list[tuple[Position, Position]]) -> tuple[bool, Optional[Position]]:
        direct_distance = calculate_distance(bot_position.x, bot_position.y, target_position.x, target_position.y)

        for teleporter_pair in teleporter_pairs:
            teleporter1, teleporter2 = teleporter_pair
            distance_via_teleporter_1 = calculate_distance(bot_position.x, bot_position.y, teleporter1.x, teleporter1.y) + calculate_distance(teleporter2.x, teleporter2.y, target_position.x, target_position.y)
            distance_via_teleporter_2 = calculate_distance(bot_position.x, bot_position.y, teleporter2.x, teleporter2.y) + calculate_distance(teleporter1.x, teleporter1.y, target_position.x, target_position.y)

            if distance_via_teleporter_1 < direct_distance:
                return True, teleporter1
            elif distance_via_teleporter_2 < direct_distance:
                return True, teleporter2

        return False, None

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

        teleporter = [x for x in board.game_objects if x.type == "TeleportGameObject"]
        teleporter_pairs = []
        paired_ids = []
        for teleport in teleporter:
            if teleport.properties.pair_id not in paired_ids:
                pair = next((x for x in teleporter if x.properties.pair_id == teleport.properties.pair_id and x != teleport), None)
                if pair:
                    teleporter_pairs.append((teleport.position, pair.position))
                    paired_ids.append(teleport.properties.pair_id)

        if props.diamonds >= 4:
            self.goal_position = base
            is_closer, teleporter_to_use = is_teleporting_closer(board_bot.position, self.goal_position, teleporter_pairs)
            if is_closer:
                self.goal_position = teleporter_to_use
            
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

            if delta_x == 0 and delta_y == 0 :
                delta_x, delta_y = handle_not_moving(current_position, board.width, board.height)
            return delta_x, delta_y
        
        if len(self.selected_checkpoints) > 1:
            if calculate_distance(current_position.x, current_position.y,self.selected_checkpoints[0][1].x,self.selected_checkpoints[0][1].y) > 10 and props.diamonds > 2:
                self.goal_position = base
            
                is_closer, teleporter_to_use = is_teleporting_closer(board_bot.position, self.goal_position, teleporter_pairs)
                if is_closer:
                    self.goal_position = teleporter_to_use
                
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
                if delta_x == 0 and delta_y == 0 :
                    delta_x, delta_y = handle_not_moving(current_position, board.width, board.height)
                return delta_x, delta_y

        objects = []
        for obj in boardGame:
            if obj.type=="DiamondGameObject" or obj.type == "DiamondButtonGameObject":
                objects.append(obj.position)

        distances = []
        for obj in objects:
            distance = calculate_distance(current_position.x, current_position.y, obj.x, obj.y)
            distances.append((distance, obj))

        distances.sort(key=lambda x: x[0])

        self.goal_position = distances[0][1]

        uToBase = calculate_distance(current_position.x, current_position.y, base.x, base.y)
        baseToTarget = calculate_distance(self.goal_position.x, self.goal_position.y, base.x, base.y)
        uTotarget  = calculate_distance(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        # check jika plg ke base searah
        if (props.diamonds > 0 and (uToBase + baseToTarget - uTotarget) <= 2):
            self.goal_position = base

        if (board_bot.properties.milliseconds_left < (baseToTarget + 1.3) * (1000)) and (props.diamonds >= 1):
            self.goal_position = base

        is_closer, teleporter_to_use = is_teleporting_closer(board_bot.position, self.goal_position, teleporter_pairs)
        if is_closer:
            self.goal_position = teleporter_to_use
        
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        if delta_x == 0 and delta_y == 0 :
                delta_x, delta_y = handle_not_moving(current_position, board.width, board.height)
        return delta_x, delta_y