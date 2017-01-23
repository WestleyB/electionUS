import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import Figure, Choropleth, Bar, Pie, Layout
import numpy as np
import pandas as pd
from pymongo import MongoClient
import time


client = MongoClient('34.196.21.20', 27017, replicaset='rs0')
# client = MongoClient("localhost")
db = client['election']


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


def key_time_dataframe(key_time):
    cursor = db.us.aggregate([
                 {"$match": {"vote_timestamp": key_time}},
                 {"$group": {"_id": {"state": "$state",
                "vote_result": "$vote_result"}, "total": {"$sum": 1}}},
               ])
    info = (list(cursor))
    ligne = []
    df = pd.DataFrame()
    if len(info) != 0:
        for i in range(len(info)):
            ligne = [info[i]['total'], info[i]['_id']['state'],
                     info[i]['_id']['vote_result']]
            df = pd.concat([df, pd.DataFrame(ligne).T])
        df.columns = ['total', 'state', 'vote_result']
    return df


def query_grands_elec():
    df_grd_elec = pd.DataFrame()
    cur = db.grdelec.find()
    xcur = list(cur)
    if len(xcur):
        for j, elt in enumerate(xcur):
            df_grd_elec = df_grd_elec.append(pd.DataFrame(elt, index=[j]),
                                             ignore_index=True)
    return df_grd_elec


def states_result(key_time):
    df_state = key_time_dataframe(key_time)
    df_resultat = pd.DataFrame()
    df_prop_state = pd.DataFrame()

    if not df_state.empty:
        df_state_group = df_state.groupby('state')
        for key, elmt in df_state_group:
            elmt['pct'] = elmt['total'].apply(lambda x: x/elmt.total.sum())
            df_resultat = df_resultat.append(elmt[elmt.pct == elmt.pct.max()][['state', 'vote_result', 'total']], ignore_index=True)
            df_prop_state = df_prop_state.append(elmt[elmt.state == 'Maine'],
                                                 ignore_index=True)
            df_prop_state = df_prop_state.append(elmt[elmt.state == 'Nebraska'],
                                                 ignore_index=True)
    return df_resultat, df_prop_state


def score_election(df_r, df_grd_elec):
    result = pd.merge(df_r, df_grd_elec, on='state')
    return result[['vote_result', 'grands_electeurs']]


def score_state(df_r, df_grd_elec):
    return pd.merge(df_r, df_grd_elec, on='state')


def score_election_prop(df_r, df_prop_state, df_grd_elec):
    result = pd.merge(df_r, df_grd_elec, on='state')
    result[['vote_result', 'grands_electeurs']].groupby('vote_result').sum()


stream_tokens = tls.get_credentials_file()['stream_ids']
token_map = stream_tokens[0]
token_bar_pop = stream_tokens[1]
token_pie_pop = stream_tokens[2]
token_bar_elec = stream_tokens[3]
token_pie_elec = stream_tokens[4]

stream_map = dict(token=token_map, maxpoints=3)
stream_bar_pop = dict(token=token_bar_pop, maxpoints=51)
stream_pie_pop = dict(token=token_pie_pop, maxpoints=51)
stream_bar_elec = dict(token=token_bar_elec, maxpoints=51)
stream_pie_elec = dict(token=token_pie_elec, maxpoints=51)

states = get_states()
states_long = list(states.keys())
states_short = list(states.values())


new_z = list(np.zeros(51) + 0.5)
trace_map = Choropleth(
            z=new_z, autocolorscale=False, hoverinfo='text',
            colorscale=[[0, 'rgb(186,58,51)'], [0.2, 'rgb(186,58,51)'],
                        [0.4, 'rgb(255,255,255)'], [0.6, 'rgb(255,255,255)'],
                        [0.8, 'rgb(68,94,150)'], [1, 'rgb(68,94,150)']],
            locationmode='USA-states', locations=states_short, name='Democrat',
            showscale=False, showlegend=False, text=states_long, zauto=False,
            zmax=1, zmin=0, stream=stream_map,)

data = [trace_map]

layout = dict(autosize=False, geo=dict(countrycolor='rgb(102, 102, 102)',
                                       countrywidth=0.1,
                                       lakecolor='rgb(255, 255, 255)',
                                       landcolor='rgba(237, 247, 138, 0.28)',
                                       lonaxis=dict(gridwidth=1.60,
                                                    range=[-250, -50],
                                                    showgrid=False),
                                       projection=dict(type='albers usa'),
                                       scope='usa', showland=True,
                                       showrivers=False, showsubunits=True,
                                       subunitcolor='rgb(102, 102, 102)',
                                       subunitwidth=1),
              hovermode='closest', showlegend=False, title='<b>""</b>',
              width=1000, margin=dict(l=0, r=0, b=40, t=20, pad=4),
              font=dict(family="comic sans ms", size=24, color="grey"),
              rmode='group', bargap=0.5,)


fig_map = dict(data=data, layout=layout)
py.iplot(fig_map, validate=False, filename='map',
         auto_open=False, fileopt='extend')


trace_3 = Bar(x=["Trump", "Clinton"], y=[0, 0], xaxis='x1', yaxis='y1',
              marker=dict(color=['rgb(186,58,51)', 'rgb(68,94,150)']),
              showlegend=False, stream=stream_bar_pop,)

