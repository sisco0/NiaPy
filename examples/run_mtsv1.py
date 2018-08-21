# encoding=utf8
# This is temporary fix to import module from parent folder
# It will be removed when package is published on PyPI
import sys
sys.path.append('../')
# End of fix

import random
import logging
from NiaPy.algorithms.other import MultipleTrajectorySearchV1
from NiaPy.util import TaskConvPrint, TaskConvPlot, OptimizationType, getDictArgs

logging.basicConfig()
logger = logging.getLogger('examples')
logger.setLevel('INFO')

# For reproducive results
class MinMB(object):
	def __init__(self):
		self.Lower = -11
		self.Upper = 11

	def function(self):
		def evaluate(D, sol):
			val = 0.0
			for i in range(D): val = val + sol[i] * sol[i]
			return val
		return evaluate

class MaxMB(MinMB):
	def function(self):
		f = MinMB.function(self)
		def e(D, sol): return -f(D, sol)
		return e

def simple_example(alg, fnum=1, runs=10, D=10, nFES=50000, nGEN=5000, seed=None, optType=OptimizationType.MINIMIZATION, optFunc=MinMB, **kwu):
	for i in range(runs):
		task = Task(D=D, nFES=nFES, nGEN=nGEN, optType=optType, benchmark=optFunc())
		algo = alg(seed=seed, task=task)
		Best = algo.run()
		logger.info('%s %s' % (Best[0], Best[1]))

def logging_example(alg, fnum=1, D=10, nFES=50000, nGEN=5000, seed=None, optType=OptimizationType.MINIMIZATION, optFunc=MinMB, **ukw):
	task = TaskConvPrint(D=D, nFES=nFES, nGEN=nGEN, optType=optType, benchmark=optFunc())
	algo = alg(seed=seed, task=task)
	best = algo.run()
	logger.info('%s %s' % (best[0], best[1]))

def plot_example(alg, fnum=1, D=10, nFES=50000, nGEN=5000, seed=None, optType=OptimizationType.MINIMIZATION, optFunc=MinMB, **kwy):
	task = TaskConvPlot(D=D, nFES=nFES, nGEN=nGEN, optType=optType, benchmark=optFunc())
	algo = alg(seed=seed, task=task)
	best = algo.run()
	logger.info('%s %s' % (best[0], best[1]))
	input('Press [enter] to continue')

def getOptType(strtype):
	if strtype == 'min': return OptimizationType.MINIMIZATION, MinMB
	elif strtype == 'max': return OptimizationType.MAXIMIZATION, MaxMB
	else: return None

if __name__ == "__main__":
	algo = MultipleTrajectorySearchV1
	pargs = getDictArgs(sys.argv[1:])
	optType, optFunc = getOptType(pargs.pop('optType', 'min'))
	if not pargs['runType']: simple_example(algo, optType=optType, optFunc=optFunc, **pargs)
	elif pargs['runType'] == 'log': logging_example(algo, optType=optType, optFunc=optFunc, **pargs)
	elif pargs['runType'] == 'plot': plot_example(algo, optType=optType, optFunc=optFunc, **pargs)

# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
