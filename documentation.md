# Technical approach

Database Problem
        ↓
Mathematical Optimization Problem
        ↓
Quantum Optimization Problem
        ↓
Quantum Circuit
        ↓
Solution
        ↓
Compare with Classical Database Optimizer

# Phase By Phase Plan

# Phase 1: Classical Baseline (Database Optimizer)

- **Goal : What is the best join order using traditional database techniques ?**

## The Problem

Suppose we have:
customer
JOIN orders
JOIN lineitem
JOIN supplier
JOIN nation

- The database must decide :
Option A:
(customer ⋈ orders)
      ⋈ lineitem
      ⋈ supplier
      ⋈ nation
    OR
Option B:
(supplier ⋈ nation)
      ⋈ lineitem
      ⋈ orders
      ⋈ customer

- hundereds of possibilities

## Why Does Order matter?

Suppose:
customer = 150,000 rows
orders   = 1,500,000 rows
Joining these first may produce:

1,500,000 rows

But joining:
supplier = 10,000
nation   = 25

first may produce:
10,000 rows
Much smaller.

Smaller intermediate tables:
Less memory
Less CPU
Faster execution

## What Selinger DP does?

- Selinger DP is essentially:
Try all possibilities intelligently
instead of brute force

Example: For 3 tables - A, B, C
Possible Orders:
(A⋈B)⋈C
(A⋈C)⋈B
(B⋈C)⋈A
- DP stores best partial solutions.

Instead of recomputing:
Best way to join A,B
100 times,
it computes once and remembers.

This is:
Dynamic Programming

## Output of Phase 1
Best Join Order

Cost

Runtime

Phase 1
↓
Build Classical Optimizer
↓
Verify Results
↓
Build QUBO
↓
Verify QUBO
↓
Build Hamiltonian
↓
Verify Hamiltonian
↓
Build QAOA
↓
Run Experiments

## Step 1: Project Structure
qaoa_join_optimization/
│
├── data/
│
├── classical/
│   ├── join_graph.py
│   ├── cost_model.py
│   └── selinger_dp.py
│
├── quantum/
│   ├── qubo_builder.py
│   ├── hamiltonian.py
│   └── qaoa_solver.py
│
├── experiments/
│
├── results/
│
└── main.py

## Step 2: Build join Graph module
Purpose
This file stores all database information.

## Step 3: Build Cost Model
This is the heart of query optimization.

We need:
∣A⋈B∣=∣A∣×∣B∣×f

Example

customer = 150000
orders = 1500000
selectivity = 1/150000

Then:
150000 × 1500000 × (1/150000)
=
1500000
rows.

## Step 4: Verify Cost Model

- Test: customer, supplier, supplier+nation

## Step 5: main.py
===== SELINGER DP RESULT =====

Optimal Join Order:

nation -> supplier -> lineitem -> orders -> customer

Estimated Cost:
18,013,670.00

Runtime:
0.477 ms


## Step 6: Refinements
1. Add operation counter
2. Print the DP table: so that we can see DP is exploring subsets correctly

3. Scaling Experiment : experiments/scaling.py
Run the DP for N = 3,4,5,6,7,8
Collecting - N, Runtime, Operations

- These are the classical measurements firstt, which we'll be comparing to the QAOA later

===========================================================
SCALING RESULTS

N=3 | Ops=30 | Time=0.047 ms
N=4 | Ops=152 | Time=0.109 ms
N=5 | Ops=650 | Time=0.445 ms
N=6 | Ops=2532 | Time=1.782 ms
N=7 | Ops=9310 | Time=7.320 ms
N=8 | Ops=32944 | Time=28.703 ms

Raw Results:
[(3, 30, 0.04660000013245735), (4, 152, 0.10879999990720535), (5, 650, 0.4451999998309475), (6, 2532, 1.7822000002070126), (7, 9310, 7.319999999936044), (8, 32944, 28.703400000040347)]

===========================================================

# Phase 2: 

Until now:
Database Problem
      ↓
Classical Optimizer

Now: 
Database Problem
      ↓
