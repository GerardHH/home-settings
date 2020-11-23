#! /usr/bin/python3

from os.path import exists
from uuid import UUID
from sys import stderr, stdout
from typing import Dict, List, Tuple, Union
import argparse
import json


__json_object = Union[Dict, List]
__json_type = Union[bool, Dict, float, int, List, str]


def __add_segment_to_tree(segment: str, field: str, file: str, tree: List, verbose: bool = False) -> List:
    ''' Add a segment to tree with field references found in file and return the tree.'''
    if verbose:
        print('Adding {} segment'.format(segment))
    object = __load_json(file=file)
    found_objects = []
    for object in __find(object=object, attr_value=field, verbose=verbose):
        found_objects.append(object)
    if found_objects:
        tree[segment] = found_objects
    else:
        print('Did not find any "{}" for field "{}"'.format(segment, field), file=stderr)
    return tree


def __bracketed_uuid(uuidStr: str) -> str:
    '''Convert uuidStr to a UUID and return it surrounded with brackets. Raise ArgumentjTypeError when uuidStr cannot be converted to a UUID.'''
    try:
        return '{{{uuid}}}'.format(uuid=UUID(uuidStr))
    except Exception as e:
        raise argparse.ArgumentTypeError(uuidStr + ' is not a valid UUID: ' + str(e))


def __existing_path(path: str) -> str:
    ''' Check if path exists and return it, raise ArgumentTypeError otherwise.'''
    if exists(path):
        return path
    raise argparse.ArgumentTypeError(path + ' does not exist')


def __find(object: __json_type, attr_value: str, verbose: bool, __keyBeingSearched: str = None) -> Dict:
    ''' Find attr_value and yield the Dict that contains it.'''
    if verbose:
        print('-'*10)
        print('Searching for attribute: "{}" in {}'.format(attr_value, object))
    if isinstance(object, dict):
        for key, value in object.items():
            if isinstance(value, dict) or isinstance(value, list):
                yield from __find(value, attr_value, verbose, key)
            elif str(value).lower() == attr_value.lower():
                yield {__keyBeingSearched: object} if __keyBeingSearched else object

    elif isinstance(object, list):
        for element in object:
            if isinstance(element, dict) or isinstance(element, list):
                yield from __find(element, attr_value, verbose, __keyBeingSearched)


def __load_json(file: str) -> __json_object:
    '''Load JSON file into memory as python objects. Raises RuntimeError when the decoding fails.'''
    try:
        with open(file) as jsonFile:
            return json.load(jsonFile)
    except json.decoder.JSONDecodeError as e:
        raise RuntimeError('Could not decode {}: {}'.format(file, str(e)))


def builddbtree(field: str, gfffile: str = None, jobfile: str = None, opplanningfile: str = None, scoutfile: str = None, name: str = None, verbose: bool = False) -> None:
    ''' Write field JSON database that contains all references to a field.

    Parameters:
    - field:            The bracketed UUID of the field. This value will be used to find to references to the field.
    - gfffile:          The location of the GFF JSON database that will be searched for references.
    - jobfile:          The location of the job JSON database that will be searched for references.
    - opplanningfile:   The location of the operation planning JSON database that will be searched for references.
    - scoutfile:        The location of the scout JSON database that will be searched for references.
    - name:             The name of the new database tree that will be writen to disk. If not given the new tree will receive the UUID as a name.
    - verbose:          Whether intermediate steps should be printed (true) or not (false). Cation: This will make the script spell out its search steps, which can result in a lot of logging.
    '''
    result = {}
    gffJson = __load_json(file=gfffile)
    try:
        result['field'] = next(__find(object=gffJson, attr_value=field, verbose=verbose))
    except StopIteration:
        raise KeyError('Could not find "{}" in "{}"'.format(field, gfffile))

    result = __add_segment_to_tree(segment='jobs', field=field, file=jobfile, tree=result)
    result = __add_segment_to_tree(segment='operation plans', field=field, file=opplanningfile, tree=result)
    result = __add_segment_to_tree(segment='scouted objects', field=field, file=scoutfile, tree=result)

    with open(name if name else field, 'w') as file:
        json.dump(result, file, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print a given field expanded, where all references to a field are placed as children under the field')
    parser.add_argument('-g', '--gfffile', default='GFF.json', type=__existing_path, help='Path to the GFF database (default: %(default)s).')
    parser.add_argument('-j', '--jobfile', default='job.json', type=__existing_path, help='Path to the job database (default: %(default)s).')
    parser.add_argument('-n', '--name', help='The name of the file that will be written (default: the field number)')
    parser.add_argument('-o', '--opplanningfile', default='OpPlanning.json', type=__existing_path, help='Path the to operation planning database (default: %(default)s).')
    parser.add_argument('-s', '--scoutfile', default='scout.json', type=__existing_path, help='Path the the scout database (default: %(default)s).')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output.')
    parser.add_argument('field', type=__bracketed_uuid, help='UUID of a field used as an argument for finding dependencies.')
    args = parser.parse_args()
    builddbtree(**args.__dict__)

# 06967065-e512-4fa9-8ef7-5f5b00bb5a7c
