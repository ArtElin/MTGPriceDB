import json
import urllib.request
from enum import Enum
import pickle
import os.path
from mtgsdk import Card



class Urllable(str):
    def tourl(self):
        return "%20".join(self.split())

class Color(Enum):
    W = 1
    U = 2
    B = 3
    R = 4
    G = 5


class CardDB:
    name = Urllable("")
    set = Urllable("")
    price = ""
    color = None
    quantity = "0"
    def findCFB(self):
        jsonResponce = json.load(
            urllib.request.urlopen("http://magictcgprices.appspot.com/api/cfb/price.json?cardname=" +
                                   self.name.tourl() + "&setname=" + self.set.tourl()))
        return jsonResponce.pop()
    def getDBid(self):
        return self.name+'@'+self.set
    def __init__(self, name, mtgset, color):
        self.name = Urllable(name)
        self.set = Urllable(mtgset)
        self.price = self.findCFB()
        self.color = set(color)
    def __init__(self, name, mtgset, color, quantity):
        self.name = Urllable(name)
        self.set = Urllable(mtgset)
        self.price = self.findCFB()
        self.color = set(color)
        self.quantity = quantity
    def __str__(self):
        return "Card object "+self.name+" from "+self.set

DB = {}

def addtoDB(Card):
    DB[Card.getDBid()] = Card

def saveDB():
    with open('DB' + '.pkl', 'wb') as f:
        pickle.dump(DB, f, pickle.HIGHEST_PROTOCOL)

def readDB():
    print(1)
    with open('DB' + '.pkl', 'rb') as f:
       return pickle.load(f)

def checkpic(picid):
    if os.path.isfile('CardImages/'+picid+'.jpg') != True:
        jsonResponce = json.load(urllib.request.urlopen('https://api.scryfall.com/cards/' + str(getMVid(picid)) + "?format=json"))
        print(jsonResponce["image_uris"]["large"])
        urllib.request.urlretrieve(jsonResponce["image_uris"]["large"], 'CardImages/' + picid + '.jpg')

def getMVid(DBid):
    idarr = DBid.split('@')
    card = Card.where(name=idarr[0]) \
        .where(set=translateSet[idarr[1]]) \
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