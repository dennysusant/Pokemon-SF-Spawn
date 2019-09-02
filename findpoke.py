from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np 
import pandas as pd 
import json
import requests 
import folium
import random
from folium.plugins import FloatImage


app=Flask(__name__)


types=[]
for item in range(1,19):
    url='https://pokeapi.co/api/v2/type/{}'.format(item)
    data=requests.get(url=str(url))
    data=data.json()
    types.append(data['name'])
    newcolor=[]
color=['darkred', 'orange', 'darkgreen', 'green', 'white', 'pink', 'lightgray', 'gray', 'lightgreen', 'lightblue', 'cadetblue', 'red', 'black', 'lightred', 'beige', 'purple', 'blue', 'darkpurple', 'darkblue']
for item in range (len(color)):
    newcolor.append(color[item])
warna={}
for types,newcolor in zip(types,newcolor):
    warna[types]=newcolor

poke=pd.read_csv('pokemon-spawns.csv')
gambar={}
for item in poke['name'].unique()[:80]:
    if item != 'Nidoran♀' and item !='Nidoran♂':
        url1='https://pokeapi.co/api/v2/pokemon/{}'.format(item.lower())
        data=requests.get(url=url1)
        data=data.json()
        b=[]
        b.append(data["sprites"]['front_default'])
        b.append(data['types'][0]['type']['name'])
        gambar[item]=b

@app.route('/')
def home():
    return render_template('menupoke.html')

@app.route('/input', methods=['GET','POST'])
def input():
    return render_template('poke.html')


@app.route('/lihat', methods=['GET','POST'])
def lihat():
    poke=pd.read_csv('pokemon-spawns.csv')
    m=folium.Map(
    location=[37.773972, -122.431297],
    zoom_start=12
    )
    for item in range(len(list(poke['lat'].head(1000)))):
        if poke['name'].iloc[item] != 'Nidoran♀' and poke['name'].iloc[item] !='Nidoran♂':
            a=(poke['name'].iloc[item])
            html='<img src="{}">'.format(gambar[a][0])
            type1=gambar[a][1]
            folium.Marker(
                [poke['lat'].iloc[item], poke['lng'].iloc[item]],
                popup=html ,
                tooltip=poke['name'].iloc[item],
                icon=folium.Icon(color="{}".format(warna[str(type1)]), icon='info-sign')
                ).add_to(m)
    m.save('templates/mappoke1.html')
    return render_template('mappoke1.html')




@app.route('/Cari', methods=['GET','POST'])
def Cari():
    poke=pd.read_csv('pokemon-spawns.csv')
    m=folium.Map(
        location=[37.773972, -122.431297],
        zoom_start=12
        )

    body=request.form
    body1=body['pokemon']
    body1=body1.capitalize()
    if body1 in list(poke['name'].head(100)):
        for item in range(len(list(poke['name'].head(100)))):
            if poke['name'].iloc[item]==body1:
                a=poke['name'].iloc[item]
                html='<img src="{}">'.format(gambar[a][0])
                folium.Marker(
                    [poke['lat'].iloc[item], poke['lng'].iloc[item]],
                    popup=html,
                    tooltip=poke['name'].iloc[item]
                    ).add_to(m)
        savepic1='templates/{}.html'.format(body1)
        m.save(savepic1)
        return render_template('{}.html'.format(body1))
    else:
        return jsonify('data tidak ditemukan')



if __name__=='__main__':
    app.run(debug=True)