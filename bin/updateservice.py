#!/usr/bin/python3

from subprocess import CalledProcessError, TimeoutExpired, run
from sys import stderr, stdout
import argparse
import os.path

__suported_modes = ('start', 'stop', 'restart')


def __ip_exists(ip: str) -> str:
    ''' Checks if ip can be reached. '''
    try:
        run(['ping', '-c', '1', ip], check=True)
    except (CalledProcessError, TimeoutExpired):
        raise argparse.ArgumentTypeError(ip + ' could not be reached')
    return ip


def __path_exists(path: str) -> str:
    ''' Checks if path exists on disk. '''
    if os.path.exists(path=path):
        return path
    raise argparse.ArgumentTypeError(path + ' does not exists')


def __remote_cpro(mode: str, remote: str):
    ''' Send mode to /etc/init.d/cpro found in remote. '''
    if not mode in __suported_modes:
        raise NotImplementedError(mode + ' not supported, supported modes: ' + __suported_modes)
    run(['ssh', remote, '/etc/init.d/cpro', mode], check=True)


def __transfer_service(path: str, remote: str, remote_path: str):
    ''' Transfer path using rsync to remote in remote_path. '''
    run(['rsync', '-avz', path, '{}:{}'.format(remote, remote_path)], check=True)


def __update_service(path: str, remote_path: str, remote_ip: str, remote_user: str = 'root'):
    ''' Stop cpro found in remote_ip, transfer service to remote_ip in remote_path and start cpro. '''
    remote = '{}@{}'.format(remote_user, remote_ip)
    __remote_cpro(mode='stop', remote=remote)
    __transfer_service(path=path, remote=remote, remote_path=remote_path)
    __remote_cpro(mode='start', remote=remote)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stop the CPRO system, update the service and start the CPRO system again.')
    parser.add_argument('--remote-user', default='root', help='The user used to login to the remote device, default: root.')
    parser.add_argument('path', type=__path_exists, help='The executable to be updated.')
    parser.add_argument('remote_path', help='The path on the target device where the service should be copied to.')
    parser.add_argument('remote_ip', type=__ip_exists, help='IP address of the remote device.')
    args = parser.parse_args()
    __update_service(path=args.path, remote_path=args.remote_path, remote_ip=args.remote_ip, remote_user=args.remote_user)
