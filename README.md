# Operations Research Library

Published by Zijin Qin (Jin).

This is Jin's code repertory related to the linear programming course (ISE 536) and network optimization course (ISE 632). 

## Most Recent Update

[PS4: Maximum Cut for Tree](./network_ps4/maximum_cut_tree.md)

## Category

Linear Programming

- [Assignment 1 Q1: Investment Problem](./linear_programming/investment_problem/investment.py)
- [Assignment 4 Q8: Mean-Variance Optimization](./linear_programming/mvo_portforlio/mvo_portforlio.py)
- [branch-and-bound in IP](./linear_programming/branch_and_bound/branch_and_bound.py)

Network Flows

- [PS4: Maximum Cut for Tree](./network_optimization/maximize_cut_tree/maximum_cut_tree.md)

## How to run these scripts?

Clone this project: 

```
https://github.com/Jziumo/OperationsResearch-Library.git
```

Create a new virtual environment `venv` in current directory: 

```
python -m venv ./venv/
```

Activate the environment. 

If you are using **Windows**, input this command: 

```
.\venv\Scripts\Activate.ps1
```

If you are using **Linux**, input this command: 

```
source ./venv/bin/activate
```

Then you should see `(venv)` on the left side of your command line. (Not `(base)`!)

Install the libraries used in these scripts. 

```
py -m pip install -r requirements.txt
```