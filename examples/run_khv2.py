# encoding=utf8
# This is temporary fix to import module from parent folder
# It will be removed when package is published on PyPI
import sys
sys.path.append('../')
# End of fix

import random
import logging
from NiaPy.algorithms.basic import KrillHerdV2
from NiaPy.util import TaskConvPrint, TaskConvPlot

logging.basicConfig()
logger = logging.getLogger('examples')
logger.setLevel('INFO')

# For reproducive results
random.seed(1234)

class MyBenchmark(object):
	def __init__(self):
		self.Lower = -11
		self.Upper = 11

	def function(self):
		def evaluate(D, sol):
			val = 0.0
			for i in range(D): val += sol[i] ** 2
			return val
		return evaluate

def simple_example(runs=10, D=10, nFES=50000):
	for i in range(runs):
		algo = KrillHerdV2(D=D, nFES=nFES, n=15, C_a=1, C_r=0.5, benchmark=MyBenchmark())
		best = algo.run()
		logger.info('%s %s' % (best[0], best[1]))

def logging_example(D=10, nFES=50000):
	task = TaskConvPrint(D=D, nFES=nFES, nGEN=10000, benchmark=MyBenchmark())
	algo = KrillHerdV2(task=task, n=15, C_a=1, C_r=0.5)
	best = algo.run()
	logger.info('%s %s' % (best[0], best[1]))

def plot_example(D=10, nFES=50000):
	task = TaskConvPlot(D=D, nFES=nFES, nGEN=10000, benchmark=MyBenchmark())
	algo = KrillHerdV2(task=task, n=15, C_a=1, C_r=0.5)
	best = algo.run()
	logger.info('%s %s' % (best[0], best[1]))
	input('Press [enter] to continue')

if __name__ == '__main__':
	if len(sys.argv) <= 1: simple_example(1)
	elif sys.argv[1] == 'plot': plot_example(D=10 if len(sys.argv) <= 2 else int(sys.argv[2]), nFES=50000 if len(sys.argv) <= 3 else int(sys.argv[3]))
	elif sys.argv[1] == 'log': logging_example(D=10 if len(sys.argv) <= 2 else int(sys.argv[2]), nFES=50000 if len(sys.argv) <= 3 else int(sys.argv[3]))
	else: simple_example(runs=sys.argv[1], D=10 if len(sys.argv) <= 2 else int(sys.argv[2]), nFES=50000 if len(sys.argv) <= 3 else int(sys.argv[3]))

# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
