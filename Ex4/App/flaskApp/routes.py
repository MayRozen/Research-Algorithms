from flask import render_template, request, redirect, url_for
from App import app
from fairpyx import santa_claus_main, Instance, AllocationBuilder

@app.route("/", methods=["GET", "POST"])
@app.route("/setup", methods=["GET", "POST"])
def setup():
    """
    שלב 1: המשתמש בוחר כמות שחקנים, כמות מתנות, וערך קבוע לכל מתנה.
    """
    if request.method == "POST":
        # קבלת הקלט מהטופס:
        try:
            num_players = int(request.form["num_players"])
            num_items = int(request.form["num_items"])
            item_value = float(request.form["item_value"])
        except (KeyError, ValueError):
            # במקרה של קלט שגוי – נחזיר פשוט ל‐setup
            return redirect(url_for("setup"))

        # נמשיך לשלב של מילוי טבלת הערכות:
        return render_template(
            "valuations.html",
            num_players=num_players,
            num_items=num_items,
            item_value=item_value
        )

    # GET: פשוט הצג את הטופס
    return render_template("setup.html")


@app.route("/run", methods=["POST"])
def run_algorithm():
    """
    שלב 2: עיבוד הטבלה ובהרצת האלגוריתם.
    """
    # נקבל ב-POST את:
    # num_players, num_items, item_value  וכן כל הערכים v-i-j
    try:
        num_players = int(request.form["num_players"])
        num_items = int(request.form["num_items"])
        item_value = float(request.form["item_value"])
    except (KeyError, ValueError):
        return redirect(url_for("setup"))

    # בונים את שמות השחקנים: P1, P2, ... P<num_players>
    players = [f"P{i}" for i in range(1, num_players+1)]
    # בונים את שמות המתנות: G1, G2, ... G<num_items>
    items = [f"G{j}" for j in range(1, num_items+1)]

    # מייצרים את מילון ה-valuations:
    # valuations = {player_name: { item_name: ערך }, ... }
    valuations = {p: {} for p in players}
    for i, p in enumerate(players, start=1):
        for j, g in enumerate(items, start=1):
            key = f"v-{i}-{j}"
            try:
                v = float(request.form[key])
            except (KeyError, ValueError):
                v = 0.0
            # אם v == item_value אז השחקן רוצה את המתנה, אחרת 0
            valuations[p][g] = v

    # נגדיר קיבולות לכל שחקן = 1
    agent_capacities = {p: 1 for p in players}
    # נדאג שקיבולת כל פריט = 1 (כל מתנה יכולה להינתן לשחקן אחד בלבד)
    item_capacities = {g: 1 for g in items}

    # בונים אינסטנס ואז AllocationBuilder ואז מריצים את האלגוריתם
    instance = Instance(
        valuations=valuations,
        agent_capacities=agent_capacities,
        item_capacities=item_capacities
    )
    allocation_builder = AllocationBuilder(instance=instance)
    # הרצת הפונקציה הראשית:
    final_alloc = santa_claus_main(allocation_builder)
    # final_alloc זו מילון { "P1": {"G3"}, "P2": {"G1","G2"}, ... } (סט של מתנות)

    return render_template("result.html", allocation=final_alloc)