trace_4 = Pie(values=[0, 0], labels=["Trump", "Clinton"], text="Voters",
              domain={"x": [0.23, 0.495], "y": [0, 0.70]},
              marker={'colors': ['rgb(186,58,51)', 'rgb(68,94,150)']},
              name="Voters", hoverinfo="label+percent+name", hole=.5,
              type="pie", textposition="inside", stream=stream_pie_pop,)

# INDIRECT :
trace_2 = Pie(values=[0, 0], labels=["Trump", "Clinton"], text="Great Voters",
              domain={"x": [0.505, 0.77], "y": [0, 0.70]},
              marker={'colors': ['rgb(186,58,51)', 'rgb(68,94,150)']},
              name="Voters", hoverinfo="label+percent+name", hole=.5,
              type="pie", showlegend=True, textposition="inside",
              stream=stream_pie_elec,)

trace_1 = Bar(x=["Trump", "Clinton"], y=[0, 0], xaxis='x2', yaxis='y2',
              marker=dict(color=['rgb(186,58,51)', 'rgb(68,94,150)']),
              showlegend=False, stream=stream_bar_elec,)

data9 = [trace_1, trace_2, trace_3, trace_4]

"""
annotations=[
        dict(x=xi,y=yi,
             #text=str(round(1.0 * float(yi)/100000,2)+'M'),
             text = round(yi/1000000.0,1),
             xanchor='bottom',
             yanchor='bottom',
             showarrow=False,
             font = {"size": 16},
        ) for xi, yi in zip(x, y3)
        ],
"""
layout9 = Layout(xaxis1=dict(domain=[0.08, 0.23], anchor='y1'),
                 yaxis1=dict(domain=[0, 1], anchor='x1',
                             title='Nombre Electeurs',
                             titlefont=dict(family='Arial, sans-serif',
                                            size=20, color='black'),
                             showticklabels=True,),
                 xaxis2=dict(domain=[0.85, 1], anchor='y2'),
                 yaxis2=dict(domain=[0, 1], anchor='x2',
                             title='Nombre Grands Electeurs',
                             titlefont=dict(family='Arial, sans-serif',
                                            size=20, color='black'),
                             showticklabels=True,),
                 margin=dict(l=0, r=0, b=100, t=100, pad=4),
                 showlegend=True, title='<b>Suffrage DIRECT vs INDIRECT</b>',
                 font={"size": 15},)


fig9 = Figure(data=data9, layout=layout9)
py.iplot(fig9, filename='diagramme')


s_map = py.Stream(stream_id=token_map)
s_bar_pop = py.Stream(stream_id=token_bar_pop)
s_pie_pop = py.Stream(stream_id=token_pie_pop)
s_bar_elec = py.Stream(stream_id=token_bar_elec)
s_pie_elec = py.Stream(stream_id=token_pie_elec)


def lets_stream():
    key_time = '2016-11-08T20:00'
    electorals = query_grands_elec()
    nb_electoral_demo = 0
    nb_electoral_repu = 0
    count_demo = 0
    count_repu = 0

    for el in range(61):
        key_time = '2016-11-08T20:' + ('00' + str(el))[-2:]
        print(key_time)
        vote_results, _ = states_result(key_time)
        if "state" in vote_results.columns:
            popular_results = key_time_dataframe(key_time)
            electoral_results = score_election(vote_results, electorals)
            l_states = vote_results["state"].values
            vote_count = vote_results["total"].values
            winners = vote_results["vote_result"].values
            electoral = electoral_results["grands_electeurs"].values
            for s, w, e, c in zip(l_states, winners, electoral, vote_count):
                index_state = states_short.index(states[s])
                if "clinton" in w.lower():
                    new_z[index_state] = 1
                    nb_electoral_demo += e
                if "trump" in w.lower():
                    new_z[index_state] = 0
                    nb_electoral_repu += e

                state_df = popular_results.loc[popular_results["state"] == s]
                c = state_df.loc[state_df["vote_result"] == "Trump"]["total"].values[0]
                count_repu += c
                c = state_df.loc[state_df["vote_result"] == "Clinton"]["total"].values[0]
                count_demo += c

                s_map.write(dict(type="choropleth", z=new_z, zauto=False,))
                s_bar_pop.write(dict(type="bar", y=[count_repu, count_demo]))
                s_pie_pop.write(dict(type="pie", labels=["Trump", "Clinton"],
                                     values=[count_repu, count_demo]))
                s_bar_elec.write(dict(type="bar", y=[nb_electoral_repu,
                                                     nb_electoral_demo]))
                s_pie_elec.write(dict(type="pie", labels=["Trump", "Clinton"],
                                      values=[nb_electoral_repu,
                                              nb_electoral_demo]))

                time.sleep(2)


print("start sleep")

time.sleep(5)
print("end sleep and start live")

s_map.open()
s_bar_pop.open()
s_pie_pop.open()
s_bar_elec.open()
s_pie_elec.open()
lets_stream()
s_map.close()
s_bar_pop.close()
s_pie_pop.close()
s_bar_elec.close()
s_pie_elec.close()


tls.embed('streaming-demos', '121')
