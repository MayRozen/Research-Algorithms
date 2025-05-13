# Put your code here. You can add files if needed.
from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Dict
import heapq

# =================== Input Interfaces ===================
# Abstract input class for representing a graph.
class GraphInput(ABC):
    # Abstract method that will convert the graph representation to an edge list.
    @abstractmethod
    def to_edge_list(self) -> List[Tuple[int, int, int]]:
        pass


# =================== Input Implementation ===================
# Input as adjacency list: {node: [(neighbor, weight), ...]}.
class AdjacencyListInput(GraphInput):
    def __init__(self, adj_list: Dict[int, List[Tuple[int, int]]]):
        # Initialize with the adjacency list (a dictionary with nodes as keys and a list of tuples as values)
        self.adj_list = adj_list

    def to_edge_list(self) -> List[Tuple[int, int, int]]:
        # Convert the adjacency list to an edge list, where each edge is represented as (u, v, weight)
        edges = set()  # Using a set ensures no duplicate undirected edges
        for u, neighbors in self.adj_list.items():
            for v, w in neighbors:
                if (v, u, w) not in edges:  # Avoid duplicate undirected edges (e.g., both (u, v) and (v, u))
                    edges.add((u, v, w))
        return list(edges)


# Input as weight matrix: a 2D list matrix[i][j] gives the weight of edge i-j.
class WeightMatrixInput(GraphInput):
    def __init__(self, matrix: List[List[int]]):
        # Initialize with a weight matrix
        self.matrix = matrix

    def to_edge_list(self) -> List[Tuple[int, int, int]]:
        # Convert the weight matrix to an edge list
        edges = []
        n = len(self.matrix)  # Number of nodes in the graph
        for i in range(n):
            for j in range(i + 1, n):  # Only considering the upper triangle of the matrix (undirected graph)
                if self.matrix[i][j] != 0:  # If there's an edge (non-zero weight)
                    edges.append((i, j, self.matrix[i][j]))
        return edges


# =================== Output Interfaces ===================
# Design Pattern: Strategy Pattern - for interchangeable output types.
# Abstract output strategy class to extract desired MST result.
class OutputStrategy(ABC):
    @abstractmethod
    def output(self, mst_edges: List[Tuple[int, int, int]]) -> Union[int, List[Tuple[int, int, int]]]:
        pass


# =================== Output Implementation ===================
# Output strategy: return only the total weight of the MST.
class MSTWeightOutput(OutputStrategy):
    def output(self, mst_edges: List[Tuple[int, int, int]]) -> int:
        # Instead of calculating the sum after computing the MST, we can do it in the algorithm
        return sum(w for _, _, w in mst_edges)  # sum the weights of the edges in MST


# Output strategy: return the actual list of edges in the MST.
class MSTEdgesOutput(OutputStrategy):
    def output(self, mst_edges: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        # Return the list of edges in the MST.
        return mst_edges


# =================== Algorithms ===================
# Design Pattern: Strategy Pattern - for interchangeable MST algorithms.

# Abstract MST algorithm class: interface for all MST algorithms.
class MSTAlgorithm(ABC):
    @abstractmethod
    def compute_mst(self, edges: List[Tuple[int, int, int]], n: int) -> List[Tuple[int, int, int]]:
        pass


# Kruskal's algorithm: sort edges and union-find for cycle detection.
class KruskalMST(MSTAlgorithm):
    def compute_mst(self, edges: List[Tuple[int, int, int]], n: int) -> List[Tuple[int, int, int]]:
        # Union-Find data structure for Kruskal's algorithm
        parent = list(range(n))  # Initialize parent for union-find

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # Path compression
                x = parent[x]
            return x

        def union(x, y):
            # Union the sets containing x and y
            xr, yr = find(x), find(y)
            if xr == yr:
                return False
            parent[yr] = xr
            return True

        mst = []
        # Sort edges by weight and process them in increasing order
        for u, v, w in sorted(edges, key=lambda x: x[2]):
            if union(u, v):  # If adding the edge doesn't form a cycle
                mst.append((u, v, w))  # Add to MST
        return mst


# Prim's algorithm: use priority queue to grow MST from a seed node.
class PrimMST(MSTAlgorithm):
    def compute_mst(self, edges: List[Tuple[int, int, int]], n: int) -> List[Tuple[int, int, int]]:
        # Build adjacency list for the graph
        adj = {i: [] for i in range(n)}
        for u, v, w in edges:
            adj[u].append((w, v))
            adj[v].append((w, u))

        visited = [False] * n  # Track visited nodes
        min_heap = [(0, 0, -1)]  # (weight, node, parent)
        mst = []

        # Prim's algorithm using a min-heap (priority queue)
        while min_heap and len(mst) < n - 1:
            w, u, p = heapq.heappop(min_heap)  # Pop node with the smallest edge weight
            if visited[u]:
                continue
            visited[u] = True
            if p != -1:
                mst.append((p, u, w))  # Add edge to MST
            for weight, v in adj[u]:
                if not visited[v]:
                    heapq.heappush(min_heap, (weight, v, u))  # Add neighbors to the heap
        return mst


# =================== System Class ===================
# Design Pattern: Open/Closed Principle - MSTSolver is open to extension, closed to modification.
class MSTSolver:
    def __init__(self, algorithm: MSTAlgorithm, output_strategy: OutputStrategy):
        self.algorithm = algorithm
        self.output_strategy = output_strategy

    def solve(self, graph_input: GraphInput) -> Union[int, List[Tuple[int, int, int]]]:
        edges = graph_input.to_edge_list()  # Convert the graph to an edge list
        nodes = set()
        for u, v, _ in edges:
            nodes.add(u)
            nodes.add(v)
        n = max(nodes) + 1  # Number of nodes in the graph

        # Compute the MST and handle the output based on the chosen strategy
        mst = self.algorithm.compute_mst(edges, n)
        return self.output_strategy.output(mst)  # If the output is MSTEdgesOutput, it will return the edges



def test_all_combinations():
    """
    >>> adj_list = {
    ...     0: [(1, 4), (2, 3)],
    ...     1: [(0, 4), (2, 1), (3, 2)],
    ...     2: [(0, 3), (1, 1), (3, 4)],
    ...     3: [(1, 2), (2, 4)]
    ... }
    >>> matrix = [
    ...     [0, 4, 3, 0],
    ...     [4, 0, 1, 2],
    ...     [3, 1, 0, 4],
    ...     [0, 2, 4, 0]
    ... ]
    >>> inputs = [AdjacencyListInput(adj_list), WeightMatrixInput(matrix)]
    >>> outputs = [MSTWeightOutput(), MSTEdgesOutput()]
    >>> algorithms = [KruskalMST(), PrimMST()]
    >>> results = []
    >>> for inp in inputs:
    ...     for out in outputs:
    ...         for algo in algorithms:
    ...             solver = MSTSolver(algo, out)
    ...             result = solver.solve(inp)
    ...             results.append(result)
    >>> len(results)
    8
    """
    pass


if __name__ == '__main__':
    import doctest

    print(doctest.testmod())
