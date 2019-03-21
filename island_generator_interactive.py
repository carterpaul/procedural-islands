from tkinter import *
from noise import snoise2
import math
from random import randint

SEED = randint(0, 1024)
print("SEED:", SEED)

OCTAVES = 3
PERSISTENCE = 0.3
LACUNARITY = 3.0
IMG_SIZE = 256
IMG_SCALE = 2
LANDSCAPE_SCALE = 0.1
FREQUENCY = IMG_SIZE * LANDSCAPE_SCALE * OCTAVES

DEEP_OCEAN = "#122F5E"
MID_OCEAN = "#173C72"
SHALLOW_OCEAN = "#1E4C8E"
BEACH = "#F9D986"
LOWLANDS = "#679A19"
HIGHLANDS = "#677819"
MOUNTAIN = "#44442F"
SNOW = "#F0F0F0"


# recieves heightmap. an array of elements 0-255
# returns array of RGB tuples
def islandify(heightmap):
    island = [[0] * IMG_SIZE for i in range(IMG_SIZE)]
    for x in range(len(heightmap)):
        for y in range(len(heightmap)):
            height = heightmap[x][y]
            if height < 48:
                island[x][y] = DEEP_OCEAN
            elif height < 96:
                island[x][y] = MID_OCEAN
            elif height < 128:
                island[x][y] = SHALLOW_OCEAN
            elif height < 145:
                island[x][y] = BEACH
            elif height < 170:
                island[x][y] = LOWLANDS
            elif height < 190:
                island[x][y] = HIGHLANDS
            elif height < 210:
                island[x][y] = MOUNTAIN
            else:
                island[x][y] = SNOW
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


def draw_image(img, canvas):
    global newimg
    pixels = islandify(generate_heightmap())
    newimg = PhotoImage(width=IMG_SIZE, height=IMG_SIZE)
    for x in range(IMG_SIZE):
        for y in range(IMG_SIZE):
            img.put(pixels[x][y], (x, y))
    newimg.zoom(IMG_SCALE)
    if startimg is not None:
        canvas.itemconfigure(startimg, image=newimg)
    # canvas.create_image((IMG_SIZE*IMG_SCALE/2, IMG_SIZE*IMG_SCALE/2), image=newimg)


startimg = None
window = Tk()
canvas = Canvas(window, width=IMG_SIZE*IMG_SCALE, height=IMG_SIZE*IMG_SCALE)
canvas.pack()
img = PhotoImage(width=IMG_SIZE, height=IMG_SIZE)
pixels = islandify(generate_heightmap())
draw_image(img, canvas)
img = img.zoom(IMG_SCALE)
startimg = canvas.create_image((IMG_SIZE*IMG_SCALE/2, IMG_SIZE*IMG_SCALE/2), image=img)


updateButton = Button(window, text="Update", command=lambda: draw_image(img, canvas))
updateButton.pack(side=RIGHT, padx=5, pady=5)
slide = Scale(window, from_=0, to=100, orient=HORIZONTAL)
slide.pack(side=LEFT)


while True:
    window.update_idletasks()
    window.update()
    SEED = slide.get()
