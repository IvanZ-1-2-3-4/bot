from random import uniform
from math import sqrt
from sys import argv

if not (len(argv) == 2):
    raise SystemExit('ERROR: enter number of trials')

try: 
    int(argv[1])
except ValueError:
    raise SystemExit('ERROR: you must enter a number')

num_trials = int(argv[1])
inside_circle = 0

for i in range(num_trials):
    x = uniform(0, 1)
    y = uniform(0, 1)
    if sqrt((0.5 - x)**2 + (0.5 - y)**2) <= 0.5:
        inside_circle = inside_circle + 1

print(inside_circle / num_trials * 4)