# PAC Import/Export
Easily import BDO PAC files into blender
Easily export BDO PAC files from blender

# Godot Engine's "Better" Collada exporter for Blender
Enhanced Collada exporter for [Blender](https://www.blender.org).

## Installation

1. Copy the `io_scene_pac` directory, to the location where Blender stores the
   scripts/addons folder on your system (you should see other io_scene_*
   folders there from other addons)
   If you downloaded blender through steam, the directory path is:
   SteamInstallDir\steamapps\common\Blender\<newest blender version>\scrips\addons
   Copy the entire dir and not just its
   contents.
2. Go to the Blender settings and enable the "PAC format and Better Collada Exporter" plugin.
3. Enjoy full-featured PAC Import/Export and Collada export.

## Note
The PAC Import can be found at File>Import>PAC Import
The PAC Export can be found at File>Export>PAC Export
The better collada export can be found at File>Export>Better Callada (.dae)

This tool has been modified for better compatibility with PACtool.

The PACtool version is 1.4.3

If you find bugs or want to suggest improvements for the PAC import/export, please contact 
the userid 290513750027534356 on discord.
If you find bugs or want to suggest improvements for the collada exporter, please open an issue on the
upstream [GitHub repository](https://github.com/godotengine/collada-exporter).

## Pac Import
1. Click on File>Import>PAC Import
2. Select an pac file to import
3. Done

## Pac Export
1. Click on File>Export>PAC Export
2. Select the pac file, in which the mesh ( DAE ) should be replaced
3. Done

## Better Collada Export
1. Click on File>Export>Better Callada (.dae)
2. Select a filepath to where the file, should be saved, or the file which should be overwritten
3. Done

## License

This Better Collada exporter is distributed under the terms of the GNU General
Public License, version 2 or later. See the [LICENSE.txt](/LICENSE.txt) file
for details.
