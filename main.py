#!/bin/env python
from argparse import ArgumentParser, Namespace

from base import NoWar

# agents = NoWar.extract_lines('data/agents.txt')
agents = NoWar.extract_lines('data/agents.txt')
sites = NoWar.extract_lines('data/sites-new.txt')
no_war = NoWar(sites, agents)
NoWar.setup_logger()


def deploy(args: Namespace):
	no_war.deploy()


def check_targets(args: Namespace):
	no_war.check_hosts()


if __name__ == '__main__':
	parser = ArgumentParser()
	subs = parser.add_subparsers()

	p = subs.add_parser('deploy')
	p.set_defaults(func=deploy)

	p = subs.add_parser('check')
	p.set_defaults(func=check_targets)

	args = parser.parse_args()
	if hasattr(args, 'func'):
		args.func(args)
	else:
		parser.print_help()
