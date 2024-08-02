import json
import requests
from os.path import exists

def verifyDB():
    if (not exists('./players.json')):
        downloadPlayers()
    if (not exists('./clans.json')):
        downloadClans()
    if (not exists('./legends.json')):
        downloadLegends()

def downloadClans():
    raw = requests.get('https://api.npoint.io/6488fb58f82a76e31664')
    response = json.loads(raw.text)
    with open('./clans.json', 'w') as f:
        f.write(json.dumps(response, indent=4))
        
def downloadLegends():
    raw = requests.get('https://api.npoint.io/a61cbe38560a9ac5d278')
    response = json.loads(raw.text)
    with open('./legends.json', 'w') as f:
        f.write(json.dumps(response, indent=4))

def downloadPlayers():
    data = requests.get('https://api.npoint.io/73701443fb9f9a913c0b')
    player = json.loads(data.text)
    with open('./players.json', 'w') as f:
        f.write(json.dumps(player, indent=4))
    
def getPlayers():
    with open('./players.json', 'r') as f:
        raw = json.load(f)
        f.close()
    return raw

def getClans():
    with open('./clans.json', 'r') as f:
        clanList = json.load(f)
        f.close()
    return clanList

def getLegends():
    with open('./legends.json', 'r') as f:
        lend = json.load(f)
        f.close()
    return lend

def savePlayer(treeview):
    items = treeview.get_children()
    jsonArr = {'jogadores': []}
    for i in items:
        data = treeview.item(i)
        player = {"nome": f"{data['text']}", "hierarquia": f"{data['values'][2]}", "custo": data['values'][0], "clan": f"{data['values'][1]}", "lenda": f"{data['values'][3]}"}
        jsonArr['jogadores'].append(player)
    jsonArr['jogadores'].sort(key=lambda x: x['custo'], reverse=True)
    with open('players.json', 'w') as f:
        f.write(json.dumps(jsonArr, indent=4))
        f.close()

def saveClans(treeview):
    items = treeview.get_children()
    jsonArr = []
    for i in items:
        data = treeview.item(i)
        clan = {"CT": [int(data['values'][3][0]), int(data['values'][3][2]), int(data['values'][3][4])], "clan": f"{data['text']}", "color": f'{data['values'][4]}', "leader": f"{data['values'][0]}", "seasons": data['values'][2],"coleader": f"{data['values'][1]}"}
        jsonArr.append(clan)
    with open('clans.json', 'w') as f:
        f.write(json.dumps(jsonArr, indent=4))
        f.close()

def saveLegends(treeview):
    items = treeview.get_children()
    jsonArr = []
    for i in items:
        data = treeview.item(i)
        legend = {"thumbnail": f"{data['values'][0]}", "legend_name_key": data['text']}
        jsonArr.append(legend)
    jsonArr.sort(key=lambda x: x['legend_name_key'])
    with open('legends.json', 'w') as f:
        f.write(json.dumps(jsonArr, indent=4))
        f.close()

def getClansValues():
    clans = getClans()
    return [c['clan'] for c in clans]

def getLegendsValues():
    lendas = getLegends()
    return [l['legend_name_key'] for l in lendas]
