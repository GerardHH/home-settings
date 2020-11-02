#! /usr/bin/python3

from os import chdir
from subprocess import run
import argparse
import env


def __checkout(branch: str = 'master', tag: str = None, abort_on_errors: bool = False, pager: bool = False):
    ''' Checkout branch/commit in every repo in CRx. Fast forward merge to ${git remote}/branch if applicable'''
    git_command = 'git checkout {commit}{merge_command}'.format(
        commit=branch if not tag else tag,
        merge_command=' && git merge $(git remote)/{}'.format(branch) if not tag else '')
    run([env.REPO, 'forall', '{}'.format('--abort-on-errors' if abort_on_errors else ''), '{}'.format('-pv' if pager else ''), '--command', '{}'.format(git_command)], check=True)


def __sync():
    ''' Download sources and submodules from server. '''
    run([env.REPO, 'sync', '--prune', '--fetch-submodules'], check=True)


def __update_submodules(abort_on_errors: bool = False):
    ''' Update all submodules in CRx. '''
    run([env.REPO, 'forall', '{}'.format('--abort-on-errors' if abort_on_errors else ''), '--command', 'git submodule update --init --recursive'], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sync the whole CRx project')
    parser.add_argument('-a', '--abort-on-errors', action='store_true', help='Exit subcommands when an error is encountered')
    parser.add_argument('-s', '--skip-sync', action='store_true', help='Skip the download from server step and only execute the checkout (and potential merge)')
    parser.add_argument('-p', '--pager', action='store_true', help='Show pager with per repo verbose output for checkout step')
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument('-b', '--branch', default='master', help='The branch to checkout after the sync, default: master')
    exclusive_group.add_argument('-t', '--tag', help='The tag to checkout after the sync')

    args = parser.parse_args()

    chdir(env.CRX)

    if not args.skip_sync:
        __sync()
    __checkout(branch=args.branch, tag=args.tag, abort_on_errors=args.abort_on_errors, pager=args.pager)
    __update_submodules(abort_on_errors=args.abort_on_errors)
