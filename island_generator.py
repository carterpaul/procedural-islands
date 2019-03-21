from noise import snoise2
from PIL import Image
import math
from random import randint

SEED = randint(0, 1024)
print("SEED:", SEED)

OCTAVES = 3
PERSISTENCE = 0.3
LACUNARITY = 3.0
IMG_SIZE = 1024
LANDSCAPE_SCALE = 0.1
FREQUENCY = IMG_SIZE * LANDSCAPE_SCALE * OCTAVES

DEEP_OCEAN = (18, 47, 94)
MID_OCEAN = (23, 60, 114)
SHALLOW_OCEAN = (30, 76, 142)
BEACH = (249, 217, 134)
LOWLANDS = (103, 154, 25)
HIGHLANDS = (103, 120, 25)
MOUNTAIN = (68, 68, 47)
SNOW = (240, 240, 240)


# recieves heightmap. an array of elements 0-255
# returns array of RGB tuples
def islandify(heightmap):
    island = []
    for height in heightmap:
        if height < 48:
            island.append(DEEP_OCEAN)
        elif height < 96:
            island.append(MID_OCEAN)
        elif height < 128:
            island.append(SHALLOW_OCEAN)
        elif height < 145:
            island.append(BEACH)
        elif height < 170:
            island.append(LOWLANDS)
        elif height < 190:
            island.append(HIGHLANDS)
        elif height < 210:
            island.append(MOUNTAIN)
        else:
            island.append(SNOW)
    return island


def fallout_curve(x, y):
    return math.sin(math.pi*(x/IMG_SIZE))*math.sin(math.pi*(y/IMG_SIZE))


def generate_heightmap():
    noise_array = [[0] * IMG_SIZE for i in range(IMG_SIZE)]
    for i in range(IMG_SIZE):
        for j in range(IMG_SIZE):
            noise_array[i][j] = int(snoise2(i / FREQUENCY, j / FREQUENCY,
                                    OCTAVES, PERSISTENCE, LACUNARITY,
                                    base=SEED) * 127 + 128) * fallout_curve(i,j)
    return noise_array


flat_array = []
for row in generate_heightmap():
    for item in row:
        flat_array.append(item)

img = Image.new("RGB", (IMG_SIZE, IMG_SIZE))
img.putdata(islandify(flat_array))
img.save("output.png")
