import json

road_length = 10
player_velocity = 5
framerate = 30
jump_distance = 24

obstacles = []

def load():
    loaded_data = {}
    with open("data.json", "r") as f:
        loaded_data = json.load(f)