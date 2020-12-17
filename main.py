import requests
from bs4 import BeautifulSoup
import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["forbes"]
col=db["billionaires"]
URL="https://www.forbes.com/forbesapi/person/billionaires/2020/position/true.json"
def addJson():
    r=requests.get(URL,headers= {
            "cookie": "notice_gdpr_prefs"
       })
    r=r.json()
    for person in r["personList"]["personsLists"]:
        col.insert_one(person)

def youngest():
    print("\nTen youngest billionaires:\n")
    contor=1
    youngest=col.find({ "age": { "$exists": True } }).sort("age")
    for x in youngest:
        if contor<=10:
            print(contor,x['personName']+", age =",x['age'])
            contor=contor+1
def numberOfAmericans():
    citizens=col.find({ "countryOfCitizenship": { "$exists": True } })
    americans=0
    nonamericans=0
    for x in citizens:
        if x['countryOfCitizenship']=="United States":
            americans=americans+1
        else:
            nonamericans=nonamericans+1
    print("\nAmericans:",americans)
    print("Other:",nonamericans)
def philanthropy():
    print("\nTop ten highest philantropy score:\n")
    contor=1
    youngest=col.find({ "philanthropyScore": { "$exists": True } }).sort("philanthropyScore",pymongo.DESCENDING)
    for x in youngest:
        if contor<=10 or x['philanthropyScore']==5:
            print(contor,x['personName']+", philanthropyScore =",x['philanthropyScore'])
            contor=contor+1

youngest()
numberOfAmericans()
philanthropy()