import unittest
from hypernetx import Hypergraph as HNXHypergraph
from fairpyx.fairpyx.algorithms.Santa_Algorithm import santa_claus_main, AllocationBuilder, is_threshold_feasible, solve_configuration_lp, classify_items
from fairpyx import Instance, AllocationBuilder

class TestSantaClausAlgorithms(unittest.TestCase):

    def test_simple_case(self):
        # בדיקה פשוטה עם שני שחקנים ו-3 פריטים
        allocation_builder = AllocationBuilder()
        allocation_builder.add_valuation("Alice", {"c1": 5, "c2": 0, "c3": 6})
        allocation_builder.add_valuation("Bob", {"c1": 0, "c2": 8, "c3": 0})

        result = santa_claus_main(allocation_builder)

        self.assertEqual(result, {'Alice': {'c1', 'c3'}, 'Bob': {'c2'}})

    def test_more_complex_case(self):
        # בדיקה עם 4 שחקנים ו-4 פריטים
        allocation_builder = AllocationBuilder()
        allocation_builder.add_valuation("A", {"c1": 10, "c2": 0, "c3": 0, "c4": 6})
        allocation_builder.add_valuation("B", {"c1": 10, "c2": 8, "c3": 0, "c4": 0})
        allocation_builder.add_valuation("C", {"c1": 0, "c2": 8, "c3": 6, "c4": 0})
        allocation_builder.add_valuation("D", {"c1": 0, "c2": 0, "c3": 6, "c4": 6})

        result = santa_claus_main(allocation_builder)

        self.assertEqual(result, {'A': {'c1'}, 'B': {'c2'}, 'C': {'c3'}, 'D': {'c4'}})

    def test_large_scale_case(self):
        # קלט גדול יותר עם 100 שחקנים ו-100 פריטים
        allocation_builder = AllocationBuilder()
        for i in range(100):
            valuations = {f"c{j + 1}": (1 if j == i else 0) for j in range(100)}  # Player_i values only item_i
            allocation_builder.add_valuation(f"Player_{i + 1}", valuations)

        result = santa_claus_main(allocation_builder)

        # Verify each player gets exactly one item: Player_1 gets c100, Player_2 gets c99, ..., Player_100 gets c1
        for i in range(100):
            self.assertEqual(result[f"Player_{i + 1}"], {f"c{100 - i}"})

    def test_threshold_feasibility(self):
        # בדיקה לפונקציה is_threshold_feasible
        valuations = {
            "Alice": {"c1": 7, "c2": 0, "c3": 4},
            "Bob": {"c1": 0, "c2": 8, "c3": 0}
        }

        self.assertFalse(is_threshold_feasible(valuations, 15))
        self.assertFalse(is_threshold_feasible(valuations, 10))
        self.assertTrue(is_threshold_feasible(valuations, 8))

    def test_solve_configuration_lp(self):
        # בדיקה לפונקציה solve_configuration_lp
        valuations = {
            "Alice": {"c1": 7, "c2": 0, "c3": 8},
            "Bob": {"c1": 0, "c2": 8, "c3": 0}
        }

        result = solve_configuration_lp(valuations, 8)

        expected = {'Alice': [{'c1'}, {'c3'}], 'Bob': [{'c2'}]}
        self.assertEqual(result, expected)

    def test_classify_items(self):
        # בדיקה לפונקציה classify_items
        valuations = {
            "Alice": {"c1": 0.5, "c2": 0, "c3": 0},
            "Bob": {"c1": 0, "c2": 0.1, "c3": 0.2}
        }

        fat_items, thin_items = classify_items(valuations, 1)

        self.assertEqual(fat_items, {'c1'})
        self.assertEqual(thin_items, {'c2', 'c3'})


if __name__ == '__main__':
    unittest.main()
