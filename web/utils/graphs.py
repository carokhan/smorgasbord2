import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import yaml
import json

with open("data/teams.yaml", "r") as f:
    teamnames = yaml.load(f, Loader=yaml.Loader)


def overall_event(df):
    df["teamNumber2"] = df["teamNumber"]
    avgs = df.groupby(["teamNumber"]).mean().round(2)
    avgs["teamName"] = avgs.apply(lambda row: teamnames[int(row.teamNumber2)], axis=1)

    print(avgs.head())

    fig = px.scatter(
        avgs,
        x="telePoints",
        y="autoPoints",
        hover_data=[
            "teamName",
            "telePoints",
            "autoPoints",
            "chargePoints",
            "defenseScore",
        ],
        size="chargePoints",
        labels={
            "telePoints": "teleop points",
            "autoPoints": "auto points",
            "chargePoints": "charge station points",
            "teamName": "team name",
            "defenseScore": "defense",
        },
        color="defenseScore",
        color_continuous_scale=px.colors.sequential.Plotly3,
    )

    fig.update_layout(
        title={
            "text": "Eventwide performance by team",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        width=1500,
        height=700,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#777"),
        xaxis=dict(linecolor="#777", gridcolor="#777", showgrid=True),
        yaxis=dict(
            linecolor="#777",
            gridcolor="#777",
            showgrid=True,
        ),
    )

    fig.update_traces(marker_sizemin=5)

    fig.update_xaxes(
        showspikes=True,
        spikecolor="#777",
        spikesnap="cursor",
        spikemode="across",
        spikedash="dot",
    )
    fig.update_yaxes(showspikes=True, spikecolor="#777", spikedash="dot")
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return plot_json


def by_team(df):
    df = df.sort_values("matchNum")

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    
    fig.add_trace(
        go.Scatter(
            x=list(df["matchNum"]),
            y=list(df["autoPoints"]),
            name="auto points",
            hovertemplate="Match number: %{x}<br>Auto points: %{y}<br>",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=list(df["matchNum"]),
            y=list(df["telePoints"]),
            name="tele points",
            hovertemplate="Match number: %{x}<br>Teleop points: %{y}<br>",
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=list(df["matchNum"]),
            y=list(df["teleopDockState"]),
            name="endgame level",
            hovertemplate="Match number: %{x}<br>Climb level=: %{y}<br>",
        ),
        row=3,
        col=1,
    )

    fig.update_layout(
        title={
            "text": "Team performance by each match",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        width=1500,
        height=425,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#777"),
    )
    fig.update_xaxes(
        linecolor="#777",
        gridcolor="#777",
        showspikes=True,
        spikesnap="cursor",
        spikemode="across",
        spikecolor="#777",
        spikedash="dot",
    )
    fig.update_xaxes(title_text="match number", row=3, col=1)

    fig.update_yaxes(
        linecolor="#777",
        gridcolor="#777",
        showspikes=True,
        spikecolor="#777",
        spikedash="dot",
    )
    fig.update_yaxes(title_text="auto cargo", row=1, col=1)
    fig.update_yaxes(title_text="teleop cargo", row=2, col=1)
    fig.update_yaxes(title_text="endgame level", row=3, col=1)

    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
