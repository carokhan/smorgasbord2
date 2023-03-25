import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import json
from data.allteams import teamnames

def allperf(final_df):
    avgs = final_df.groupby(["teamNum"]).mean().round(2)

    avgs["teamName"] = avgs.apply(lambda row: teamnames[int(row.teamNum2)], axis=1)
    avgs["shooterLvl"] = avgs.apply(lambda row: round(row.level), axis=1)
    def highlow(row):
        if row.shooterLvl == 1:
            return "high"
        else:
            return "low"
    avgs["shooterLevel"] = avgs.apply(lambda row: highlow(row), axis=1)
    fig = px.scatter(avgs, x='telePoints', y='autoPoints',
             hover_data=['teamName', 'telePoints', 'autoPoints', 'climb', 'shooterLevel'], size='climb',
             labels={'telePoints':'teleop cargo points', 'autoPoints': "auto cargo points", 'climb': 'climb level', 'teamName': "team name", 'shooterLevel': "shooter level"}, color="shooterLevel", color_continuous_scale=px.colors.sequential.Plotly3)
    fig.update_layout(
        title={'text': "Eventwide performance by team",
               'y': 0.9,
               'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},  
        width=1500, height= 500, paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)',
    font=dict(
            color="#777"
            ),
    xaxis=dict(
        linecolor="#777",  
        gridcolor="#777",
        showgrid=True  
    ),
    yaxis=dict(
        linecolor="#777",  
        gridcolor="#777",
        showgrid=True,  
    )
    )
    fig.update_traces(marker_sizemin = 5)

    fig.update_xaxes(showspikes=True, spikecolor="#777", spikesnap="cursor", spikemode="across", spikedash="dot")
    fig.update_yaxes(showspikes=True, spikecolor="#777", spikedash="dot")
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


def teamplot(df):
    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.02)

    fig.add_trace(go.Scatter(x=list(df["matchNum"]), y=list(df["autoPoints"]), name="auto cargo", hovertemplate="Match number: %{x}<br>Points scored from auto cargo: %{y}<br>"),row=3, col=1, )

    fig.add_trace(go.Scatter(x=list(df["matchNum"]), y=list(df["telePoints"]),name="tele cargo", hovertemplate="Match number: %{x}<br>Points scored from teleop cargo: %{y}<br>"),row=2, col=1)

    fig.add_trace(go.Scatter(x=list(df["matchNum"]), y=list(df["climb"]),name="climb level", hovertemplate="Match number: %{x}<br>Climb level=: %{y}<br>"),row=1, col=1)

    fig.update_layout(title={'text': "Team performance by each match",
               'y': 0.9,
               'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'}, width=1500, height= 425, paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)',
    font=dict(
            color="#777"
            ))
    fig.update_xaxes(linecolor="#777",  gridcolor="#777", showspikes=True, spikesnap="cursor", spikemode="across", spikecolor="#777", spikedash="dot")
    fig.update_xaxes(title_text="match number", row=3, col=1)


    fig.update_yaxes(linecolor="#777",  gridcolor="#777", showspikes=True, spikecolor="#777", spikedash="dot")
    fig.update_yaxes(title_text="climb level", row=1, col=1)
    fig.update_yaxes(title_text="teleop cargo", row=2, col=1)
    fig.update_yaxes(title_text="auto cargo", row=3, col=1)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json