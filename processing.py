from colorthief import ColorThief
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

from os import listdir
from os.path import isfile, join

from random import randrange

import json

class Block:
    def __init__(self, name, img, color=None, texture=None):
        self.name = name
        self.img = img
        self.color = ''
        self.textures = []

    def __str__(self):
        blockStr = '{:<40s} | {:40s}| {:<15s}'.format(self.name, self.img, self.color)
        textureStr = '| '
        if len(self.textures) != 0:
            for i in range(0, len(self.textures)):
                if len(self.textures) == 1 or i == (len(self.textures) - 1):
                    textureStr = textureStr + self.textures[i]
                else:
                    textureStr = textureStr + self.textures[i] + ', '

        blockStr = blockStr + textureStr
        return blockStr

    def setColor(self, color):
        self.color = color

    def setTexture(self, texture):
        self.textures.append(texture)

class Palette:
    def __init__(self, paletteID, blocks):
        self.paletteID = paletteID
        self.blocks = blocks

class Color:
    def __init__(self, name, rgb):
        self.name = name
        self.rgb = rgb

def createBlockList():
    files = [ f for f in listdir('block') if isfile(join('block', f))]
    blockList = []
    for name in files:
        blockName = name.replace('_',' ').replace('.png','').title()
        blockList.append(Block(blockName, name))

    return blockList

def setColors(blockList):

    white = Color('White', sRGBColor(249, 255, 255))
    lightGray = Color('Light Gray', sRGBColor(156, 157, 151))
    gray = Color('Gray', sRGBColor(71, 79, 82))
    black = Color('Black', sRGBColor(29, 28, 33))
    yellow = Color('Yellow', sRGBColor(255, 216, 61))
    orange = Color('Orange', sRGBColor(249, 128, 29))
    red = Color('Red', sRGBColor(176, 46, 38))
    brown = Color('Brown', sRGBColor(130, 84, 50))
    lime = Color('Lime', sRGBColor(128, 199, 31))
    green = Color('Green', sRGBColor(93, 124, 21))
    lightBlue = Color('Light Blue', sRGBColor(58, 179, 218))
    cyan = Color('Cyan', sRGBColor(22, 156, 157))
    blue = Color('Blue', sRGBColor(60, 68, 169))
    pink = Color('Pink', sRGBColor(243, 140, 170))
    magenta = Color('Magenta', sRGBColor(198, 79, 189))
    purple = Color('Purple', sRGBColor(137, 50, 183))
    colors = [white, lightGray, gray, black, yellow, orange, red, brown, lime, green, lightBlue, cyan, blue, pink, magenta, purple]

    for block in blockList:
        # Compare by name
        for color in colors:
            if color.name in block.name:
                block.setColor(color.name)
                break

        # Compare by color
        if block.color == '':
            img = ColorThief('block/' + block.img)
            dominant = img.get_color(quality=3)

            # Format as sRGBColor
            imgColor = sRGBColor(dominant[0], dominant[1], dominant[2])

            # Compare
            imgLab = convert_color(imgColor, LabColor)
            minDiff = 0
            for color in colors:
                colorLab = convert_color(color.rgb, LabColor)
                diff = delta_e_cie2000(imgLab, colorLab)
                if minDiff == 0 or diff < minDiff:
                    minDiff = diff
                    block.setColor(color.name)
            
