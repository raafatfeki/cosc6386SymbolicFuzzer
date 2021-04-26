from SymbolicFuzzer import AdvancedSymbolicFuzzer, PNode, used_identifiers, identifiers_with_types, define_symbolic_vars, checkpoint, to_single_assignment_predicates, to_src
from ControlFlow import to_graph, Digraph, gen_cfg
import z3

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
        self.pathsList      = list()
        # Default behavior: line of exit is same as enter
        self.fnexit.ast_node.lineno = -1
        self.mapConstrains = dict()
        # Each node defined by its key = (rid, order)
        self.pnodesListall  = {(self.fnenter.rid, 0): PNode(self.fnenter.rid, self.fnenter)}

    def printMapConstrains(self):
        print("Map of constraints to nodes")
        for key, value in self.mapConstrains.items():
            print("Node at line %d: (%s): %s" % \
                (self.pnodesListall[key].cfgnode.lineno(), "False" if key[1] else "True", value))
        print("*************************************************")

    def getConstraintsByNode(self, node):
        return self.mapConstrains[node.idx, node.order]

    def hasConstraints(self, node):
        if (node.idx, node.order) in self.mapConstrains.keys():
            return True
        else:
            return False

    def process(self):
        pass

    def options(self, kwargs):
        self.z3 = kwargs.get('solver', self.z3)
        super().options(kwargs)

    def renderCFG(self, graphName="defaultCFG_", view=False):
        graphName = graphName + self.fn_name
        graph = to_graph(gen_cfg(self.fn_source))
        graph.render(graphName,  view=view)

    # Redefine the function so we can map the constraints to Code by node id
    def extract_constraints(self, path):
        constList = list()
        for idx, p in enumerate(to_single_assignment_predicates(path)):
            if p:
                src_p = to_src(p)
                constList.append(src_p)
                if (path[idx].idx, path[idx].order) not in self.mapConstrains.keys():
                    self.mapConstrains[path[idx].idx, path[idx].order] = src_p
        return constList

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
                    if i:
                        parent_updateOrder = parentPnode.copy(i)
                        self.pnodesListall[(parent_updateOrder.idx, parent_updateOrder.order)] = parent_updateOrder
                    else:
                        parent_updateOrder = parentPnode
                    newNode = PNode(childCfg.rid, childCfg, parent_updateOrder)
                    self.pnodesList[self.level].append(newNode)
                    self.pnodesListall[(newNode.idx, newNode.order)] = newNode
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
            print("Path %d: [%s]" % (idx+1, ", ".join(pathLines)))
            print("List of constraints: ")

            for node in path:
                if(self.hasConstraints(node)):
                    print("\tFrom Node %d: %s" % (node.cfgnode.lineno(), self.getConstraintsByNode(node)))

            print("=> Solution = " , args)
            print("**********************************")

    def fuzz(self):
        self.renderCFG()
        self.generatePnodesByDepth()
        self.generatePathsList()
        self.solveAllPaths()
        self.printMapConstrains()

# TODO:
# If we want to get path by node, we can create dictionary that contains list of all Pnodes
# that have same idx (Same cfg node)
