import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import Choropleth, Bar
import numpy as np
import time


def get_states():
    states_dict = {}
    states_dict["Alabama"] = "AL"
    states_dict["Michigan"] = "MI"
    states_dict["Alaska"] = "AK"
    states_dict["Minnesota"] = "MN"
    states_dict["Arizona"] = "AZ"
    states_dict["Mississippi"] = "MS"
    states_dict["Arkansas"] = "AR"
    states_dict["Missouri"] = "MO"
    states_dict["Californie"] = "CA"
    states_dict["Montana"] = "MT"
    states_dict["Caroline_du_Nord"] = "NC"
    states_dict["Nebraska"] = "NE"
    states_dict["Caroline_du_Sud"] = "SC"
    states_dict["Nevada"] = "NV"
    states_dict["Colorado"] = "CO"
    states_dict["New_Hampshire"] = "NH"
    states_dict["Connecticut"] = "CT"
    states_dict["New_Jersey"] = "NJ"
    states_dict["Dakota_du_Nord"] = "ND"
    states_dict["Nouveau_Mexique"] = "NM"
    states_dict["Dakota_du_Sud"] = "SD"
    states_dict["New_York"] = "NY"
    states_dict["Delaware"] = "DE"
    states_dict["Ohio"] = "OH"
    states_dict["Floride"] = "FL"
    states_dict["Oklahoma"] = "OK"
    states_dict["Georgie"] = "GA"
    states_dict["Oregon"] = "OR"
    states_dict["Hawai"] = "HI"
    states_dict["Pennsylvanie"] = "PA"
    states_dict["Idaho"] = "ID"
    states_dict["Rhode_Island"] = "RI"
    states_dict["Illinois"] = "IL"
    states_dict["Tennessee"] = "TN"
    states_dict["Indiana"] = "IN"
    states_dict["Texas"] = "TX"
    states_dict["Iowa"] = "IA"
    states_dict["Utah"] = "UT"
    states_dict["Kansas"] = "KS"
    states_dict["Vermont"] = "VT"
    states_dict["Kentucky"] = "KY"
    states_dict["Virginie"] = "VA"
    states_dict["Louisiane"] = "LA"
    states_dict["Virginie_Occidentale"] = "WV"
    states_dict["Maine"] = "ME"
    states_dict["Washington"] = "WA"
    states_dict["Maryland"] = "MD"
    states_dict["Wisconsin"] = "WI"
    states_dict["Massachusetts"] = "MA"
    states_dict["Wyoming"] = "WY"
    states_dict["District_de_Columbia"] = "DOC"
    return states_dict


stream_tokens = tls.get_credentials_file()['stream_ids']
token_map = stream_tokens[0]
stream_map = dict(token=token_map, maxpoints=3)
token_democrats = stream_tokens[1]
stream_democrats = dict(token=token_democrats, maxpoints=51)
token_republicans = stream_tokens[2]
stream_republicans = dict(token=token_republicans, maxpoints=51)
token_pie_voters = stream_tokens[3]
stream_pie_voters = dict(token=token_pie_voters, maxpoints=51)
token_pie_big_voters = stream_tokens[4]
stream_pie_big_voters = dict(token=token_pie_big_voters, maxpoints=51)

states = get_states()
states_long = list(states.keys())
states_short = list(states.values())


new_z = list(np.zeros(51) + 0.5)
trace_map = Choropleth(
            z=new_z,
            autocolorscale=False,
            colorscale=[[0, 'rgb(186,58,51)'], [0.2, 'rgb(186,58,51)'],
                        [0.4, 'rgb(255,255,255)'], [0.6, 'rgb(255,255,255)'],
                        [0.8, 'rgb(68,94,150)'], [1, 'rgb(68,94,150)']],
            hoverinfo='text',
            locationmode='USA-states',
            locations=states_short,
            name='Democrat',
            showscale=False,
            showlegend=False,
            text=states_long,
            zauto=False,
            zmax=1,
            zmin=0,
            stream=stream_map,
            )

trace_bar_democrats = Bar(
        x=['Democrats'],
        y=[100],
        marker=dict(color='rgb(68,94,150)'),
        showlegend=False,
        width=0.2,
        stream=stream_democrats,
)

trace_bar_republicans = Bar(
        x=['Republicans'],
        y=[100],
        marker=dict(color='rgb(186,58,51)'),
        showlegend=False,
        width=0.2,
        stream=stream_republicans,
)

