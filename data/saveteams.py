import tbapy
from tqdm import trange
import yaml

tba = tbapy.TBA('')


allteams = {}
for team in trange(10000):
	try:
		allteams[team] = str(team) + " - " + tba.team(team).nickname
	except AttributeError:
		continue

with open('teams.yaml', 'w') as t:
	yaml.dump(allteams, t)

