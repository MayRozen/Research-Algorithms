# Santa Claus Algorithm Implementation

This repository provides a Python implementation of the algorithm described in  
“Santa Claus Meets Hypergraph Matchings” (Asadpour, Feige & Saberi, 2012). It solves the classic *Santa Claus* (max‐min fair‐share) allocation problem by constructing a hypergraph over agents and items, then performing a local‐search to find a perfect matching that maximizes the minimum value any agent receives.

---

## Table of Contents

1. [Overview](#overview)  
2. [Dependencies](#dependencies)  
3. [Installation](#installation)   
4. [Project Structure](#project-structure)  
5. [Function Reference](#function-reference)  
6. [Testing](#testing)  

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

## Function Reference

### `santa_claus_main(allocation_builder: AllocationBuilder) -> Dict[str, Set[str]]`
- **Description**: Main entry point. Runs binary search over threshold _t_, constructs hypergraphs, finds perfect matching, and produces final capacity‐respecting allocation.
- **Inputs**:
  - `allocation_builder`: an `AllocationBuilder` instance containing `fairpyx.Instance` with valuations and capacities.
- **Output**: A dictionary mapping each agent to a set of allocated item IDs.
- **Key Steps**:
  1. Build `valuations` matrix from the instance.  
  2. Binary‐search `t` over `[0, min_i sum_i(v)]`.  
  3. Call `is_threshold_feasible` to test if a matching exists for candidate _t_.  
  4. Once optimal _t_ found, perform greedy assignment respecting agent capacities.  

### `is_threshold_feasible(valuations: Dict[str, Dict[str, float]], threshold: float, agent_names: List[str]) -> Tuple[bool, Dict[str, str]]`
- **Description**: Tests if every agent can receive a bundle of items of total value at least _threshold_. Returns a boolean feasibility flag and, if feasible, a matching (agent→edge_name).
- **Inputs**:
  - `valuations`: Nested dictionary of size `[agent][item] → value`.  
  - `threshold`: Candidate value _t_ for each agent.  
  - `agent_names`: List of all agent IDs (strings).
- **Output**: `(feasible: bool, matching: Dict[agent, edge_name])`.  
- **Key Steps**:
  1. Call `solve_configuration_lp` to get a fractional LP assignment.  
  2. Parse LP output via `parse_allocation_strings`.  
  3. Classify items (`fat_items`, `thin_items`) relative to _threshold_.  
  4. Build hypergraph via `build_hypergraph`.  
  5. Attempt local‐search perfect matching via `local_search_perfect_matching`.  
  6. If matching covers all agents, return `(True, matching)`, else `(False, {})`.

### `solve_configuration_lp(valuations: Dict[str, Dict[str, float]], threshold: float) -> Dict[str, str]`
- **Description**: Solves the configuration‐LP (relaxation) for each agent selecting a bundle of items whose total value ≥ _threshold_. Uses `cvxpy`.
- **Inputs**:
  - `valuations`: Nested dictionary `[agent][item] → value`.  
  - `threshold`: Candidate target value _t_.
- **Output**: Dictionary mapping each agent to a string of form `"<x_value>*{item1, item2, ...}"` describing the (fractional) bundle chosen by LP.
- **Key Steps**:
  1. Enumerate all subsets (bundles) of items whose sum of values for agent _i_ ≥ _threshold_.  
  2. Create LP variables `x_{i,S}` for each agent _i_ and bundle _S_.  
  3. Constraints:
     - ∑_{S∈bundles[i]} x_{i,S} ≤ 1  (each agent picks at most one bundle).  
     - ∑_{i: j∈S} x_{i,S} ≤ 1  (each item is used at most once across all bundles).  
  4. Objective: maximize ∑ x_{i,S} (arbitrary, just to find a valid fractional solution).  
  5. Solve with `ECOS` or default solver.  
  6. For each agent, pick the bundle with max `x_{i,S}`.

### `classify_items(valuations: Dict[str, Dict[str, float]], threshold: float) -> Tuple[Set[str], Set[str]]`
- **Description**: Classify every item as **fat** if there exists some agent whose valuation of that item ≥ _threshold_/4; otherwise **thin**.
- **Inputs**:
  - `valuations`: Nested dictionary `[agent][item] → value`.  
  - `threshold`: Target value _t_.
- **Output**: Tuple of two sets: `(fat_items, thin_items)`.
- **Logic**:
  1. For each `item`, compute `max_val = max_{i}(valuations[i][item])`.  
  2. If `max_val ≥ threshold/4`, add to `fat_items`; else to `thin_items`.

### `build_hypergraph(valuations: Dict[str, Dict[str, float]], allocation: Dict[str, List[Set[str]]], fat_items: Set[str], thin_items: Set[str], threshold: float) -> HNXHypergraph`
- **Description**: Build a bipartite hypergraph whose vertices are agent‐IDs and item‐IDs. Each hyperedge represents a feasible bundle of value ≥ _threshold_. Edges are labeled:
  - `"lp*"` for bundles returned by LP.  
  - `"f*"` for each **fat** bundle of size 1 (agent + fat item).  
  - `"t*"` for minimal **thin** bundles (agent + subset of thin items) whose total value ≥ _threshold_.
- **Inputs**:
  - `valuations`: `[agent][item] → value`.  
  - `allocation`: Output of `parse_allocation_strings` (`agent → [set_of_items]`).  
  - `fat_items`, `thin_items`: Sets from `classify_items`.  
  - `threshold`: Candidate _t_.
- **Output**: A `HyperNetX.Hypergraph` instance.  
- **Key Steps**:
  1. Add edges from `allocation` (LP bundles): for each `agent` and `bundle`, create `frozenset({agent} ∪ bundle)`.  
  2. For each `fat_item ∈ fat_items` and each `agent` such that `valuations[agent][fat_item] ≥ threshold`, add edge `{agent, fat_item}`.  
  3. For **thin** items: for each agent and each subset `S ⊆ thin_items`, if `sum(valuations[agent][j] for j∈S) ≥ threshold` **and** minimal (removing any item from `S` drops below _threshold_), add edge `{agent} ∪ S`.  

### `local_search_perfect_matching(H: HNXHypergraph, valuations: Dict[str, Dict[str, float]], players: List[str], threshold: float) -> Dict[str, Set[str]]`
- **Description**: Finds a perfect matching (agent → hyperedge) covering all agents, such that each agent gets a bundle of items of total value ≥ _threshold_. Uses an augmenting‐tree local search.
- **Inputs**:
  - `H`: Hypergraph built by `build_hypergraph`.  
  - `valuations`: `[agent][item] → value`.  
  - `players`: List of agent IDs.  
  - `threshold`: Candidate _t_.  
- **Output**: Dictionary mapping each `agent → set_of_items`. If no perfect matching found, returns a partial mapping (|mapping| < |players|).
- **Algorithm Outline**:
  1. Initialize `matching = {}` (agent→edge_name) and `used_items = set()`.  
  2. For each unmatched `agent`:
     - Build an alternating tree (BFS) starting from `agent`.  
     - In the BFS, explore hyperedges that contain the current player and yield a valid bundle (value ≥ _threshold_).  
     - If a hyperedge’s items are disjoint from `used_items`, augment the matching along the discovered path (update `matching` and `used_items`).  
     - Otherwise, follow overlapping match edges to new players and continue.  
     - If no augmenting edge found, stop.  
  3. Return the agent→item allocation extracted from `matching`.

### `parse_allocation_strings(allocation: Dict[str, str]) -> Dict[str, List[Set[str]]]`
- **Description**: Helper that parses the string‐based LP output (e.g. `"1.0*{'c1', 'c3'}"`) into a Python `Dict[str, List[Set[str]]]`.  
- **Inputs**:
  - `allocation`: Mapping from `agent` to a string like `"1.0*{c1, c3}"`.  
- **Output**: Mapping from `agent` to a list of item‐sets (each `set(str)`). Usually there is at most one bundle per agent from LP.

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
