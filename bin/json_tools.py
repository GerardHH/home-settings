#!/usr/bin/python3

from collections.abc import Mapping
from os import getcwd
from shutil import copyfile
from sys import argv, stderr, stdout
import argparse
import json
import os.path

# TODO: Add check if json is installed and report error if it isn't
# TODO: Multiple objects for --add? Now it results in a cryptic error
# TODO: Add search on attribute in JSON list for --query
# TODO: Add check if file is readable JSON
# TODO: Document arguments of functions


def __add(object, addition, verbose):
    '''Add addition JSON object to abject.'''
    __verbose_print('Adding to object', verbose)
    if isinstance(object, Mapping):
        object.update(addition)
    if isinstance(object, list):
        object.append(addition.copy())
    __verbose_print(object, verbose, False)


def __backup(path, verbose):
    '''Backup path by appending .backup to path.'''
    verbose_print('Backing up', verbose)
    backup_path = '{}.backup'.format(path)
    __verbose_print(path, verbose, False)
    __verbose_print(backup_path, verbose, False)
    if not os.path.exists(backup_path):
        copyfile(path, backup_path)
    else:
        print('Backup already exists, ignoring...')


def __is_valid_file(path):
    '''Check if path is a valid path to file.'''
    if os.path.isfile(path):
        return path
    raise argparse.ArgumentTypeError(path + ' is not a valid path')


def __is_valid_json(string):
    ''' Check if string is a valid JSON. '''
    return json.loads(string)


def __is_valid_query(string):
    ''' Check if string is a valid point saperated query and return it. '''
    return string.split('.')


def __print_object(object, verbose):
    '''Print JSON or value.'''
    __verbose_print('Printing object', verbose)
    json.dump(object, stdout, indent=4)
    print('') # For some reason following prints will mess with the json.dump but printing a new line seems to fix it.


def __query(root, query_list, verbose):
    '''Query object based on query_list.'''
    __verbose_print('Querying object', verbose)
    object = root
    for query in query_list:
        object = object[query if not query.isdigit() else int(query)]
        __verbose_print(query, verbose, False)
        __verbose_print(object, verbose, False)
    return object


def __verbose_print(printable, verbose, heading=True):
    '''Print if verbose is true in the form of --- printable --- if heading is True, without the - if heading is False.'''
    if verbose:
        if heading:
            print('--- {} ---'.format(printable), file=stderr)
        else:
            print(printable, file=stderr)


def json_tools(file, add=None, backup=False, print_result=False, query=None, verbose=False, write=False):
    ''' Execute JSON tools dependant on enabled features.
    add - should be dict/list (JSON)
    query - should be list of strings
    '''
    if backup:
        __backup(path=file, verbose=verbose)
    root = {}
    with open(file, 'r') as json_file:
        __verbose_print('Loading file to object', verbose)
        root = json.load(json_file)
    object = root if not query else __query(root=root, query_list=query, verbose=verbose)
    if add:
        __add(object=object, addition=add, verbose=verbose)
    if print_result:
        __print_object(object=object, verbose=verbose)
    if write:
        __verbose_print('Writing object to file', verbose)
        with open(file, 'w') as json_file:
            json.dump(root, json_file, indent=4)
    else:
        print('Did not write to file, use --write to file', file=stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line JSON tools.')
    parser.add_argument('file', type=__is_valid_file, help='Path to target.')
    parser.add_argument('-a', '--add', type=__is_valid_json, help='Add JSON object(s) to existing object/list in the form of `{"key":"value}`. Can be used to overwrite attributes by adding a key with the same name.')
    parser.add_argument('-b', '--backup', action='store_true', help='Write a backup of file by appending .backup. If a backup already exist, then this step is skipped.')
    parser.add_argument('-p', '--print_result', action='store_true', help='Print JSON file to stdout. In case of --query, will print the query result.')
    parser.add_argument('-q', '--query', type=__is_valid_query, help='Query an object in the form of `key.index.key` starting from root, Default = root.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print intermediate steps.')
    parser.add_argument('-w', '--write', action='store_true', help='Write JSON in place.')
    args = parser.parse_args()
    json_tools(**args.__dict__)
