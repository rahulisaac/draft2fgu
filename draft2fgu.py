#!/usr/bin/env python3

import argparse 
from base64 import decodebytes
from json import load, loads
from math import sin, cos
from os import listdir, getcwd, path
from os.path import isfile, join
from pathlib import Path
import sys
from xml.etree.ElementTree import Element, tostring


def convert_to_fgu(filename, output_path, portal_width, portal_length, args):
    dd2vttPath = Path(filename)

    if args.verbose:
        print(f'Converting {dd2vttPath}')
        
    pngPath = Path.joinpath(output_path, filename.with_suffix('.png').name)
    jpgPath = Path.joinpath(output_path, filename.with_suffix('.jpg').name)
    xmlPath = Path.joinpath(output_path, filename.with_suffix('.xml').name)
    
    if pngPath.exists() and not args.force:
        print(f'Not overwriting {pngPath}', file=sys.stderr)
        return
    if jpgPath.exists() and args.jpeg and not args.force:
        print(f'Not overwriting {jpgPath}', file=sys.stderr)
        return
    if xmlPath.exists() and not args.force:
        print(f'Not overwriting {xmlPath}', file=sys.stderr)
        return

    with dd2vttPath.open(mode='r') as f:
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
            raise ValueError('Invalid input')
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

    if args.verbose:
        print('  {} occluders'.format(len(occluders)))

    with xmlPath.open('wb') as f:
        f.write(tostring(root))

    if args.verbose:
        print(f'  Wrote {xmlPath}')

    with pngPath.open('wb') as f:
        f.write(decodebytes(file['image'].encode('utf-8')))

    if args.verbose:
        print(f'  Wrote {pngPath}')

    if args.jpeg:
        from PIL import Image
        imag = Image.open(pngPath)
        rgb_imag = imag.convert('RGB')
        rgb_imag.save(jpgPath)

        if args.verbose:
            print(f'  Wrote {jpgPath}')

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS] [FILES]',
        description='Convert Dungeondraft .dd2vtt files to .png/.xml for Fantasy Grounds Unity (FGU)'
    )
    parser.add_argument(
        '-f', '--force', help='Force overwrite destination files', action='store_true'
    )
    parser.add_argument(
        '-v', '--verbose', help='Display progress', action='store_true'
    )
    parser.add_argument(
        '--version', action='version', version=f'{parser.prog} version 4.0.0'
    )
    parser.add_argument(
        '-i', '--input', help='Path to the input directory'
    )
    parser.add_argument(
        '--jpeg', '--jpg', help='Write the image as a .jpg file', action='store_true'
    )
    parser.add_argument(
        '-o', '--output', help='Path to the output directory'
    )
    parser.add_argument(
        '--portallength', help='Specify the length of portals'
    )
    parser.add_argument(
        '--portalwidth', help='Specify the width of portals'
    )

    parser.add_argument('files', nargs='*', help="Files to convert to .png + .xml for FGU")
    return parser

def main() -> None:
    input_path = Path.cwd()
    output_path = Path.cwd()
    portal_width = '25%'
    portal_length = '0px'

    configPath = Path('config.txt')
    if configPath.exists():
        with configPath.open(mode='r') as f:
            config = loads(f.read().replace('\\', '/'))

        if config.get('input_path', '') != '':
            input_path = config['input_path']
        if config.get('output_path', '') != '':
            output_path = config['output_path']
        if config.get('portal_width', '') != '':
            portal_width = config['portal_width']
        if config.get('portal_length', '') != '':
            portal_length = config['portal_width']

    parser = init_argparse()
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input)
    if args.output:
        output_path = Path(args.output)
    if args.portalwidth:
        portal_width = args.portalwidth
    if args.portallength:
        portal_length = args.portallength

    if input_path:
        if not input_path.is_dir():
            sys.exit( f'{input_path} is not a directory' )

    if output_path:
        if not output_path.is_dir():
            sys.exit( f'{output_path} is not a directory' )

    dd2vtt_files = []

    if args.files:
        for f in args.files:
            if not output_path:
                # Filename was specified, but no output_path
                dd2vtt_files.append( (Path(f), Path(f).parent) )
            else:
                # Filename was specified and an output_path
                dd2vtt_files.append( (Path(f), output_path))
    else:
        for f in input_path.iterdir():
            if f.suffix == '.dd2vtt':
                # Filename found in the input_path, send to the output_path
                dd2vtt_files.append( (f, output_path) )

    for filename, fileOutputPath in dd2vtt_files:
        convert_to_fgu(filename, fileOutputPath, portal_width, portal_length, args)

if __name__ == '__main__':
    main()