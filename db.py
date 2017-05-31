import pickle
import json
import urllib.request
import os.path

class Urllable(str):
    def tourl(self):
        return "%20".join(self.split())

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



class DB:

    database = {}

    def add(self, CardDB):
      self.database[CardDB.getDBid()] = CardDB

    def save(self):
        with open('DB' + '.pkl', 'wb') as f:
            pickle.dump(self.database, f, pickle.HIGHEST_PROTOCOL)

    def read(self):
        if os.path.isfile('DB.pkl') == True:
            with open('DB.pkl', 'rb') as f:
                self.database = pickle.load(f)