data = [trace_map, trace_bar_democrats, trace_bar_republicans]

layout = dict(
    autosize=False,
    xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
              ),
    yaxis=dict(
                autorange=False,
                range=[0, 250],
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            ),
    geo=dict(
        countrycolor='rgb(102, 102, 102)',
        countrywidth=0.1,
        lakecolor='rgb(255, 255, 255)',
        landcolor='rgba(237, 247, 138, 0.28)',
        lonaxis=dict(
            gridwidth=1.5999999999999999,
            range=[-250, -50],
            showgrid=False
        ),
        projection=dict(
            type='albers usa'
        ),
        scope='usa',
        showland=True,
        showrivers=False,
        showsubunits=True,
        subunitcolor='rgb(102, 102, 102)',
        subunitwidth=1
    ),
    hovermode='closest',
    showlegend=False,
    title='<b>US elections in live</b>',
    width=1000,
    margin=dict(
        l=0,
        r=0,
        b=40,
        t=20,
        pad=4),
    font=dict(
        family="comic sans ms",
        size=24,
        color="grey"
        ),
    rmode='group',
    bargap=0.5,
)


fig_map = dict(data=data, layout=layout)
py.iplot(fig_map, validate=False, filename='map',
         auto_open=False, fileopt='extend')

fig = {
  "data": [
    {
      "values": [10, 10],
      "labels": [
        "Republicans",
        "Democrats"
      ],
      "text":"Voters",
      "domain": {"x": [0, .48]},
      "insidetextfont": {"color": "rgb(255,255,255)"},
      "marker": {'colors': ['rgb(186,58,51)', 'rgb(68,94,150)']},
      "name": "Voters",
      "hoverinfo":"label+percent+name",
      "hole": .5,
      "type": "pie",
      "stream": stream_pie_voters,
    },
    {
      "values": [10, 10],
      "labels": [
        "Republicans",
        "Democrats"
      ],
      "text":"Big Voters",
      "textposition":"inside",
      "domain": {"x": [.52, 1]},
      "insidetextfont": {"color": "rgb(255,255,255)"},
      "marker": {'colors': ['rgb(186,58,51)', 'rgb(68,94,150)']},
      "name": "Big Voters",
      "hoverinfo":"label+percent+name",
      "hole": .5,
      "type": "pie",
        "stream": stream_pie_big_voters,
    }],
  "layout": {
        "annotations": [
            {
                "font": {
                    "size":16
                },
                "showarrow": False,
                "text": "Popular",
                "x": 0.20,
                "y": 0.5
            },
            {
                "font": {
                    "size":16
                },
                "showarrow": False,
                "text": "Electoral",
                "x": 0.80,
                "y": 0.5
            }
        ],
        "showlegend":False,
    }
}

py.iplot(fig, filename='diagramme')


s_map = py.Stream(stream_id=token_map)
s_democrats = py.Stream(stream_id=token_democrats)
s_republicans = py.Stream(stream_id=token_republicans)
s_pie_voters = py.Stream(stream_id=token_pie_voters)
s_pie_big_voters = py.Stream(stream_id=token_pie_big_voters)

"""
def lets_stream():

    i = 0
    new_z = list(np.zeros(51) + 0.5)
    y_dem = 0
    y_repu = 0
    v_1 = 0
    v_2 = 0

    while i <= 10:
        new_z[i] = i % 2
        y_dem += 10
        y_repu += 12
        s_map.write(dict(
            type="choropleth",
            z=new_z,
            zauto=False,
            ))
        s_map.heartbeat()
        s_democrats.write(dict(type="bar", y=[y_dem]))
        s_republicans.write(dict(type="bar", y=[y_repu]))
        v_1 += np.random.randint(0, 21)
        v_2 += np.random.randint(0, 21)
        s_pie_voters.write(dict(type="pie", labels=["Republicans", "Democrats"],
                                values=[v_1, v_2]))
        s_pie_big_voters.write(dict(type="pie", values=[v_1, v_2],
                                    labels=["Republicans", "Democrats"]))
        time.sleep(2)
        i += 1
"""

"""
print("start sleep")
time.sleep(12)
print("end sleep and start live")
s_map.open()
s_democrats.open()
s_republicans.open()
s_pie_voters.open()
s_pie_big_voters.open()
lets_stream()
s_map.close()
s_democrats.close()
s_republicans.close()
s_pie_voters.close()
s_pie_big_voters.close()


tls.embed('streaming-demos', '121')
"""
