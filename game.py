import pygame
import json
import tree
import res

from enum import Enum

from road import Road
from player import Player

from point import Point
from obstacle import obstacle_from_index, obstacle_texture_from_index, get_obstacle_types_count, obstacle_damage_from_index

class State(Enum):
    """ Describes the current state of the game """
    EDITING = 0
    PLAYING = 1
    WINNER = 2
    GAMEOVER = 3

game_state: State = State.EDITING

player_velocity: float = 5
editing_scroll_velocity: float = 0
framerate: int = 30
dialog_timer:int = 0
screen_width: int = 0
screen_height: int = 0
placeholder_texture_index: int = 0
player_sprite = ""

tree = tree.Tree()

focused_obj: Point = None
road: Road = None
player: Player = None

rendering_obstacle_list = []

# ------------------------------------------------
# State change funcs
# ------------------------------------------------

def goto_edit():
    """ Change game to edit mode """
    global game_state, dialog_timer
    # --- Global decl end ---
    road.offset = 0
    dialog_timer = 0
    game_state = State.EDITING

def goto_play():
    """ Change game to play mode """
    global game_state, dialog_timer
    # --- Global decl end ---
    player.HP = player.max_HP
    road.offset = -100
    dialog_timer = 0
    game_state = State.PLAYING

def goto_win():
    """ Change game to win screen """
    global game_state, dialog_timer
    # --- Global decl end ---
    dialog_timer = 0
    game_state = State.WINNER

def goto_to_the_graveyard():
    """ Change game to death screen """
    global game_state, dialog_timer
    # --- Global decl end ---
    dialog_timer = 0
    game_state = State.GAMEOVER

# ------------------------------------------------
# Init funcs
# ------------------------------------------------

def init(SCREEN_WIDTH: int, SCREEN_HEIGHT: int):
    """ Initialize the game's general variables """
    global road, player, screen_width, screen_height
    # --- Global decl end ---
    road = Road(screen_width=SCREEN_WIDTH, length=5)
    player = Player(road=road)
    road.rect.y = (SCREEN_HEIGHT - road.rect.h) / 2
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT
    load_json()

# ------------------------------------------------
# Main loop funcs
# ------------------------------------------------

def event_update(event: pygame.event.Event):
    """ Updates the game's logic for pygame events """
    global placeholder_texture_index
    # --- Global decl end ---
    if game_state == State.EDITING:
        if event.type == pygame.MOUSEWHEEL:
            placeholder_texture_index += 1
            placeholder_texture_index %= get_obstacle_types_count()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                goto_play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and focused_obj is None:
                pos = list(pygame.mouse.get_pos())
                pos[0] += road.offset
                obj = obstacle_from_index(placeholder_texture_index, pos[0], pos[1])
                tree.add(obj.as_point())
            elif event.button == 2:
                placeholder_texture_index += 1
                placeholder_texture_index %= get_obstacle_types_count()
            elif event.button == 3:
                if focused_obj:
                    tree.delete(focused_obj)
    elif game_state == State.PLAYING:
        if event.type == pygame.KEYDOWN:
            # Check for specific key presses
            if event.key == pygame.K_UP:
                player.lane_up()
            if event.key == pygame.K_DOWN:
                player.lane_down()
            if event.key == pygame.K_SPACE or event.key == pygame.K_c or event.key == pygame.K_x:
                player.jump()
            if event.key == pygame.K_e:
                goto_edit()
    elif game_state == State.WINNER or game_state == State.GAMEOVER:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                goto_edit()

def get_visible_obstacle_limits():
    """ Get the visible obstacles edge nodes """
    def compare(x, y):
        if x == y:
            return 0
        elif x > y:
            return 1
        return -1
    
    low_limit = tree.search_closer(None, lambda obj: compare(0, obj.obstacle.rect.right - road.offset))[0]
    high_limit = tree.search_closer(None, lambda obj: compare(screen_width, obj.obstacle.rect.x - road.offset))[0]

    return (low_limit, high_limit)

def load_visible_obstacles():
    """ Loads the visible obstacles into the rendering list """
    global rendering_obstacle_list
    # --- Global decl end ---
    low_limit, high_limit = get_visible_obstacle_limits()
    rendering_obstacle_list = []

    # print(low_limit.value, high_limit.value)
    while low_limit != None:
        rendering_obstacle_list.append(low_limit.value)
        if low_limit.value == high_limit.value or low_limit.value > high_limit.value:
            break
        low_limit = low_limit.next()

def update():
    """ Updates the main game's logic """
    global rendering_obstacle_list, editing_scroll_velocity
    # --- Global decl end ---
    load_visible_obstacles()

    keys = pygame.key.get_pressed()
    if game_state == State.EDITING:
        sub_vel = 0
        if keys[pygame.K_LEFT] and road.offset > 0:
            sub_vel = -3
        if keys[pygame.K_RIGHT] and road.offset < road.get_size() - screen_width:
            sub_vel = 3
        editing_scroll_velocity = (editing_scroll_velocity + player_velocity * sub_vel) / 2
        road.offset += editing_scroll_velocity
    road.update()
    player.update()
    if game_state == State.PLAYING:
        if (road.completeness >= 100):
            goto_win()
        elif player.HP <= 0:
            goto_to_the_graveyard()
        else:
            if not player.jumping:
                for object in rendering_obstacle_list:
                    object_rect = object.obstacle.rect
                    padding = object.obstacle.hitbox_padding
                    rect = pygame.Rect(object_rect.x - road.offset + padding[0], object_rect.y + padding[2], object_rect.w - padding[0] - padding[1], object_rect.h - padding[2] - padding[3])
                    if point_inside_rect(player.rect.centerx, player.rect.bottom - 4, rect):
                        player.damage(obstacle_damage_from_index(object.obstacle.type))

