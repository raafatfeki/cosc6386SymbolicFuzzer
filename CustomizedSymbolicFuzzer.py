from SymbolicFuzzer import SimpleSymbolicFuzzer
from ControlFlow import to_graph, Digraph, gen_cfg

# Redefine initial values to 10 instead of 100
MAX_DEPTH = 10
MAX_TRIES = 10
MAX_ITER = 10

class CustomizedSymbolicFuzzer(SimpleSymbolicFuzzer):
	"""customizedSymbolicFuzzer"""
	def process(self):
		pass

	def options(self, kwargs):
		self.z3 = kwargs.get('solver', self.z3)
		super().options(kwargs)

	def renderCFG(self, graphName="defaultCFG", view=False):
		graph = to_graph(gen_cfg(self.fn_source))
		graph.render(graphName,  view=view)
