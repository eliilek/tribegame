import json
import importlib
from tile import Tile

# read objects Tile from file and return list of Tiles
def readfile(file_path):
    tiles = []
    with open(file_path, 'r') as file:
        for line in file:
            tile = json.loads(line)
            jobs = parseobjs('jobs', tile['jobs'])
            tile['jobs'] = jobs
            buildings = parseobjs('tile', tile['buildings'])
            tile['buildings'] = buildings
            tiles.append(Tile(**tile))
    return tiles

# parse complex objects Jobs and Buildings from string
def parseobjs(module_name, objs):
    objs_instances = []
    for obj in objs:
        objclass = class_for_name(module_name, obj['name'])
        objs_instances.append(objclass(**obj['attribs']))
    return objs_instances

# return Class object from string
def class_for_name(module_name, class_name):
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c

if __name__ == "__main__":
    tiles = readfile("Tile.txt")
    for tile in tiles:
        print tile
