import json
from enum import Enum
import os.path
from mtgsdk import Card
import urllib.request





class Color(Enum):
    W = 1
    U = 2
    B = 3
    R = 4
    G = 5





def checkpic(picid):
    if os.path.isfile('CardImages/'+picid+'.jpg') != True:
        print('https://api.scryfall.com/cards/multiverse' + str(getMVid(picid)) + "?format=json")
        jsonResponce = json.load(urllib.request.urlopen('https://api.scryfall.com/cards/multiverse/' + str(getMVid(picid))))
        print(jsonResponce["image_uris"]["large"])
        urllib.request.urlretrieve(jsonResponce["image_uris"]["large"], 'CardImages/' + picid + '.jpg')

def getMVid(DBid):
    idarr = DBid.split('@')
    print(idarr[1])
    print(idarr[0])
    if idarr[1] in translateSet: idarr[1] = translateSet[idarr[1]]
    for setJson in jsonSets['data']:
        print(setJson['name'].lower())
        if idarr[1].lower() == setJson['name'].lower():
            idarr[1] = setJson['code']
            print(idarr[1])
    print(idarr[0])
    print(idarr[1])
    card = Card.where(name=idarr[0]) \
        .where(set=idarr[1]) \
        .all()
    print(card[0].multiverse_id)
    print(card[0].number)
    return card[0].multiverse_id

translateSet = {
    'Limited Edition Alpha' : 'LEA',
    'Alpha' : 'LEA',
    'Limited Edition Beta' : 'LEB',
    'Beta': 'LEB',
    'Unlimited Edition' : '2ED',
    'Unlimited' : '2ED',
    '2ed' : '2ED',
    'Revised' : '3ED',
    'Revised Edition' : '3ED',
    '3ed' : '3ED',
    'Fourth Edition' : '4ED',
    'Fifth Edition' : '5ED',
    'Classic Sixth Edition' : '6ED',
    'Sixth Edition': '6ED',
    'Seventh Edition': '7ED',
    'Eighth Edition': '8ED',
    'Ninth Edition': '9ED',
    'Tenth Edition': '10E',
    'Magic 2010': 'M10',
    'Magic 2011': 'M11',
    'Magic 2012': 'M12',
    'Magic 2013': 'M13',
    'Magic 2014': 'M14',
    'Magic 2015': 'M15',
    'Magic Origins': 'ORI',
    'Origins': 'ORI',
    'Magic 2012': 'M12'
}

jsonSets = json.load(urllib.request.urlopen('https://api.scryfall.com/sets/'))