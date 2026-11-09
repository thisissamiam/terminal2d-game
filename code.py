import random
from opensimplex import OpenSimplex
import blessed
import time
import cbor2
import os
import zlib
import psutil
import base64

world = []

term = blessed.Terminal()
print(term.clear)

# Debugging
process = psutil.Process(os.getpid())
last_debug_time = time.time()
debug_frames = 0
debug_times = {
    'input': 0,
    'gravity': 0,
    'terrain': 0,
    'editing': 0,
    'render': 0
}

def debug_start():
    return time.perf_counter()

def debug_end(name, start):
    debug_times[name] += time.perf_counter() - start

def debug_frame():
    global last_debug_time
    global debug_frames

    debug_frames += 1
    now = time.time()

    if now - last_debug_time >= 1:
        elapsed = now - last_debug_time
        fps_debug = debug_frames / elapsed
        cpu = process.cpu_percent()

        with open("game_debug.txt", "a") as file:
            file.write(
                "FPS: " + str(round(fps_debug, 1)) +
                " | CPU: " + str(round(cpu, 1)) + "%" +
                " | Input: " + str(round(debug_times['input'] * 1000 / debug_frames, 2)) + "ms/frame" +
                " | Gravity: " + str(round(debug_times['gravity'] * 1000 / debug_frames, 2)) + "ms/frame" +
                " | Terrain: " + str(round(debug_times['terrain'] * 1000 / debug_frames, 2)) + "ms/frame" +
                " | Editing: " + str(round(debug_times['editing'] * 1000 / debug_frames, 2)) + "ms/frame" +
                " | Render: " + str(round(debug_times['render'] * 1000 / debug_frames, 2)) + "ms/frame\n"
            )

        for key in debug_times:
            debug_times[key] = 0

        debug_frames = 0
        last_debug_time = now


# Chunk Settings

worldy = 0
tick = 0
reach = 5
velocity = 1
fps = 0
fpsframe = 0
saved = ''
worldname = 'World'
bordertrigger = None
health = 10
showhealth = True
healthtick = 0
lastvelocity = 0
undercurser = None
solidtiles = ['#', '|']
gravitytiles = ['#', '|', 'l']
flight = False
start = 0

chunk = []
worldchanges = {}
curserx = 3
cursery = 0


class blocks:
    air = 0
    stone = 1
    log = 2
    leaf = 3
    wheat = 4


blockidtochar = {
    0: ' ',
    1: '#',
    2: '|',
    3: '@',
    4: 'F'
}

chartoblockid = {
    ' ': 0,
    '#': 1,
    '|': 2,
    '@': 3,
    'F': 4
}