def post_update():
    """ Update the game's logic for the frme end """
    global dialog_timer
    # --- Global decl end ---
    if game_state == State.PLAYING:
        road.offset += player_velocity
    elif game_state == State.WINNER or game_state == State.GAMEOVER:
        dialog_timer += 2

def draw(surface: pygame.Surface):
    """ Draws the game content to a surface """
    global focused_obj, rendering_obstacle_list
    # --- Global decl end ---
    surface.blit(res.Image.BG.value, (0,24))
    road.draw(surface)

    if game_state == State.EDITING and focused_obj is None:
        surface.blit(obstacle_texture_from_index(placeholder_texture_index), pygame.mouse.get_pos())

    focused_obj = None

    for object in rendering_obstacle_list:
        rect = pygame.Rect(object.obstacle.rect.x - road.offset, object.obstacle.rect.y, object.obstacle.rect.w, object.obstacle.rect.h)
        if game_state == State.EDITING and point_inside_rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], rect):
            focused_obj = object
            pygame.draw.rect(surface, "white", rect)
        surface.blit(object.obstacle.image, rect)
    
    player.draw(surface)
    road_below_y = 0
    surface.blit(res.Font.NJ.value.render(f"HP {player.HP} <{road.completeness}x>", False, (143, 98, 51)), (2, road_below_y))
    dialog_aperture = min(24, dialog_timer)
    pygame.draw.rect(surface, (56, 0, 15), (0, screen_height / 2 - dialog_aperture, screen_width, dialog_aperture * 2))
    if dialog_aperture == 24:
        if game_state == State.WINNER:
            surface.blit(res.Image.WIN.value, (0, screen_height / 2 - 12))
        elif game_state == State.GAMEOVER:
            surface.blit(res.Image.LOSE.value, (0, screen_height / 2 - 12))
    
    road_below_y = road.rect.bottom
    if game_state == State.EDITING:
        surface.blit(res.Font.NJ.value.render(f"L/R: Scroll", False, (143, 98, 51)), (0, road_below_y))
        surface.blit(res.Font.NJ.value.render(f"Wheel: Change", False, (143, 98, 51)), (0, road_below_y + 10))
        surface.blit(res.Font.NJ.value.render(f"LMB: Place", False, (143, 98, 51)), (0, road_below_y + 20))
        surface.blit(res.Font.NJ.value.render(f"RMB: Delete", False, (143, 98, 51)), (0, road_below_y + 30))
        surface.blit(res.Font.NJ.value.render(f"MMB: Change", False, (143, 98, 51)), (0, road_below_y + 40))
        surface.blit(res.Font.NJ.value.render(f"E: Switch to play", False, (143, 98, 51)), (0, road_below_y + 50))
        surface.blit(res.Font.NJ.value.render(f"V: See avl", False, (143, 98, 51)), (0, road_below_y + 60))
    elif game_state == State.PLAYING:
        surface.blit(res.Font.NJ.value.render(f"E: Switch to edit", False, (143, 98, 51)), (0, road_below_y))
        surface.blit(res.Font.NJ.value.render(f"Space/C/X: Jump", False, (143, 98, 51)), (0, road_below_y + 10))
        surface.blit(res.Font.NJ.value.render(f"Up/Down: Dodge", False, (143, 98, 51)), (0, road_below_y + 20))
        surface.blit(res.Font.NJ.value.render(f"V: See avl", False, (143, 98, 51)), (0, road_below_y + 30))


# ------------------------------------------------
# Save/Load funcs
# ------------------------------------------------

def load_json():
    """ Load configurable data from disk """
    # load atomic properties
    global player_velocity, framerate, tree, player_sprite, player, tree, obstacle_damage
    # --- Global decl end ---
    with open('data.json', 'r') as file:
        loaded_data = json.load(file)
        road.length = loaded_data["config"]["road_length"]
        player_velocity = loaded_data["config"]["player_velocity"]
        framerate = loaded_data["config"]["framerate"]
        player.jump_distance = loaded_data["config"]["jump_distance"]
        player_sprite = loaded_data["config"]["player_sprite"]
        player.image = pygame.image.load( player_sprite ).convert_alpha()
        # load obstacles
        tree.clear()
        for obs in loaded_data["objects"]:
            obstacle = obstacle_from_index(obs["type"], obs["x"], obs["y"])
            tree.add(obstacle.as_point())
        pass

def save_json():
    """ Save configurable data to disk """
    global player_velocity, framerate, tree, player_sprite, player, tree, obstacle_damage
    # --- Global decl end ---
    with open('data.json', 'w') as file:
        json.dump({
            "config": {
                "road_length": road.length,
                "player_velocity": player_velocity,
                "framerate": framerate,
                "jump_distance": player.jump_distance,
                "player_sprite": player_sprite
            },
            "objects": [{ "x": obj.x, "y": obj.y, "type": obj.obstacle.type } for obj in tree.LIR_list()]
        }, file, indent=4)

# ------------------------------------------------
# Misc
# ------------------------------------------------

def point_inside_rect(x, y, rect):
    """ Checks if a point (x, y) is inside a pygame rect """
    return x >= rect.x and x <= rect.right and y >= rect.y and y <= rect.bottom