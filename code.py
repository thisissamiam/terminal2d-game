import random
from opensimplex import OpenSimplex
import blessed
import time

world = []
seed = random.randint(0, 100000000)
wheatgen = OpenSimplex(seed=seed + 1)
treegen = OpenSimplex(seed=seed + 2)
cavegen = OpenSimplex(seed=seed + 3)
gen = OpenSimplex(seed=seed)
term = blessed.Terminal()

print(term.clear)

worldy = 0
tick = 0
reach = 5
velocity = 1
bordertrigger = None
health = 10
showhealth = True
healthtick = 0
lastvelocity = 0
undercurser = None
solidtiles = ['#', '|']
flight = False

chunk = []
worldchanges = {}
curserx = 3
cursery = 0

# Performance statistics (times are measured in milliseconds).
stats = {
    'terrain': 0.0,
    'caves': 0.0,
    'trees': 0.0,
    'editing': 0.0,
    'rendering': 0.0,
    'loop': 0.0
}
stats_frames = 0
stats_started = time.perf_counter()
stats_show = True
stats_display = ''


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

    # Terrain and wheat
    start = time.perf_counter()

    for x in range(width):
        worldblockx = x + worldx + centerx
        topheight = 15 - int(gen.noise2(worldblockx / 10.0, 0) * 10)

        for y in range(height):
            worldblocky = y + worldy
            if worldblocky >= topheight:
                chunk[y * width + x] = '#'

        wheaty = topheight - worldy - 1
        if wheatgen.noise2(worldblockx / 10.0, 0) > 0.2:
            if 0 <= wheaty < height:
                chunk[wheaty * width + x] = 'F'

    stats['terrain'] = (time.perf_counter() - start) * 1000

    # Caves
    # Caves
    start = time.perf_counter()

    for x in range(width):
        worldblockx = x + worldx + centerx
        topheight = 15 - int(gen.noise2(worldblockx / 10.0, 0) * 10)

        for y in range(height):
            index = y * width + x
            worldblocky = y + worldy

            # Only generate caves well underground
            if worldblocky >= topheight + 4 and chunk[index] in solidtiles:
                cave = cavegen.noise2(
                    worldblockx / 10.0,
                    worldblocky / 10.0
                )

                if cave > 0.3:
                    chunk[index] = ' '

    stats['caves'] = (time.perf_counter() - start) * 1000

    # Trees
    start = time.perf_counter()

    for x in range(width):
        treex = x + worldx + centerx
        topheight = 15 - int(gen.noise2(treex / 10.0, 0) * 10)
        treey = topheight - worldy - 1

        if treex % 8 == 0:
            if treegen.noise2(treex / 10.0, 0) > 0.3:
                if 0 <= treey < height:
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

    stats['trees'] = (time.perf_counter() - start) * 1000


def findspawnlocation():
    global centerx
    global worldx

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
    global health
    global flight

    key = term.inkey(timeout=0.01)

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
        if velocity <= 30:
            velocity *= 1.05

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
    return chunk[centerx + (centery + 1) * width] in solidtiles


def render():
    global stats_display

    render_start = time.perf_counter()

    frame = ''
    for row in range(height):
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
                frame += tiletextframelist[tile]
            else:
                frame += term.color_rgb(
                    int(colorcoderframelist[tile]),
                    int(colorcodegframelist[tile]),
                    int(colorcodebframelist[tile])
                )(tiletextframelist[tile])

        if row != height - 1:
            frame += '\n'

    # Show stats on the last terminal row without changing the actual world.
    if stats_show:
        frame_rows = frame.split('\n')
        if frame_rows:
            frame_rows[-1] = stats_display[:width].ljust(width)
            frame = '\n'.join(frame_rows)

    print(term.home + frame, end='', flush=True)

    # This includes frame building AND terminal output.
    stats['rendering'] = (time.perf_counter() - render_start) * 1000

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
    global stats_frames
    global stats_started
    global stats_display

    with term.cbreak(), term.hidden_cursor():
        while True:
            loop_start = time.perf_counter()

            calculatescreenres()
            move()

            if not flight:
                gravity()

            checkhealth()
            generateterrain()

            edit_start = time.perf_counter()
            editchunk()
            stats['editing'] = (time.perf_counter() - edit_start) * 1000

            stats_frames += 1

            now = time.perf_counter()
            elapsed = now - stats_started

            # Refresh the displayed stats only twice per second.
            if elapsed >= 0.5:
                fps = stats_frames / elapsed
                stats_display = (
                    'GEN T:{:.1f} C:{:.1f} TR:{:.1f} EDIT:{:.1f} '
                    'RENDER:{:.1f}ms FPS:{:.1f}'
                ).format(
                    stats['terrain'], stats['caves'], stats['trees'],
                    stats['editing'], stats['rendering'], fps
                )
                stats_frames = 0
                stats_started = now

            render()
            chunk[centerx + curserx + (centery + cursery) * width] = undercurser
            stats['loop'] = (time.perf_counter() - loop_start) * 1000

calculatescreenres()
worldx = -50
spawny = findspawnlocation()
worldy = spawny - centery

generateterrain()
render()
gameloop()