def editchunk():
    global lastvelocity
    global health
    global undercurser

    for y in range(height):
        for x in range(width):
            blockx = x + worldx + centerx
            blocky = y + worldy

            if (blockx, blocky) in worldchanges:
                chunk[y * width + x] = worldchanges.get((blockx, blocky))

    chunk[centerx + centery * width] = '!'
    undercurser = chunk[centerx + curserx + (centery + cursery) * width]
    chunk[centerx + curserx + (centery + cursery) * width] = 'X'

    if bordertrigger == 'up':
        chunk[centerx + curserx + (centery + cursery - 1) * width] = '_'
    elif bordertrigger == 'down':
        chunk[centerx + curserx + (centery + cursery + 1) * width] = '_'
    elif bordertrigger == 'left':
        chunk[centerx + curserx - 1 + (centery + cursery) * width] = '|'
    elif bordertrigger == 'right':
        chunk[centerx + curserx + 1 + (centery + cursery) * width] = '|'

    if showhealth:
        for i in range(int(health)):
            chunk[i] = '='

        for i in range(10 - int(health)):
            chunk[i + int(health)] = '-'

    if health == 0:
        text = [
            '+-----------+',
            '| YOU DIED  |',
            '|Respawn (1)|',
            '+-----------+'
        ]

        for line in range(len(text)):
            for char in range(len(text[line])):
                chunk[(5 + line) * width + centerx - len(text[line]) // 2 + char] = text[line][char]


def generateterrain():
    global worldx
    global worldy
    global chunk

    chunk = [' '] * width * height

    for x in range(width):
        topheight = 15 - int(gen.noise2((x + worldx + centerx) / 10.0, 0) * 10)

        for y in range(height):
            worldblocky = y + worldy

            if worldblocky >= topheight:
                chunk[y * width + x] = '#'

        wheaty = topheight - worldy - 1

        if wheatgen.noise2((x + worldx + centerx) / 10.0, 0) > 0.2:
            if wheaty >= 0 and wheaty < height:
                chunk[wheaty * width + x] = 'F'

    for x in range(width):
        treex = x + worldx + centerx
        topheight = 15 - int(gen.noise2(treex / 10.0, 0) * 10)
        treey = topheight - worldy - 1

        if treex % 8 == 0:
            if treegen.noise2(treex / 10.0, 0) > 0.3:
                tree = [
                    '           @    ',
                    '          @@@   ',
                    '         @@@@@  ',
                    '           |    ',
                    '           |    ',
                    '           |    '
                ]

                tree = list(reversed(tree))

                for line in range(len(tree)):
                    for char in range(len(tree[line])):
                        if tree[line][char] != ' ':
                            treerow = treey - line
                            treex_screen = x + char - 11

                            if 0 <= treex_screen < width and 0 <= treerow < height:
                                chunk[treerow * width + treex_screen] = tree[line][char]


def findspawnlocation():
    global centerx

    topheight = 15 - int(gen.noise2((worldx + centerx + centerx) / 10.0, 0) * 10)

    if wheatgen.noise2((worldx + centerx + centerx) / 10.0, 0) > 0.2:
        topheight -= 1

    return topheight - 1


def move():
    global worldx
    global centerx
    global worldy
    global cursery
    global curserx
    global reach
    global bordertrigger
    global saved
    global health
    global flight

    key = term.inkey(timeout=0.005)

    if key == 'd':
        if chunk[1 + centerx + centery * width] not in solidtiles:
            worldx += 1

    elif key == 'a':
        if chunk[centerx + centery * width - 1] not in solidtiles:
            worldx -= 1

    elif key == 'w':
        if chunk[centerx + (centery - 1) * width] not in solidtiles:
            if flight:
                worldy -= 1
            else:
                if onground():
                    worldy -= 1

    elif key == 's':
        if flight:
            if chunk[centerx + (centery + 1) * width] not in solidtiles:
                worldy += 1

    elif key.name == 'KEY_UP':
        if cursery > -reach:
            cursery -= 1
            bordertrigger = None
        else:
            bordertrigger = 'up'

    elif key.name == 'KEY_DOWN':
        if cursery < reach:
            cursery += 1
            bordertrigger = None
        else:
            bordertrigger = 'down'

    elif key.name == 'KEY_LEFT':
        if curserx > -reach:
            curserx -= 1
            bordertrigger = None
        else:
            bordertrigger = 'left'

    elif key.name == 'KEY_RIGHT':
        if curserx < reach:
            curserx += 1
            bordertrigger = None
        else:
            bordertrigger = 'right'

    elif key.name == 'KEY_ENTER':
        blockx = centerx + curserx + worldx + centerx
        blocky = centery + cursery + worldy
        worldchanges[(blockx, blocky)] = ' '

    elif key == ' ':
        blockx = centerx + curserx + worldx + centerx
        blocky = centery + cursery + worldy

        if chunk[centerx + curserx + (centery + cursery) * width] == ' ':
            worldchanges[(blockx, blocky)] = '#'

    elif key == '1':
        if health == 0:
            health = 10
            worldx = -50
            worldy = findspawnlocation() - centery

            while worldchanges.get((worldx + centerx * 2, centery + worldy), ' ') != ' ':
                worldy -= 1

            curserx = 3
            cursery = 0

    elif key == 'f':
        flight = not flight

    elif key == 'p':
        saveworld = [seed, worldchanges]

        with open(worldname + ".samcraft", "wb") as file:
            file.write(zlib.compress(cbor2.dumps(saveworld)))

        saved = True

    elif key == 'l':
        blockx = centerx + curserx + worldx + centerx
        blocky = centery + cursery + worldy

        if chunk[centerx + curserx + (centery + cursery) * width] == ' ':
            worldchanges[(blockx, blocky)] = 'l'


def gravity():
    global velocity
    global tick
    global centerx
    global centery
    global worldy
    global health
    global lastvelocity

    if not onground():
        tick += velocity

        if velocity <= 50:
            velocity *= 1.03

        if tick >= 40:
            worldy += 1
            tick = 0

        lastvelocity = velocity

    else:
        tick = 0
        velocity = 1
        health -= lastvelocity // 5

        if health < 0:
            health = 0

        lastvelocity = 0


def onground():
    return chunk[centerx + (centery + 1) * width] in gravitytiles


def render():
    global fps
    global saved
    global fpsframe
    global start

    frame = ''

    for row in range(height - 1):
        colorcoderframelist = []
        colorcodegframelist = []
        colorcodebframelist = []
        tiletextframelist = []

        for tile in chunk[row * width:row * width + width]:
            incolorcode = False
            tiletext = ''
            colorcode = ''

            for char in tile:
                if char == '`':
                    if incolorcode:
                        incolorcode = False
                    else:
                        incolorcode = True
                        continue
                else:
                    if not incolorcode:
                        tiletext += char

                if incolorcode:
                    colorcode += char

            colormode = 'r'
            r = ''
            g = ''
            b = ''

            for char in colorcode:
                if char == ',':
                    if colormode == 'r':
                        colormode = 'g'
                    elif colormode == 'g':
                        colormode = 'b'
                else:
                    if colormode == 'r':
                        r += char
                    elif colormode == 'g':
                        g += char
                    elif colormode == 'b':
                        b += char

            colorcoderframelist.append(r)
            colorcodegframelist.append(g)
            colorcodebframelist.append(b)
            tiletextframelist.append(tiletext)

        for tile in range(len(tiletextframelist)):
            if colorcoderframelist[tile] == '':
                frame = frame + tiletextframelist[tile]
            else:
                frame = frame + term.color_rgb(
                    colorcoderframelist[tile],
                    colorcodegframelist[tile],
                    colorcodebframelist[tile]
                )(tiletextframelist[tile])

        if row != height - 1:
            frame += '\n'

    if fpsframe > 60:
        timeinframe = time.perf_counter() - start
        fps = fpsframe / timeinframe
        start = time.perf_counter()
        fpsframe = 0
    else:
        fpsframe += 1

    print(
        term.home + frame,
        str(round(fps, 1)) + '   ' + str(seed) + '    ' + str(saved),
        end="",
        flush=True
    )


def checkhealth():
    global health
    global showhealth
    global healthtick

    if health <= 0:
        healthtick += 1

        if healthtick >= 30:
            healthtick = 0

        if healthtick <= 10:
            showhealth = False
        else:
            showhealth = True

    else:
        showhealth = True
        healthtick = 0


def calculatescreenres():
    global width
    global height
    global centery
    global centerx

    width = term.width
    height = term.height
    centery = height // 2
    centerx = width // 2


def gameloop():
    global undercurser

    with term.cbreak(), term.hidden_cursor():
        while True:
            frame_start = time.perf_counter()

            calculatescreenres()

            stage_start = debug_start()
            move()
            debug_end('input', stage_start)

            stage_start = debug_start()
            if not flight:
                gravity()
            checkhealth()
            debug_end('gravity', stage_start)

            stage_start = debug_start()
            generateterrain()
            debug_end('terrain', stage_start)

            stage_start = debug_start()
            editchunk()
            debug_end('editing', stage_start)

            stage_start = debug_start()
            render()
            debug_end('render', stage_start)

            chunk[centerx + curserx + (centery + cursery) * width] = undercurser

            debug_frame()


user = input('DO YOU WANT TO LOAD A WORLD OR MAKE ONE SAY L TO MAKE M TO MAKE\n')

if user == 'L':
    for filename in os.listdir("."):
        if filename.endswith(".samcraft"):
            print(filename)

    user = input('WHAT IS YOUR WORLD NAME IT PROBALLY CRASHES RIGHT NOW IF IT DOESNT EXIST\n')

    start = time.perf_counter()

    with open(user + ".samcraft", "rb") as file:
        saveworld = cbor2.loads(zlib.decompress(file.read()))

    worldname = user
    seed = saveworld[0]
    worldchanges = saveworld[1]
    loaded = True

elif user == 'M':
    user = input('WHAT DO YOU WANT TO CALL YOUR WORLD\n')
    worldname = user.strip()

    user = input('What seed? Or just hit enter for a random one\n')

    if user.isdigit() and int(user) < 2**64 - 100:
        seed = int(user)
    else:
        print('I am assuming you want a random seed')
        seed = random.randint(0, 100000000)

    loaded = False

else:
    print('you suck its ur fault i didnt allow for lowercase letters if thats why idk u suck all ur problem')
    exit()

print('Starting generation, this probally won\'t take long')

gen = OpenSimplex(seed=seed)
wheatgen = OpenSimplex(seed=seed + 1)
treegen = OpenSimplex(seed=seed + 2)
cavegen = OpenSimplex(seed=seed + 3)

calculatescreenres()

worldx = -50
spawny = findspawnlocation()
worldy = spawny - centery

if loaded:
    while worldchanges.get((worldx + centerx * 2, centery + worldy), ' ') != ' ':
        worldy -= 1

generateterrain()
render()
gameloop()