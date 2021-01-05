import requests
import pymongo
#Connecting to mongodb database and collection
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client["forbes"]
col=db["billionaires"]
#url from forbes with the data
URL="https://www.forbes.com/forbesapi/person/billionaires/2020/position/true.json"

#add the data to mongodb database
def addJson():
    r=requests.get(URL,headers= {
            "cookie": "notice_gdpr_prefs"
       })
    r=r.json()
    nr=0
    for person in r["personList"]["personsLists"]:
        if nr<200:
            col.insert_one(person)
            nr=nr+1
#sort and show youngest billionaires
def youngest():
    print("\nTen youngest billionaires:\n")
    contor=1
    youngest=col.find({ "age": { "$exists": True } }).sort("age")
    for x in youngest:
        if contor<=10:
            print(contor,x['personName']+", age =",x['age'])
            contor=contor+1
#show number of american citizens
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
#sort and show bigges philantropy scores
def philanthropy():
    print("\nTop ten highest philantropy score:\n")
    contor=1
    youngest=col.find({ "philanthropyScore": { "$exists": True } }).sort("philanthropyScore",pymongo.DESCENDING)
    for x in youngest:
        if contor<=10 or x['philanthropyScore']==5:
            print(contor,x['personName']+", philanthropyScore =",x['philanthropyScore'])
            contor=contor+1
#call functions and then delete from database
addJson()
youngest()
numberOfAmericans()
philanthropy()
col.drop()