#! /usr/bin/python3

from os import chdir, system
import argparse
import env

chdir(env.CRX)

parser = argparse.ArgumentParser(description='Sync the whole project')
parser.add_argument('-n', '--no-sync', action='store_true', help='Skip syncing all the repo\'s')
parser.add_argument('-d', '--dry-run', action='store_true', help='Only show the command that will be executed')
parser.set_defaults(branch=None, tag=None, reset=None) # Hack to be able to check them
subparsers = parser.add_subparsers(title='Modes', description='Used to checkout either a branch or tag')

parser_branch = subparsers.add_parser('branch', help='Checkout a branch after syncing')
parser_branch.add_argument('-b', '--branch', default='master', help='The branch to checkout, default: master')
parser_branch.add_argument('-r', '--reset', action='store_true', help='Execute git reset --hard cpro-gitlab/$branch')

parser_tag = subparsers.add_parser('tag', help='Checkout a tag after syncing')
parser_tag.add_argument('tag', help='The tag to checkout')

args = parser.parse_args()

if not args.branch and not args.tag:
    parser.error('Either branch or tag mode are required')

command = '{sync}{repo} forall -c "git checkout {commit}{reset}"'.format(
    sync='{repo} sync --fetch-submodules && '.format(repo=env.REPO) if not args.no_sync else '',
    repo=env.REPO,
    commit=args.branch if args.branch else args.tag,
    reset=' && git reset --hard cpro-gitlab/{}'.format(args.branch) if args.reset else ''
    )

if args.dry_run:
    print(command)
else:
    system(command)
