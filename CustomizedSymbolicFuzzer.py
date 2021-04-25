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
        self.pnodesListall  = [PNode(self.fnenter.rid-1, self.fnenter)]
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
                for childCfg in parentPnode.cfgnode.children:
                    if(childCfg.rid in parsedCfgNodes):
                        continue
                    self.nbNodes = self.nbNodes + 1
                    newNode = PNode(childCfg.rid-1, childCfg, parentPnode)
                    self.pnodesList[self.level].append(newNode)
                    self.pnodesListall.append(newNode)
                    parsedCfgNodes.append(childCfg.rid)
            self.level = self.level + 1
        # self.pnodesList[-1].append()self.fnexit
        print("We have %d levels and %d nodes" % (self.level, self.nbNodes))
        print(len(self.pnodesListall))
        # print(self.pnodesList)
        return self.pnodesListall

    def generatePathsList(self, entryLevel=-1, exitLevel=1000):
        # Raafat: We need to check entryLevel and exitLevel are within the limits
        # Raafat: we can adjust the code such we can get path not only from node to root
        if entryLevel < 1:
            entryLevel = 1
        if exitLevel > self.level:
            exitLevel = self.level
        for level in range(entryLevel, exitLevel):
            for pNode in self.pnodesList[level-1]:
                self.pathsList.append(pNode.get_path_to_root())

    def solveAllPaths(self):
        for idx, path in enumerate(self.pathsList):
            print("*********************")
            pathStr = "Path %d: " % (idx+1)
            for node in path:
                pathStr = (pathStr + "L%s -> " %  str(node.cfgnode.lineno()))
            args = self.solve_path_constraint(path)
            print(pathStr, ": ", args)
            print("*********************")

