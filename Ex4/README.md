# Santa Claus Algorithm Implementation

This repository provides a Python implementation of the algorithm described in  
“Santa Claus Meets Hypergraph Matchings” (Asadpour, Feige & Saberi, 2012). It solves the classic *Santa Claus* (max‐min fair‐share) allocation problem by constructing a hypergraph over agents and items, then performing a local‐search to find a perfect matching that maximizes the minimum value any agent receives.

---

## Table of Contents

1. [Overview](#overview)  
2. [Dependencies](#dependencies)  
3. [Installation](#installation)   
4. [Project Structure](#project-structure)  
5. [Testing](#testing)  

---

## Overview

In the *Santa Claus* problem, each agent (child) has a valuation over a set of indivisible items (gifts). The goal is to allocate items so as to maximize the minimum total value any agent receives. This implementation follows the modular outline from the original paper:

1. **Threshold Selection** (binary search over a candidate value _t_).  
2. **Configuration‐LP Relaxation** (solve a linear program to obtain a fractional “bundle” assignment for each agent).  
3. **Item Classification** (classify each item as **fat** or **thin** relative to _t_).  
4. **Hypergraph Construction** (build a bipartite hypergraph whose edges represent feasible bundles of value ≥ _t_).  
5. **Local Search for Perfect Matching** (use alternating‐tree and augmenting‐path ideas to find a perfect matching in the hypergraph).  
6. **Capacity‐Respecting Final Allocation** (greedy assignment respecting agent/item capacities once the optimal threshold is found).

By repeating Steps 1–5 in a binary‐search loop, the algorithm zeroes in on the largest feasible _t_. The final output is an allocation of items to agents that guarantees each agent at least this value.

---

## Dependencies

- **Python 3.8+**  
- **cvxpy** (>= 1.0)  
- **HyperNetX** (for hypergraph data structures)  
- **fairpyx** (custom library providing `Instance`, `AllocationBuilder`, and `validate_allocation`)  
- Standard library modules: `itertools`, `logging`, `typing`

> **Note:**  
> - `fairpyx` is assumed to be installed from a local or internal source (not on PyPI).  
> - Ensure that `cvxpy` and `hypernetx` are available before running the code.

---

## Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/your-organization/santa-claus-hypergraph.git
   cd santa-claus-hypergraph
   ```

2. **(Optional) Create and activate a virtual environment**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # macOS/Linux
   .\.venv\Scripts\activate   # Windows
   ```

3. **Install required packages**  
   ```bash
   pip install cvxpy hypernetx
   ```
   Then install **fairpyx** (if not on PyPI):  
   ```bash
   pip install /path/to/fairpyx
   ```

---

## Project Structure

```
santa-claus-hypergraph/
├── Santa_Algorithm.py      # Main implementation of the Santa Claus algorithm
├── README.md               # This README
├── requirements.txt        # List of Python dependencies
└── tests/
    └── test_santa.py       # Unit tests and doctests
```

- **Santa_Algorithm.py**  
  Contains:
  - `santa_claus_main`: entry point performing binary search and final allocation.
  - `solve_configuration_lp`: solves the configuration‐LP using `cvxpy`.
  - `classify_items`: classifies items into fat/thin based on threshold.
  - `build_hypergraph`: constructs the hypergraph (agents + item bundles).
  - `local_search_perfect_matching`: finds a perfect matching via local search.
  - `parse_allocation_strings`: helper to parse LP output into Python sets.

- **requirements.txt**  
  Pin the following versions (example):
  ```
  cvxpy>=1.0
  hypernetx>=0.2
  fairpyx>=0.1
  ```

- **tests/test_santa.py**  
  Basic doctests and unit tests covering functionality of each module.
---

## Testing

- All core functions include doctests in their docstrings.  
- Run tests with:
  ```bash
  python -m unittest discover tests
  ```
- To manually run doctests:
  ```bash
  python -m doctest -v Santa_Algorithm.py
  ```

---

## License

[Specify your license here—for example, MIT License]

---

## Acknowledgements

- Original paper: **Asadpour, Feige & Saberi**, “Santa Claus Meets Hypergraph Matchings,” STOC 2012.  
- Implementation inspired by `fairpyx` library structure and notation.  
- Thanks to May Rozen for coding and testing.
