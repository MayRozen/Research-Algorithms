import numpy as np
from Santa_Algorithm import (
    is_threshold_feasible,
    solve_configuration_lp,
    classify_items,
    build_hypergraph,
    local_search_perfect_matching,
    Hypergraph
)

# ========== Edge case testing ==========
def test_empty_input():
    valuations = np.array([[]])
    assert not is_threshold_feasible(valuations, 0.5)

def test_one_player_one_item_enough():
    valuations = np.array([[1.0]])
    assert is_threshold_feasible(valuations, 0.5)

def test_one_player_one_item_not_enough():
    valuations = np.array([[0.2]])
    assert not is_threshold_feasible(valuations, 0.5)

def test_negative_values():
    valuations = np.array([[0.3, -0.2], [-0.1, 0.5]])
    assert is_threshold_feasible(valuations, 0.3) # True to the second player

# ========== Large input tests ==========
def test_large_input_feasibility():
    np.random.seed(0)
    valuations = np.random.rand(50, 100)  # 50 players, 100 items
    assert isinstance(is_threshold_feasible(valuations, 0.5), bool)

# ========== Random inputs and comparison to conditions ==========
def test_random_allocation_classification_consistency():
    np.random.seed(1)
    valuations = np.random.rand(5, 10)
    threshold = 0.6
    allocation = solve_configuration_lp(valuations, threshold)
    fat, thin = classify_items(valuations, threshold)
    H = build_hypergraph(valuations, allocation, fat, thin, threshold)
    match = local_search_perfect_matching(H)

    # Make sure each player has received a set of items, and their total value meets the threshold
    for player, items in match.items():
        assert sum(valuations[player - 1, np.array(list(items)) - 1]) >= threshold

# ========== Tests for classify_items ==========
def test_classify_items_fat_thin():
    valuations = np.array([
        [0.9, 0.1],
        [0.2, 0.9]
    ])
    fat, thin = classify_items(valuations, 0.9)
    assert fat == {1, 2}
    assert thin == set()