QUBO Formulation
      ↓
Quantum Optimization Problem

## What exactly we are building
Suppose we have 5 tables:
customer
orders
lineitem
supplier
nation

A join order is:
customer
orders
lineitem
supplier
nation

or

nation
supplier
lineitem
orders
customer

or any other permutation.

- How many possibilities: for 5 tables:  5! = 120

- The quantum computer cannot understand:customer, orders,lineitem

- It only understands:
0
1
0
1
1

- Join order -> Binary Variable -> QUBO

- Our Encoding
we wil use:
**x(i,j)**
meaning:
**Table i is placed at position j.**

Example:
for 3 tables:
A, B, C
Positions:
0, 1, 2
Varibales:
x(A,0)
x(A,1)
x(A,2)

x(B,0)
x(B,1)
x(B,2)

x(C,0)
x(C,1)
x(C,2)

Total: 3x3 = 9 varibales

For our problem: 25 binary variables

## What does a valid solution looks like?
nation
supplier
lineitem
orders
customer

Binary matrix:

             Pos0 Pos1 Pos2 Pos3 Pos4

customer       0    0    0    0    1
orders         0    0    0    1    0
lineitem       0    0    1    0    0
supplier       0    1    0    0    0
nation         1    0    0    0    0

This is exactly what QAOA will optimize over.

- Constarint 1: Eveery table appears once
- Constrtaint 2: Every position contains exactly one table
- Constraint 3: Join cost
We want:
good join orders
↓
low energy

and

bad join orders
↓
high energy

## Result
The QUBO becomes:

**Q=Ctable​+Cposition​+Cjoin​**

## Update main.py
Finally updated the ***main.py***

For our 5 table TPC-H problem:
Total Variables = 25 
- Verified

## Building the first actual QUBO matrix
Moving from Variable Creation -> Optimization Problem

## Mathematical Constraint 1
**For each table: (j∑​xi,j​−1)^2**

-This expression becomes: 0 , when customer appears exactly once.
- It becomes positive penalty: when customer appers 0,1,2... times

**Why QUBO?**
A QUBO is: xTQx
- So we need a matrix: Q (that contains all the penalties)

- Output
Q shape = (25,25)
25 variables
↓
25×25 QUBO Matrix

## Mathematical Constraint 2
Each position contains exactly one table
**(i∑​xi,j​−1)^2**

Example

Position 0: (xcustomer,0​+xorders,0​+xlineitem,0​+xsupplier,0​+xnation,0​−1)^2

If exactly one table occupies Position 0:
Penalty = 0

If two tables occupy Position 0:
Penalty > 0

If no table occupies Position 0:
Penalty > 0

- Output
===== QUBO SUMMARY =====
Variables: 25
Matrix Shape: (25, 25)
Non-Zero Entries: 125
Min Value: -20.0
Max Value: 20.0

- At this stage: All valid join orders have the same energy
Because: We haven't added Join Cost yet

- The QUBO currently knows:
valid
vs
invalid
but not:
good
vs
bad

## Cost Encoding
We need:
Good Join Order
↓
Low Energy

Bad Join Order
↓
High Energy

- We encode cardinality-based cost

- Idea:
 if a table appears early:
        cost += cardinality
weighted by position


===== QUBO SUMMARY =====
Variables: 25
Matrix Shape: (25, 25)
Non-Zero Entries: 125
Min Value: -19.99975
Max Value: 280.06075000000004

Sample Diagonal Entries:
Q[0,0] = -18.5000
Q[1,1] = -17.0000
Q[2,2] = -15.5000
Q[3,3] = -14.0000
Q[4,4] = -12.5000
Q[5,5] = -5.0000
Q[6,6] = 10.0000
Q[7,7] = 25.0000
Q[8,8] = 40.0000
Q[9,9] = 55.0000

- Now the QUBO finally distinguishes between good & bad join orders

## Join selectivity cost
Before:
Q =
Constraints
+
Cardinality Cost

After:
Q =
Constraints
+
Cardinality Cost
+
Join Selectivity Cost

