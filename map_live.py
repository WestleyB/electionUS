import plotly.plotly as py
import plotly.tools as tls
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
token = stream_tokens[0]
stream_id = dict(token=token, maxpoints=3)

states = get_states()
states_long = list(states.keys())
states_short = list(states.values())


new_z=list(np.zeros(51) + 0.5)
data = [dict(
            type="choropleth",
            z=new_z,
            autocolorscale=False,
            colorscale=[[0, 'rgb(255,0,0)'], [0.2, 'rgb(255,0,0)'],
                        [0.4, 'rgb(255,255,255)'], [0.6, 'rgb(255,255,255)'],
                        [0.8, 'rgb(0,0,255)'], [1, 'rgb(0,0,255)']],
            hoverinfo='text',
            locationmode='USA-states',
            locations=states_short,
            name='Democrat',
            showscale=False,
            text=states_long,
            zauto=False,
            zmax=1,
            zmin=0,
            stream=stream_id,
        )]

layout = dict(
    autosize=False,
    geo=dict(
        countrycolor='rgb(102, 102, 102)',
        countrywidth=0.1,
        lakecolor='rgb(255, 255, 255)',
        landcolor='rgba(237, 247, 138, 0.28)',
        lonaxis=dict(
            gridwidth=1.5999999999999999,
            range=[-180, -50],
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
        subunitwidth=0.5
    ),
    hovermode='closest',
    images=list([
        dict(
            x=1,
            y=0.6,
            sizex=0.155,
            sizey=0.4,
            source='http://i.imgur.com/Xe3f1zg.png',
            xanchor='right',
            xref='paper',
            yanchor='bottom',
            yref='paper'
        )
    ]),
    showlegend=True,
    title='<b>PACE Approved legislation</b>',
    width=800,
    margin=dict(
        l=0,
        r=50,
        b=100,
        t=100,
        pad=4)
)
fig = dict(data=data, layout=layout)
py.iplot(fig, validate=False, filename='geo-streaming2',
         auto_open=False, fileopt='extend')


s = py.Stream(stream_id=token)

def lets_stream():

    i = 0
    new_z=list(np.zeros(51) + 0.5)
    s.open()

    while i <= 10:
        new_z[i] = i % 2
        s.write(dict(
            type="choropleth",
            z=new_z,
            autocolorscale=False,
            hoverinfo='text',
            showscale=False,
            zauto=False,
            ))
        s.heartbeat()
        time.sleep(2)
        i += 1


print("start sleep")
time.sleep(12)
print("end sleep and start live")
lets_stream()
s.close()

tls.embed('streaming-demos', '121')
