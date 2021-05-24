from json import load, loads
from base64 import decodebytes
from xml.etree.ElementTree import Element, tostring
from os import listdir, getcwd, path
from os.path import isfile, join
from math import sin, cos


def convert_to_fgu(filename, input_path, output_path, portal_width, portal_length):
    with open(join(input_path, f'{filename}.dd2vtt')) as f:
        file = load(f)

    ppg = file['resolution']['pixels_per_grid']
    x_dim = file['resolution']['map_size']['x']
    y_dim = file['resolution']['map_size']['y']

    def parse_string_to_number(string_val):
        if string_val[-1] == '%':
            num = max(ppg * float(string_val[:-1]) / 100, 1) / 2
        elif string_val[-2:] == 'px':
            num = float(string_val[:-2]) / 2
        else:
            raise ValueError("Invalid input")
        return num

    epsilon_w = parse_string_to_number(portal_width)
    epsilon_l = parse_string_to_number(portal_length)

    occular_list = list()

    for figure in file['line_of_sight']:
        wall_dict = dict()
        wall_dict['type'] = 'wall'

        wall_dict['x'] = [coord['x'] for coord in figure]
        wall_dict['y'] = [coord['y'] for coord in figure]

        occular_list.append(wall_dict)

    for door in file['portals']:
        door_dict = dict()

        door_dict['type'] = 'door'

        door_dict['x'] = [coord['x'] for coord in door['bounds']]
        door_dict['y'] = [coord['y'] for coord in door['bounds']]

        door_dict['closed'] = door['closed']
        door_dict['rotation'] = door['rotation']

        occular_list.append(door_dict)

    for occular in occular_list:
        x_trans = [x * ppg - (x_dim * ppg) // 2 for x in occular['x']]
        y_trans = [-y * ppg + (y_dim * ppg) // 2 for y in occular['y']]

        if occular['type'] == 'door':
            epsilon_w_x = epsilon_w * sin(occular['rotation'])
            epsilon_w_y = epsilon_w * cos(occular['rotation'])

            epsilon_l_x = abs(epsilon_l * cos(occular['rotation']))
            epsilon_l_y = abs(epsilon_l * sin(occular['rotation']))

            if x_trans[0] > x_trans[1]:
                x_trans[0] += epsilon_l_x
                x_trans[1] -= epsilon_l_x
            else:
                x_trans[0] -= epsilon_l_x
                x_trans[1] += epsilon_l_x

            if y_trans[0] > y_trans[1]:
                y_trans[0] += epsilon_l_y
                y_trans[1] -= epsilon_l_y
            else:
                y_trans[0] -= epsilon_l_y
                y_trans[1] += epsilon_l_y

            x_trans = [x_trans[0] - epsilon_w_x, x_trans[1] - epsilon_w_x, x_trans[1] + epsilon_w_x,
                       x_trans[0] + epsilon_w_x]
            y_trans = [y_trans[0] - epsilon_w_y, y_trans[1] - epsilon_w_y, y_trans[1] + epsilon_w_y,
                       y_trans[0] + epsilon_w_y]
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

        if object_['type'] == 'door':
            door = Element('door')
            door.text = 'true'
            occluder.append(door)

            close = Element('close')
            close.text = str(object_['closed']).lower()
            occluder.append(close)

        occluders.append(occluder)

    gridsize = Element('gridsize')
    gridsize.text = str(ppg) + ',' + str(ppg)
    root.append(gridsize)

    with open(join(output_path, f'{filename}.xml'), 'wb') as f:
        f.write(tostring(root))

    with open(join(output_path, f'{filename}.png'), 'wb') as f:
        f.write(decodebytes(file['image'].encode('utf-8')))


input_path = getcwd()
output_path = getcwd()
portal_width = '25%'
portal_length = '0px'

if path.exists('config.txt'):
    with open('config.txt') as f:
        config = loads(f.read().replace('\\', '/'))

    if config.get('input_path', '') != '':
        input_path = config['input_path']
    if config.get('output_path', '') != '':
        output_path = config['output_path']
    if config.get('portal_width', '') != '':
        portal_width = config['portal_width']
    if config.get('portal_length', '') != '':
        portal_length = config['portal_width']

dd2vtt_files = [f[:-7] for f in listdir(input_path) if f.endswith('.dd2vtt')]
for filename in dd2vtt_files:
    convert_to_fgu(filename, input_path, output_path, portal_width, portal_length)
