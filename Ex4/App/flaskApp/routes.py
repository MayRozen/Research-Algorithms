from flask import render_template, request, redirect, url_for, flash
from flaskApp import app

from fairpyx.algorithms.Santa_Algorithm import santa_claus_main, logger as algo_logger
from fairpyx.instances import Instance
from fairpyx.allocations import AllocationBuilder

import logging,io
from logging import StreamHandler

logger = logging.getLogger(__name__)

@app.route("/", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        try:
            num_players = int(request.form["num_players"]) # Entering multiple players
            num_items   = int(request.form["num_items"]) # Entering multiple gifts
            if num_players < 1 or num_items < 1:
                raise ValueError
        except:
            flash("Please enter integers ≥ 1", "danger")
            return redirect(url_for("setup"))

        return render_template(
            "valuations.html",
            num_players=num_players,
            num_items=num_items
        )

    return render_template("setup.html")


@app.route("/run", methods=["POST"])
def run_algorithm():
    log_stream = io.StringIO()
    stream_handler = StreamHandler(log_stream)
    stream_handler.setLevel(logging.DEBUG)
    algo_logger.addHandler(stream_handler)
    algo_logger.setLevel(logging.DEBUG)

    try:
        num_players = int(request.form["num_players"])
        num_items   = int(request.form["num_items"])
    except (KeyError, ValueError):
        flash("Session expired—please start over.", "warning")
        return redirect(url_for("setup"))

    # Reads the number of players and items from the form
    players = [f"P{i}" for i in range(1, num_players+1)]
    items   = [f"G{j}" for j in range(1, num_items+1)]

    # build valuations dict (each gift its own value)
    valuations = {p: {} for p in players}
    for i, p in enumerate(players, start=1):
        for j, g in enumerate(items, start=1):
            key = f"v-{i}-{j}"
            try:
                v = float(request.form[key])
            except (KeyError, ValueError):
                v = 0.0
            valuations[p][g] = v

    # build and run
    agent_caps = {p:1 for p in players}
    item_caps  = {g:1 for g in items}

    instance   = Instance(
        valuations=valuations,
        agent_capacities=agent_caps,
        item_capacities=item_caps
    )
    builder    = AllocationBuilder(instance=instance)
    final_alloc = santa_claus_main(builder) # Running the algorithm

    algo_logger.removeHandler(stream_handler)
    logs = log_stream.getvalue().splitlines()

    return render_template(
        "result.html",
        allocation=final_alloc,
        logs=logs
    )
