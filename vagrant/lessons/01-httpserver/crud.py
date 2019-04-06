from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

def connect():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    print("Ok")
    print(session)
    return session

def listAll(dbs):
    # restaurant1 = Restaurant(name="Urban Burger")
    print("Entrou em list")
    items = dbs.query(Restaurant).all()
    for item in items:
        print (item.name)
    return items

def listOne(dbs, search):
    print("listone - search: ", search)
    queryResult = dbs.query(Restaurant).filter_by(id = search).first() 
    print("listOne - queryResult: ", queryResult)
    return queryResult

def updateOne(dbs, search, result):
    queryResult = dbs.query(Restaurant).filter_by(id = search).one() 
    queryResult.name = result
    dbs.add(queryResult)
    dbs.commit()
    # print("Eita Porra: ", restaurantName.name)
    return queryResult.name

def create(dbs, result):
    print("Entrou no Create: ", result)
    newRestaurant = Restaurant(name = result)
    dbs.add(newRestaurant)
    dbs.commit()
    return True

def deleteOne(dbs, target):
    print("Entrou no Delete: ", target)
    targetRestaurant = dbs.query(Restaurant).filter_by(id = target).one()
    dbs.delete(targetRestaurant)
    dbs.commit()