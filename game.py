import pygame
import json
import tree
import res

from enum import Enum

from road import Road
from player import Player

from point import Point
from obstacle import obstacle_from_index, obstacle_texture_from_index, obstacle_variants

class State(Enum):
    EDITING = 0
    PLAYING = 1
    WINNER = 2
    GAMEOVER = 3

game_state: State = State.EDITING

edit_scroll_velocity: float = 0
focused_obj: Point = None
placeholder_texture_index: int = 0

player_velocity: float = 5
framerate: int = 30

tree = tree.Tree()

road: Road = None
player: Player = None

rendering_queue = []



def init(SCREEN_WIDTH: int, SCREEN_HEIGHT: int):
    global road, player
    road = Road(screen_width=SCREEN_WIDTH, length=5)
    player = Player(road=road)
    road.rect.y = (SCREEN_HEIGHT - road.rect.h) / 2
    load_json()

def event_update(event: pygame.event.Event):
    global placeholder_texture_index
    if event.type == pygame.KEYDOWN:
        # Check for specific key presses
        if event.key == pygame.K_UP:
            player.lane_up()
        if event.key == pygame.K_DOWN:
            player.lane_down()
        if event.key == pygame.K_SPACE or event.key == pygame.K_c or event.key == pygame.K_x:
            player.jump()
    if game_state == State.EDITING:
        if event.type == pygame.MOUSEWHEEL:
            placeholder_texture_index += 1
            placeholder_texture_index %= obstacle_variants
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and focused_obj is None:
                pos = list(pygame.mouse.get_pos())
                pos[0] += road.offset
                obj = obstacle_from_index(placeholder_texture_index, pos[0], pos[1])
                tree.add(obj.as_point())
            elif event.button == 2:
                placeholder_texture_index += 1
                placeholder_texture_index %= obstacle_variants
            elif event.button == 3:
                if focused_obj:
                    tree.delete(focused_obj)

def pre_update():
    global edit_scroll_velocity
    keys = pygame.key.get_pressed()
    if game_state == State.EDITING:
        sub_vel = 0
        if keys[pygame.K_LEFT]:
            sub_vel = -3
        if keys[pygame.K_RIGHT]:
            sub_vel = 3
        edit_scroll_velocity = (edit_scroll_velocity + player_velocity * sub_vel) / 2
        road.offset += edit_scroll_velocity

def update():
    if len(rendering_queue) > 0 and rendering_queue[0].rect.right - road.offset < 0:
        print(f"Removed left: { rendering_queue.pop(0).as_point() }")
    road.update()
    player.update()
    pass

def post_update():
    if game_state == State.PLAYING:
        road.offset += player_velocity
    elif game_state == State.EDITING:
        pass

def point_inside_rect(x, y, rect):
    return x >= rect.x and x <= rect.right and y >= rect.y and y <= rect.bottom

def draw(screen: pygame.Surface):
    global focused_obj
    screen.blit(res.Image.BG.value, (0,24))
    road.draw(screen)

    rendering_queue = tree.LIR_list()

    if game_state == State.EDITING and focused_obj is None:
        screen.blit(obstacle_texture_from_index(placeholder_texture_index), pygame.mouse.get_pos())

    focused_obj = None

    for object in rendering_queue:
        rect = pygame.Rect(object.obstacle.rect.x - road.offset, object.obstacle.rect.y, object.obstacle.rect.w, object.obstacle.rect.h)
        if game_state == State.EDITING and point_inside_rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], rect):
            focused_obj = object
            pygame.draw.rect(screen, "white", rect)
        screen.blit(object.obstacle.image, rect)
    
    player.draw(screen)
    road_below_y = 0
    screen.blit(res.Font.NJ.value.render(f"HP {player.HP} <{road.completeness}x>", False, (143, 98, 51)), (2, road_below_y))

    # print(pygame.mouse.get_pos())
    pass

def load_json():
    loaded_data = {}
    with open('data.json', 'r') as file:
        loaded_data = json.load(file)
    # load atomic properties
    global player_velocity, framerate
    road.length = loaded_data["config"]["road_length"]
    player_velocity = loaded_data["config"]["player_velocity"]
    framerate = loaded_data["config"]["framerate"]
    player.jump_distance = loaded_data["config"]["jump_distance"]
    player.image = pygame.image.load( loaded_data["config"]["player_sprite"] ).convert_alpha()
    # load obstacles
    tree.clear()
    for obs in loaded_data["objects"]:
        obstacle = obstacle_from_index(obs["type"], obs["x"], obs["y"])
        tree.add(obstacle.as_point())
    pass