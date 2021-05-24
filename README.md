# draft2fgu
Script to convert LOS data from Dungeondraft's .dd2vtt files to into a usable format for Fantasy Grounds Unity

You can run the file in any directory with .dd2vtt files. It will output a .png file and a .xml file in the same directory. 

## How to use this script:

1. Export your Dungoendraft map in the .dd2vtt format
    - You should turn off Grid in the export as you want FGU to draw the grid, if the GM wishes
2. Place the script/executable in the same folder as your .dd2vtt file (or files)
3. Run the script (just double click on the executable)
4. Voila! Your .png & .xml files have been created and are in the same folder. It will do this for all .dd2vtt files in the folder. 
5. Place these in your "Fantasy Grounds\campaigns\{campaign name}\images" folder and import in FGU as normal.


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