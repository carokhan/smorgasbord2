import pandas as pd
import numpy as np
from flask import render_template, request
from web import app
import web.utils.data as data_tools
import yaml
import web.utils.graphs as graphs

with open("data/teams.yaml", "r") as f:
    teamnames = yaml.load(f, Loader=yaml.Loader)


@app.route("/")
def main_page():
    data = data_tools.load_data()

    if data is None:
        return render_template("204.html")

    teams = {}
    for num in list(data["teamNumber"]):
        try:
            teams[int(num)] = teamnames[int(num)]
        except KeyError:
            data = data[data.teamNumber != num]

    auto_average = round(data["autoPoints"].mean(), 2)
    teleop_average = round(data["telePoints"].mean(), 2)
    charge_average = round(data["chargePoints"].mean(), 2)
    cycles = round(data["cycles"].mean(), 2)
    matches = data["matchNum"].max()

    graph = graphs.overall_event(data)

    context = {
        "auto_average": auto_average,
        "teleop_average": teleop_average,
        "charge_average": charge_average,
        "cycles": cycles,
        "matches": matches,
        "team_list": sorted(list(teams.values())),
        "graph": graph,
    }
    return render_template("main.html", context=context)


@app.route("/team", methods=["POST"])
def plot_team():
    data = data_tools.load_data()

    teams = {}
    for num in list(data["teamNumber"]):
        try:
            teams[int(num)] = teamnames[int(num)]
        except KeyError:
            data = data[data.teamNumber != num]

    team = request.form["team_name"].split(" ")[0]
    name = teamnames[int(team)]

    lookup = lambda x: data[data.teamNumber == x]
    team_data = lookup(int(team))

    total_avg = round(team_data["totalPoints"].mean(), 2)

    auto_avg = round(team_data["autoPoints"].mean(), 2)
    teleop_avg = round(team_data["telePoints"].mean(), 2)
    charge_avg = round(team_data["chargePoints"].mean(), 2)

    cycle_avg = round(team_data["cycles"].mean(), 2)

    defense = round(team_data["defenseScore"].mean(), 2)

    graph = graphs.by_team(team_data)

    context = {
        "name": name,
        "total_avg": "Average points: " + str(total_avg),
        "auto_avg": auto_avg,
        "teleop_avg": teleop_avg,
        "charge_avg": charge_avg,
        "cycle_avg": cycle_avg,
        "defense": defense,
        "graph": graph,
        "team_list": sorted(list(teams.values())),
    }

    return render_template("team.html", context=context)