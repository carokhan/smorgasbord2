import pandas as pd
import numpy as np
from flask import render_template, request
from web import app, utils
from data.allteams import teamnames
    
@app.route("/")
def main_page():
    data = utils.load_data()

    teams = {}
    for num in list(data["teamNum"]):
        teams[int(num)] = teamnames[num]

    auto_average = round(data["autoPoints"].mean(), 2)
    teleop_average = round(data["telePoints"].mean(), 2)
    climb_average = round(data["climb"].mean(), 2)
    auto_accuracy = str(round(data["autoAcc"].mean(), 2)*100) + "%"
    teleop_accuracy = str(round(data["teleAcc"].mean(), 2)*100) + "%"
    matches = data["matchNum"].max()
    # print(data["matchNum"])
    teleop_avg_bars = plotly_plot.allperf(data)
    context = {"auto_average": auto_average,
               "teleop_average": teleop_average, "climb_average": climb_average,
            'auto_accuracy': auto_accuracy,
            'teleop_accuracy': teleop_accuracy,'matches': matches, 'teleop_avg': teleop_avg_bars, "team_list": sorted(list(allteams.values()))}
    return render_template('plotly.html', context=context)


@app.route("/team", methods=['POST'])
def plot_team():
    team = request.form['team_name']
    team = team.split(" ")[0]
    teamSt = allteams[int(team)]
    byteam = lambda x: data[data.teamNum == x]
    teamdata = byteam(int(team))
    if teamdata["highPoints"].sum() > teamdata["lowPoints"].sum():
        level = "High shooter"
    elif teamdata["highPoints"].sum() < teamdata["lowPoints"].sum():
        level = "Low shooter"
    else:
        level = "Shoots high and low"
    auto_avg = round(teamdata["autoPoints"].mean(), 2)
    teleop_avg = round(teamdata["telePoints"].mean(), 2)
    climb_avg = round(teamdata["climb"].mean(), 2)
    auto_acc = str(round(teamdata["autoAcc"].mean(), 2)*100) + "%"
    tele_acc = str(round(teamdata["teleAcc"].mean(), 2)*100) + "%"
    defense = round(teamdata["defense"].mean(), 2)
    taxipc = round(teamdata["taxi"].mean(),2)
    teamgraph = plotly_plot.teamplot(teamdata)
    infostr = level + ", " + str(taxipc*100) + "% taxi rate"
    
    context = {"teamSt": teamSt, "level": infostr, "auto_avg": auto_avg, "teleop_avg": teleop_avg, "climb_avg": climb_avg, "auto_acc": auto_acc, "tele_acc": tele_acc, "defense": defense, "teamgraph": teamgraph, "team_list": sorted(list(allteams.values()))}
    
    return render_template('team.html', context=context)
