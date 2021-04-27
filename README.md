# cosc6386_symbolicFuzzer
This is a project for class cosc6386: A symbolic fuzzer based on "fuzzingbook".
I used **Python 3.8.5**.
 
## Dependencies
* First step is to install the following python packages.
	```
	pip3 install fuzzingbook
	pip3 install z3-solver
	```

* We used the directly the source code from [ControlFlow.py](./ControlFlow.py) and [SymbolicFuzzer.py](./SymbolicFuzzer.py).
PS: you still need to install fuzzingbook and z3-solver.
`Please Do NOT Load SymbolicFuzzer from fuzzingbook but use the local version`

## Examples
Under the example directory there is the following function examples:
1. For simple tasks:
* [check_triangle](./check_triangle.py)
* [gcd](./gcd.py)
2. For booleans operations and expressions
* [boolOnly](./boolOnly.py)
* [evaluateBoolExpression](./evaluateBoolExpression.py)
3. For assignments and paramters that changes inside function
* [copyToEachOther](./copyToEachOther.py)
4. Using realValues
* [realValues](./realValues.py)
5. Using Lists
* [triangle_with_list](./triangle_with_list.py)

In Code, if you want to test for example **triangle_with_list**:
```
from examples.triangle_with_list import triangle_with_list
symbFuzz = CustomizedSymbolicFuzzer(triangle_with_list, max_tries=10, max_depth=10)
symbFuzz.fuzz()
```
or with more atomic functions
```
from examples.triangle_with_list import triangle_with_list
symbFuzz = CustomizedSymbolicFuzzer(triangle_with_list, max_tries=10, max_depth=10)
symbFuzz.renderCFG()
symbFuzz.generatePnodesByDepth()
symbFuzz.generatePathsList()
symbFuzz.solveAllPaths()
symbFuzz.printMapConstrains()
```
