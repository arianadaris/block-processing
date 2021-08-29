# block-processing
This Python script creates a JSON file of 500 randomized Minecraft block palettes based on block color.

The script creates a Block object by parsing the file name of the Minecraft block. It assigns the block a color using the Color Thief module, and assigns texture based on block name. Each block is given an auto-generated block ID which is used when creating Palettes. 

A Palette object is made up of 6 blocks which are picked by color. Three colors are chosen randomly out of the 16 available in Minecraft. For each color, two blocks are randomly selected and placed in the Palette. Each palette is given an auto-generated palette ID.

Then, the script writes each Palette and appropriate data to a JSON file.
