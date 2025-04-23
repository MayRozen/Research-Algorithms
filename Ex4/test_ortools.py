import pytest
from ortools.linear_solver import pywraplp


# דוגמת בדיקה: פתרון בעיה לינארית פשוטה
def test_linear_programming():
    # יצירת פתרון לינארי חדש (LP)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise Exception("לא ניתן ליצור את הפתרון")

    # יצירת משתנים
    x = solver.IntVar(0.0, 10.0, 'x')
    y = solver.IntVar(0.0, 10.0, 'y')

    # הוספת מגבלות
    solver.Add(x + 2 * y <= 14)
    solver.Add(3 * x - y >= 0)
    solver.Add(x - y <= 2)

    # פונקציית אובייקטיבית (מטרת האופטימיזציה)
    solver.Maximize(3 * x + 4 * y)

    # פתרון הבעיה
    status = solver.Solve()

    # בדיקה אם מצאנו פתרון
    assert status == pywraplp.Solver.OPTIMAL

    # בדיקה של הערכים של המשתנים
    assert x.solution_value() == 4.0
    assert y.solution_value() == 5.0


# דוגמת בדיקה נוספת: פתרון בעיית שיבוץ
def test_assignment_problem():
    # מטריצה של עלויות
    costs = [
        [3, 2, 1],
        [5, 4, 3],
        [7, 6, 5]
    ]

    # יצירת פתרון חדש
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise Exception("לא ניתן ליצור את הפתרון")

    # יצירת משתנים עבור כל שיבוץ
    x = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(solver.BoolVar(f'x_{i}_{j}'))
        x.append(row)

    # הוספת מגבלות (כל שחקן מקבל משימה אחת)
    for i in range(3):
        solver.Add(sum(x[i][j] for j in range(3)) == 1)

    # הוספת מגבלות (כל משימה מוקצת לשחקן אחד)
    for j in range(3):
        solver.Add(sum(x[i][j] for i in range(3)) == 1)

    # פונקציית אובייקטיבית (הקטנת העלות)
    objective = solver.Objective()
    for i in range(3):
        for j in range(3):
            objective.SetCoefficient(x[i][j], costs[i][j])
    objective.SetMinimization()

    # פתרון הבעיה
    status = solver.Solve()

    # בדיקה אם מצאנו פתרון
    assert status == pywraplp.Solver.OPTIMAL

    # בדיקה של הערכים של המשתנים
    assert x[0][0].solution_value() == 1
    assert x[1][2].solution_value() == 1
    assert x[2][1].solution_value() == 1