def setTextures(blockList):
    singles = ['concrete', 'terracotta', 'mushroom', 'wool', 'shulker', 'coral', 'glass', 'ice', 'sand', 'snow', 'sponge']

    for block in blockList:
        # Check singles
        for single in singles:
            if single in block.name.lower():
                block.setTexture(single.capitalize())
                break

        # Check woods
        woods = ['log', 'plank', 'trapdoor', 'barrel', 'note jlock', 'jukebox', 'nest', 'hive', 'warped stem', 'cartography', 'composter', 'crafting', 'fletching', 'bookshelf', 'scaffold', 'loom', 'ladder']
        for wood in woods:
            if wood in block.name.lower():
                block.setTexture('Wood')
        
        # Check stones
        stones = ['stone', 'deepslate', 'andesite', 'diorite', 'granite', 'basalt', 'calcite', 'tuff', 'gravel', 'smithing', 'furnace', 'smoker', 'cauldron', 'bricks', 'bedrock', 'observer']
        for stone in stones:
            if stone in block.name.lower() and not 'sandstone' in block.name.lower():
                block.setTexture('Stone')

        # Check ores
        ores = ['iron', 'gold', 'diamond', 'coal', 'emerald', 'quartz', 'copper', 'redstone', 'amethyst', 'debris', 'lapis']
        for ore in ores:
            if ore in block.name.lower():
                block.setTexture('Ore')

        # Check dirt
        dirts = ['mycelium', 'podzol', 'dirt', 'grass', 'gravel', 'soul', 'moss block']
        for dirt in dirts:
            if dirt in block.name.lower():
                block.setTexture('Dirt')

        # Check nether
        nethers = ['nether', 'blackstone', 'basalt', 'quartz', 'warped', 'crimson', 'soul', 'shroomlight', 'obsidian', 'lode', 'debris']
        for nether in nethers:
            if nether in block.name.lower():
                block.setTexture('Nether')

        # Check light
        lights = ['glowstone', 'lantern', 'shroomlight', 'lamp']
        for light in lights:
            if light in block.name.lower():
                block.setTexture('Light')

        # Check prismarine
        seaBlocks = ['prismarine', 'sea', 'coral', 'kelp']
        for seaBlock in seaBlocks:
            if seaBlock in block.name.lower():
                block.setTexture('Sea Blocks')

        # Check Redstones
        redstones = ['redstone', 'target', 'note block', 'hopper', 'lamp', 'tnt', 'detector', 'sensor', 'piston', 'observer', 'magma']
        for redstone in redstones:
            if redstone in block.name.lower():
                block.setTexture('Redstone')

        # Check end
        ends = ['purpur', 'end']
        for end in ends:
            if end in block.name.lower():
                block.setTexture('End')
        
def formatBlockJSON(block):
    blockData = {}
    blockData['name'] = block.name
    blockData['img'] = block.img
    blockData['color'] = block.color
    blockData['textures'] = block.textures

    return blockData


def randomizePalette(blockList):
    paletteBlocks = []
    paletteIDs = []

    colors = ['White', 'Light Gray', 'Gray', 'Black', 'Yellow', 'Orange', 'Red', 'Brown', 'Lime', 'Green', 'Light Blue', 'Cyan', 'Blue', 'Pink', 'Magenta', 'Purple']
    combo = []

    for i in range(0, 3):
        randIndex = round(randrange(len(colors)))
        while blockList[randIndex] in combo:
            randIndex = round(randrange(len(colors)))


        combo.append(colors[randIndex])
        combo.append(colors[randIndex])

    for i in range(0, 6):
        randColor = round(randrange(len(combo)))
        colorBlocks = [block for block in blockList if block.color == combo[randColor]]
        combo.remove(combo[randColor])

        blockID = round(randrange(len(colorBlocks)))
        while blockID in paletteIDs:
            blockID = round(randrange(len(colorBlocks)))

        paletteIDs.append(blockID)
        paletteBlocks.append(colorBlocks[blockID])
    
    return paletteBlocks

def createAllPalettes(blockList):
    allPalettes = []
    for i in range(0, 500):
        print(i)
        blocks = randomizePalette(blockList)
        allPalettes.append(Palette(i, blocks))

    return allPalettes

def formatPaletteJSON(allPalettes):
    print(len(allPalettes))
    paletteData = [None] * len(allPalettes)
    for i in range(0, len(allPalettes)):
        paletteData[i] = {}
        paletteData[i]['paletteID'] = allPalettes[i].paletteID
        paletteData[i]['saved'] = "False"
        paletteBlocks = []
        for j in range(0, len(allPalettes[i].blocks)):
            paletteBlocks.append(formatBlockJSON(allPalettes[i].blocks[j]))
        
        paletteData[i]['blocks'] = paletteBlocks

    with open('paletteData.json', 'w') as outfile:
        json.dump(paletteData, outfile)



if(__name__ == "__main__"):
    blockList = createBlockList()
    setColors(blockList)
    setTextures(blockList)
    allPalettes = createAllPalettes(blockList)
    formatPaletteJSON(allPalettes)