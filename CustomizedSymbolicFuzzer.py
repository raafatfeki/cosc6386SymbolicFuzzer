from SymbolicFuzzer import AdvancedSymbolicFuzzer, PNode
from ControlFlow import to_graph, Digraph, gen_cfg

# Redefine initial values to 10 instead of 100
MAX_DEPTH = 10
MAX_TRIES = 10
MAX_ITER = 10

class CustomizedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    """customizedSymbolicFuzzer"""
    def __init__(self, fn, **kwargs):
        super(CustomizedSymbolicFuzzer, self).__init__(fn, **kwargs)
        # For each level(max defined by depth), 
        # we create pnode representing each node in that level.
        # Level 0: Is the root node
        # it is a list of list such as, element 2 will be the list of nodes in level 2. 
        self.pnodesList     = [[PNode(self.fnenter.rid, self.fnenter)]]
        self.level          = 1
        self.nbNodes        = 1
        self.pnodesListall  = [PNode(self.fnenter.rid, self.fnenter)]
        self.pathsList      = list()

    def process(self):
        pass

    def options(self, kwargs):
        self.z3 = kwargs.get('solver', self.z3)
        super().options(kwargs)

    def renderCFG(self, graphName="defaultCFG", view=False):
        graph = to_graph(gen_cfg(self.fn_source))
        graph.render(graphName,  view=view)

    def generatePnodesByDepth(self, fenter=None):
        if(fenter is None):
            fenter = self.fnenter
        parsedCfgNodes = list()
        while (self.level < self.max_depth):
            if(not self.pnodesList[self.level - 1]):
                break
            self.pnodesList.append(list())
            for parentPnode in self.pnodesList[self.level - 1]:
                for (i, childCfg) in enumerate( parentPnode.cfgnode.children):
                    # if(childCfg.rid in parsedCfgNodes):
                    #     continue
                    self.nbNodes = self.nbNodes + 1
                    parent_updateOrder = parentPnode.copy(i) if i else parentPnode
                    newNode = PNode(childCfg.rid, childCfg, parent_updateOrder)
                    self.pnodesList[self.level].append(newNode)
                    self.pnodesListall.append(newNode)
                    parsedCfgNodes.append(childCfg.rid)
            self.level = self.level + 1

        if (not self.pnodesList[-1]):
            del self.pnodesList[-1]
            self.level = self.level - 1
        return self.pnodesListall

    def generatePathsList(self, entryLevel=-1, exitLevel=1000):
        # Raafat: we can adjust the code such we can get path not only from node to root
        if entryLevel < 1:
            entryLevel = 1
        if exitLevel > self.level:
            exitLevel = self.level + 1
        for level in range(entryLevel, exitLevel):
            for pNode in self.pnodesList[level-1]:
                self.pathsList.append(pNode.get_path_to_root())

    def solveAllPaths(self):
        for idx, path in enumerate(self.pathsList):
            pathLines = list()
            for node in path:
                pathLines.append(str(node.cfgnode.lineno()))
            args = self.solve_path_constraint(path)
            pathStr = "Path %d: [%s] => \tSolution=%s" % (idx+1, ", ".join(pathLines), args)
            print(pathStr)
            print("**********************************")


# TODO:
# If we want to get path by node, we can create dictionary that contains list of all Pnodes
# that have same idx (Same cfg node)
