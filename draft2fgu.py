from json import load
from base64 import decodebytes
from xml.etree.ElementTree import Element, tostring
from os import listdir
from os.path import isfile, join

def convert_to_fgu(filename):
    with open(f'{filename}.dd2vtt') as f:
        file = load(f)
        
    ppg = file['resolution']['pixels_per_grid']
    x_dim = file['resolution']['map_size']['x']
    y_dim = file['resolution']['map_size']['y']

    occular_list = list()

    for figure in file['line_of_sight']:
        wall_dict = dict()
        wall_dict['x'] = [coord['x'] for coord in figure]
        wall_dict['y'] = [coord['y'] for coord in figure]
        
        occular_list.append(wall_dict)
        
    for door in file['portals']:
        door_dict = dict()
        
        door_dict['x'] = [coord['x'] for coord in door['bounds']]
        door_dict['y'] = [coord['y'] for coord in door['bounds']]
        
        door_dict['closed'] = door['closed'] 
        occular_list.append(door_dict)

    for occular in occular_list:
        x_trans = [x*ppg - (x_dim*ppg)//2 for x in occular['x']]
        y_trans = [-y*ppg + (y_dim*ppg)//2 for y in occular['y']]
        
        occular['coords'] = [a for item in zip(x_trans, y_trans) for a in item]
        
    root = Element('root')
    occluders = Element('occluders')
    root.append(occluders)

    for id_, object_ in enumerate(occular_list):
        occluder = Element('occluder')
        
        id_number = Element('id')
        id_number.text = str(id_)
        occluder.append(id_number)
        
        points = Element('points')
        points.text = ','.join(str(o) for o in object_['coords'])
        occluder.append(points)

        if 'closed' in object_:
            door = Element('door')
            door.text = 'true'
            occluder.append(door)
            
            close = Element('close')
            close.text = str(object_['closed']).lower()
            occluder.append(close)
            
        occluders.append(occluder)

    with open(f'{filename}.xml', 'wb') as f:
        f.write(tostring(root))
        

    with open(f'{filename}.png','wb') as f:
        f.write(decodebytes(file['image'].encode('utf-8')))


dd2vtt_files = [f[:-7] for f in listdir() if f.endswith(".dd2vtt") ]
for filename in dd2vtt_files:
    convert_to_fgu(filename)
