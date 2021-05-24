# draft2fgu
Script to convert LOS data from Dungeondraft's .dd2vtt files to into a usable format for Fantasy Grounds Unity (FGU)

You can either convert individual files, or you can run the file in any directory with .dd2vtt files.

## How to (simply) use this script:

1. Export your Dungeondraft map in the .dd2vtt format
2. Place the script/executable in the same folder as your .dd2vtt file (or files)
3. Run the script (just double click on the executable)
4. Voila! Your .png & .xml files have been created and are in the same folder. It will do this for all .dd2vtt files in the folder. 
5. Place these in your "Fantasy Grounds\campaigns\{campaign name}\images" folder and import in FGU as normal.

## Command-line
```
usage: draft2fgu.py [OPTIONS] [FILES]

Convert Dungeondraft .dd2vtt files to .png/.xml for Fantasy Grounds Unity
(FGU)

positional arguments:
  files                 Files to convert to .png + .xml for FGU

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           Force overwrite destination files
  -v, --verbose         Display progress
  --version             show program's version number and exit
  -i INPUT, --input INPUT
                        Path to the input directory
  --jpeg, --jpg         Write the image as a .jpg file
  -o OUTPUT, --output OUTPUT
                        Path to the output directory
  --portallength PORTALLENGTH
                        Specify the length of portals
  --portalwidth PORTALWIDTH
                        Specify the width of portals
```

|Option          |Description|
|----------------|-----------|
| -f             | Overwrite the destination files even if they already exist |
| -v             | Display the names of the converted files and some statistics |
| -i INPUT       | Specify the directory to look in for *.dd2vtt files |
| --jpeg         | Also output the map as a .jpg file |
| -o OUTPUT      | Specify the directory to write the output .png and .xml files |
| --portallength | The additional length added to all doors in your map to overlap them with adjacent walls, so there is no LOS gap |
| --portalwidth  | The depth of all doors in your map |
| FILES          | The names of the files to convert |

If you specify filenames to convert, the output will be in the same directory as the input file, unless you have also specified `--output`.
If you have specified filenames to convert, the `--input` parameter is ignored.

If you do not specify any filenames to convert, this will scan the `INPUT` directory for `.dd2vtt` files.  If `INPUT` is not specified, the current directory will be used.

Parameters specified on the command-line supercede those in the `config.txt` file described below.

## Modifying the default behavior
If you want to modify the default behavior, you can modify the parameters in the "config.txt" file:

**input_path** 
* The location of your .dd2vtt files
* The default value of empty quotes will read from the folder the script is run from
* It can take any path to a FOLDER, for example
  "C:/Users/my_user_name/Pictures/my_dungeon_draft_files"

**output_path**
* The location you want your .png and .xml files placed
* You may choose to place these directly in your Fantasy Grounds folder, for example
  "C:/Users/Adam/AppData/Roaming/SmiteWorks/Fantasy Grounds/campaigns/OneShot/image"
* The default value of empty quotes will write to the folder the script is run from
* PLEASE NOTE THAT THIS SCRIPT WILL OVERWRITE EXISITING FILES WITH THE SAME NAME & EXTENSION WITHOUT ASKING

**portal_width**
* The depth of all doors in your map
* This can be defined as a percent of a grid square or as an absolute pixel value
* For example, if your grid has 200px and you specify "20%", your doors will have a depth of 40px
* Decimals are fine. For example, if you want a width of 1/8th of a square, specify "12.5%" 
* Alternaively, instead of a percent, you can specify an absolute value. If you want it to be exactly 50 pixels, specify "50px"
* Empty quotes "" will result in a default value of "25%"

**portal_length**
* The additional length added to all doors in your map to overlap them with adjacent walls, so there is no LOS gap
* This can be defined as a percent of a grid square or as an absolute pixel value
* For example, if your grid has 200px and you specify "2%", your doors will have an overlap of 4px will the walls on either side
* Decimals are fine. For example, if you want a width of 1/8th of a square, specify "12.5%" 
* Alternaively, instead of a percent, you can specify an absolute value. If you want it to be exactly 50 pixels, specify "50px"
* Empty quotes "" will result in a default value of "0px"

The script makes no attempt to correct bad parameters, so please format them exactly as written in the instructions. 
If the file "config.txt" is not present in the same directory, the default values are use.
Below are some valid examples of what you could put in the "config.txt" file 

**You will need to modify file paths to point to valid locations on your computer**
1.
```json
{
	"input_path":"C:/Users/my_user_name/Documents/dnd",
	"output_path":"C:/Users/my_user_name/AppData/Roaming/SmiteWorks/Fantasy Grounds/campaigns/OneShot/images",
	"portal_width":"12.5%",
	"portal_lenght":"2%"
}
```

2.
```json
{
	"input_path":"",
	"output_path":"",
	"portal_width":"40px"
}
```
3.
```json
{
	"input_path":"",
	"output_path":"C:/Users/my_user_name/AppData/Roaming/SmiteWorks/Fantasy Grounds/campaigns/OneShot/images",
	"portal_width":""
}
```

# Acknowledgements

[Dungeondraft](https://dungeondraft.net/) is a map drawing tool.  Dungeondraft is produced by Megasploot.

[Fantasy Grounds Unity](https://www.fantasygrounds.com) is a Virtual TableTop program for playing many different table-top Role Playing Games (TTRPG), virtually.  FGU is produced by SmiteWorks USA LLC.

draft2vtt.py is not endorsed by either of these companies, it is a community-effort to make these two programs interoperable.