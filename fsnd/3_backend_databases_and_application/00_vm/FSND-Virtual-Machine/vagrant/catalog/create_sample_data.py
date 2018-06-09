from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


## Adding example data

# myFirstRestaurant = Restaurant(name="Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()

# print session.query(Restaurant).all()

# cheesepizza = MenuItem(name="Cheese Pizza",
#     description="Made with all natural ingredients and fresh mozarella",
#     course="Entree",
#     price="$8.99",
#     restaurant=myFirstRestaurant)

# session.add(cheesepizza)
# session.commit()
# print session.query(MenuItem).all()

## Deleting some data (Homebrew approach, see below for way suggested by course)

# session.query(Restaurant).filter(Restaurant.id > 0).delete(synchronize_session=False)
# session.query(MenuItem).filter(MenuItem.id > 0).delete(synchronize_session=False)


## Getting Usable Data

# firstResult = session.query(Restaurant).first()
# print firstResult.name

# items = session.query(MenuItem).all()
# for item in items:
#     print item.name


## Updating Data
# veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
# for veggieBurger in veggieBurgers:
#     print veggieBurger.id
#     print veggieBurger.price
#     print veggieBurger.restaurant.name
#     print "\n"

# UrbanVeggieBurger = session.query(MenuItem).filter_by(id=12).one()
# print UrbanVeggieBurger.price
# UrbanVeggieBurger.price = '$2.99'
# session.add(UrbanVeggieBurger)
# session.commit()


## Mass-Updating Data
# veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
# for veggieBurger in veggieBurgers:
#     if veggieBurger.price != '$2.99':
#         veggieBurger.price = '$2.99'
#         session.add(veggieBurger)
#         session.commit()

# for veggieBurger in veggieBurgers:
#     print veggieBurger.id
#     print veggieBurger.price
#     print veggieBurger.restaurant.name
#     print "\n"


## Deleting some Data
# spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
# print spinach.restaurant.name
# session.delete(spinach)
# session.commit()

## Deleting Lots of Data
# Items = session.query(MenuItem)
# for i in Items:
#     session.delete(i)
#     session.commit()
