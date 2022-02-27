#!/bin/env python

from base import NoWar

agents = NoWar.extract_lines('data/agents.txt')
sites = NoWar.extract_lines('data/sites.txt')


if __name__ == '__main__':
	no_war = NoWar(sites, agents)
	no_war.deploy()
