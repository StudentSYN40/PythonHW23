from map import Map
import time
import os
import json
from helicopter import Helicopter as Helico
from utils import clear_terminal
from clouds import Clouds
from pynput import keyboard

TICK_SLEEP = 0.05
TREE_UPDATE = 50
FIRE_UPDATE = 75
CLOUDS_UPDATE = 100
MAP_W, MAP_H = 10, 10
MOVES = {'w': (-1, 0),'d': (0, 1),'s': (1, 0),'a': (0, -1)} 
# f - сохранение, g - восстановление
tmp = Map(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
tick = 1


def process_key(key):
    global helico, tick, clouds, tmp
    c = key.char.lower()

    # обработка движений вертолета
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helico.move(dx, dy)
    # сохранение игры
    elif c == 'f':
        data = {"helicopter": helico.export_data(),
                "clouds": clouds.export_data(),
                "field": tmp.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    # загрузка игры
    elif c == 'g':
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
        tick = data["tick"] or 1
        helico.import_data(data["helicopter"])
        tmp.import_data(data["field"])
        clouds.import_data(data["clouds"])

command = clear_terminal()
            

listener = keyboard.Listener(
    on_press = process_key,
    on_release = None)
listener.start()


while True:
    os.system(command)
    tmp.process_helicopter(helico, clouds)   
    helico.print_stats()
    tmp.print_map(helico, clouds)
    print("TICK", tick)

    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        tmp.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        tmp.update_fires(helico)
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()
