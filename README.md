# cosc6386_symbolicFuzzer
This is a project for class cosc6386: A symbolic fuzzer based on "fuzzingbook".
I used **Python 3.8.5**.
 
## Dependencies
* First step is to install the following python packages.
	```
	pip3 install fuzzingbook
	pip3 install z3-solver
	```

* We used the directly the source code from [ControlFlow.py](./ControlFlow.py) and [SymbolicFuzzer.py](./SymbolicFuzzer.py) instead of installing it because we might need to make new changes.

## Examples
Under the example directory there is the following function examples:
* [check_triangle](./check_triangle.py)
* [gcd](./gcd.py)
