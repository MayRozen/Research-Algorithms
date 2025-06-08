from flask import render_template, request, redirect, url_for
from flaskApp import app

from fairpyx.algorithms.Santa_Algorithm import santa_claus_main
from fairpyx.instances import Instance
from fairpyx.allocations import AllocationBuilder

@app.route("/")
def setup():
    if request.method == "POST":
        try:
            num_players = int(request.form["num_players"])
            num_items   = int(request.form["num_items"])
            item_value  = float(request.form["item_value"])
        except (KeyError, ValueError):
            flash("Please enter valid numbers.", "danger")
            return redirect(url_for("setup"))

        return render_template(
            "valuations.html",
            num_players=num_players,
            num_items=num_items,
            item_value=item_value,
            previous_vals=None
        )
    return render_template("setup.html")

@app.route("/")
def run_algorithm():
    try:
        num_players = int(request.form["num_players"])
        num_items   = int(request.form["num_items"])
        item_value  = float(request.form["item_value"])
    except (KeyError, ValueError):
        flash("Session expired—please start over.", "warning")
        return redirect(url_for("setup"))

    players = [f"P{i}" for i in range(1, num_players+1)]
    items   = [f"G{j}" for j in range(1, num_items+1)]

    # build valuations dict and simultaneously collect for re-render
    valuations = {p: {} for p in players}
    for i, p in enumerate(players, start=1):
        for j, g in enumerate(items, start=1):
            key = f"v-{i}-{j}"
            try:
                v = float(request.form[key])
            except (KeyError, ValueError):
                v = 0.0
            valuations[p][g] = v

    # validation: all non-zero for a given gift must be identical
    for g in items:
        nonzeros = {valuations[p][g] for p in players if valuations[p][g] != 0}
        if len(nonzeros) > 1:
            flash(f"All non-zero valuations for gift {g} must be the same.", "danger")
            return render_template(
                "valuations.html",
                num_players=num_players,
                num_items=num_items,
                item_value=item_value,
                previous_vals=valuations
            )

    # capacities = 1 each
    agent_caps = {p:1 for p in players}
    item_caps  = {g:1 for g in items}

    instance = Instance(
        valuations=valuations,
        agent_capacities=agent_caps,
        item_capacities=item_caps
    )
    builder = AllocationBuilder(instance=instance)
    final_alloc = santa_claus_main(builder)

    return render_template("result.html", allocation=final_alloc)