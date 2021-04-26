#!/usr/bin/python

# from SymbolicFuzzer import AdvancedSymbolicFuzzer
# from ControlFlow import *
# from graphviz import Source
# import inspect
# import sys
# import os 
from CustomizedSymbolicFuzzer import CustomizedSymbolicFuzzer
from examples.check_triangle import check_triangle
from examples.gcd import gcd
from examples.copyToEachOther import copyToEachOther

# When calling the constructor, we create the cfg using ControlFlow package 
# then we call process() function that create list of paths

# TODO: RAAFAT: max_depth reflect how deep to go into the cfg tree
# Example: if  max_depth=2 means we get level 0,1 and 2 of the tree only.
# In check_triangle, it means only the node with line= 1, 2, 3, 11
# Check the graph you can extract only 4 paths from root
# best solution would be to determine the depth of the cfg that max_depth should be less than it

# symbFuzz = CustomizedSymbolicFuzzer(check_triangle, max_tries=10, max_depth=10)
# fuzz contains all these functions
# symbFuzz.renderCFG()
# symbFuzz.generatePnodesByDepth()
# symbFuzz.generatePathsList()
# symbFuzz.solveAllPaths()
# symbFuzz.printMapConstrains()
# symbFuzz.fuzz()

# symbFuzz = CustomizedSymbolicFuzzer(gcd, max_tries=10, max_depth=10)
# symbFuzz.fuzz()


symbFuzz = CustomizedSymbolicFuzzer(copyToEachOther, max_tries=10, max_depth=10)
symbFuzz.fuzz()

# Our design:
# 1- Redefine get_all_paths function so we can handle the cases where constraints 
# cannot be satisfied and enhance the performance because that functions return duplicates
# 2- User should define the path he wants
# 3- Get that path if defined by user or parse all paths
# 4- Use symbFuzz.solve_path_constraint(newPath.get_path_to_root()) to solve constrainst
# 5- Output is bad, so we need to adjust it
# 6- Look for the other specificity defined in Project Description

