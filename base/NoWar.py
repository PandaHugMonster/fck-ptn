import logging
import socket
import threading
from random import randrange
from time import sleep

import requests
from requests import ConnectTimeout, ConnectionError, ReadTimeout


class NoWar:

	agents_quantity: int = 10
	sleep_time: float or int = 0.001

	_agents: list = None
	_sites: list = None

	def __init__(self, sites: list, agents: list):
		self._agents = self.prepare_random_agents(agents)
		self._sites = sites

	def prepare_random_agents(self, agents):
		len_agents = len(agents)
		res = []

		for i in range(0, self.agents_quantity):
			rnd_val = randrange(0, len_agents)
			res.append(agents[rnd_val])

		return res

	def query_host(self, host):
		rnd = randrange(0, len(self._agents))
		agent = self._agents[rnd]

		h = {'User-Agent': str(agent)}

		return requests.get(host, headers=h, timeout=5)

	def deploy(self):
		threads = []
		logging.info('## NoWar app deployed')
		for site in self._sites:
			t = threading.Thread(target=self.one_host, args=(site, ))
			threads.append(t)
			t.start()

		for t in threads:
			t.join()

	def one_host(self, host):
		logging.info('Started loop for host: %s', host)
		while True:
			try:
				ip = self.get_ip(host)

				if ip.startswith('127.'):
					logging.info('>> %s | localhost skipped for now (waiting 60s)', host)
					sleep(60)
					continue

				res = self.query_host(host)

				if res.status_code == 200:
					logging.info('Request is ok: %s', host)
				else:
					logging.error('Request is not ok: %s', host)
					if 300 <= res.status_code < 400:
						logging.info('>> %s | redirecting skipped for now (waiting 60s)', host)
						sleep(60)
						continue
					elif 400 <= res.status_code < 500:
						logging.info('>> %s | blocked (waiting 60s)', host)
						sleep(60)
						continue
				logging.info('%s %s', host, res.status_code)
			except ConnectTimeout as e:
				logging.error('>> %s connection timed out / %s', host, e)
			except ConnectionError as e:
				logging.error('>> %s connection error / %s', host, e)
			except ReadTimeout as e:
				logging.error('>> %s read timeout / %s', host, e)
			except Exception as e:
				logging.info('Exception: %s', e)
				break
			sleep(self.sleep_time)
			# break

	def get_ip(self, host):
		host_cleared = str(host).replace('https://', '').replace('http://', '').replace('/', '')
		return socket.gethostbyname(host_cleared)

	def check_hosts(self):
		logging.info('## Checking hosts')
		for host in self._sites:
			try:
				ip = self.get_ip(host)

				if ip.startswith('127.'):
					logging.info('>> %s | localhost skipped', host)
					continue
				try:
					res = self.query_host(host)

					logging.info('>> %s | %s | HTTP %s', host, ip, res)
				except ConnectTimeout as e:
					logging.error('>> %s connection timed out (%s)', host, e)
				except ConnectionError as e:
					logging.error('>> %s connection error (%s)', host, e)
				except ReadTimeout as e:
					logging.error('>> %s read timeout (%s)', host, e)
			except socket.gaierror as e:
				logging.error('>> %s does not exist', host)

	@classmethod
	def extract_lines(cls, file: str):
		res = []
		with open(file, 'rt') as fd:
			for line in fd:
				res.append(line.strip())

		return res

	@classmethod
	def setup_logger(cls):
		logging.basicConfig(level=logging.INFO)
