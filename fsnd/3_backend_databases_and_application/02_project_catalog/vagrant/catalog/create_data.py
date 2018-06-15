"""
    File name: create_data.py
    Author: Christian Eik
    Date created: 2018-06-10
    Date last modified: 2018-06-15
    Python Version: 2.7

    Populate the catalog_project database with some sample data.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base
from database_setup import Users, Categories, Products, ProductsCategories

engine = create_engine('sqlite:///catalog_project.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Users
User1 = Users(name="Homer Simpson", email="homer@simpsons.com")
session.add(User1)
session.commit()

User2 = Users(name="Marge Simpson", email="marge@simpsons.com")
session.add(User2)
session.commit()

# Categories
Cat1 = Categories(name="Clothing")
session.add(Cat1)
session.commit()

SubCat1 = Categories(name="T-Shirts", parent_id=Cat1.id)
session.add(SubCat1)
session.commit()

SubCat2 = Categories(name="Pants", parent_id=Cat1.id)
session.add(SubCat2)
session.commit()

SubCat3 = Categories(name="Swimwear", parent_id=Cat1.id)
session.add(SubCat3)
session.commit()

Cat2 = Categories(name="Shoes")
session.add(Cat2)
session.commit()

SubCat4 = Categories(name="Running", parent_id=Cat2.id)
session.add(SubCat4)
session.commit()

SubCat5 = Categories(name="Indoor", parent_id=Cat2.id)
session.add(SubCat5)
session.commit()

Cat3 = Categories(name="Gear")
session.add(Cat3)
session.commit()

SubCat8 = Categories(name="Swimming", parent_id=Cat3.id)
session.add(SubCat8)
session.commit()

SubSubCat1 = Categories(name="Goggles", parent_id=SubCat8.id)
session.add(SubSubCat1)
session.commit()

SubSubCat2 = Categories(name="Speedos", parent_id=SubCat8.id)
session.add(SubSubCat2)
session.commit()

SubCat9 = Categories(name="Handball", parent_id=Cat3.id)
session.add(SubCat9)
session.commit()

SubSubCat3 = Categories(name="Balls", parent_id=SubCat9.id)
session.add(SubSubCat3)
session.commit()

SubSubCat4 = Categories(name="Resin", parent_id=SubCat9.id)
session.add(SubSubCat4)
session.commit()

SubSubCat5 = Categories(name="Handball Shoes", parent_id=SubCat9.id)
session.add(SubSubCat5)
session.commit()

# Products
Pd1 = Products(name="Black T-Shirt", description="It's a black T-Shirt",
               price_cents=2999, creator=User1)
session.add(Pd1)
session.commit()

Pd2 = Products(name="Blue T-Shirt", description="It's a blue T-Shirt",
               price_cents=3999, creator=User2)
session.add(Pd2)
session.commit()

Pd3 = Products(name="Long Pants", description="These pants are long",
               price_cents=3999, creator=User1)
session.add(Pd3)
session.commit()

Pd4 = Products(name="Short Pants", description="So short...",
               price_cents=4999, creator=User2)
session.add(Pd4)
session.commit()

Pd5 = Products(name="Speedos", description="Extra thight",
               price_cents=2499, creator=User1)
session.add(Pd5)
session.commit()

Pd6 = Products(name="Baggy Speedos", description="JK, still tight",
               price_cents=2499, creator=User1)
session.add(Pd6)
session.commit()

Pd7 = Products(name="Running Shoe 1", description="Even comes in pairs",
               price_cents=7999, creator=User1)
session.add(Pd7)
session.commit()

Pd8 = Products(name="Running Shoe 2", description="Velcro, but laces included",
               price_cents=8999, creator=User2)
session.add(Pd8)
session.commit()

Pd9 = Products(name="Handball Shoe 1", description="Green",
               price_cents=8999, creator=User1)
session.add(Pd9)
session.commit()

Pd10 = Products(name="Handball Shoe 2", description="Blue",
                price_cents=9999, creator=User2)
session.add(Pd10)
session.commit()

Pd11 = Products(name="Goggles 1", description="Toxic when wet",
                price_cents=2499, creator=User1)
session.add(Pd11)
session.commit()

Pd12 = Products(name="Swimming Monocle", description="Still in season",
                price_cents=1499, creator=User1)
session.add(Pd12)
session.commit()

Pd13 = Products(name="Handball... Ball", description="Round",
                price_cents=4999, creator=User2)
session.add(Pd13)
session.commit()

Pd14 = Products(name="Super Sticky Resin", description="150g",
                price_cents=999, creator=User1)
session.add(Pd14)
session.commit()

Pd15 = Products(name="Resin", description="200g",
                price_cents=1199, creator=User1)
session.add(Pd15)
session.commit()

# Product Categories
PC1 = ProductsCategories(product=Pd1, category=SubCat1, creator=User1)
session.add(PC1)
session.commit()

PC2 = ProductsCategories(product=Pd1, category=Cat1, creator=User1)
session.add(PC2)
session.commit()

PC3 = ProductsCategories(product=Pd2, category=SubCat1, creator=User1)
session.add(PC3)
session.commit()

PC4 = ProductsCategories(product=Pd2, category=Cat1, creator=User1)
session.add(PC4)
session.commit()

PC5 = ProductsCategories(product=Pd3, category=SubCat2, creator=User1)
session.add(PC5)
session.commit()

PC6 = ProductsCategories(product=Pd3, category=Cat1, creator=User1)
session.add(PC6)
session.commit()

PC7 = ProductsCategories(product=Pd4, category=SubCat2, creator=User1)
session.add(PC7)
session.commit()

PC8 = ProductsCategories(product=Pd4, category=Cat1, creator=User1)
session.add(PC8)
session.commit()

PC9 = ProductsCategories(product=Pd5, category=SubCat3, creator=User1)
session.add(PC9)
session.commit()

PC10 = ProductsCategories(product=Pd5, category=Cat1, creator=User1)
session.add(PC10)
session.commit()

PC11 = ProductsCategories(product=Pd5, category=SubSubCat2, creator=User1)
session.add(PC11)
session.commit()

PC12 = ProductsCategories(product=Pd5, category=SubCat8, creator=User1)
session.add(PC12)
session.commit()

PC13 = ProductsCategories(product=Pd5, category=Cat3, creator=User1)
session.add(PC13)
session.commit()

PC14 = ProductsCategories(product=Pd6, category=SubCat3, creator=User1)
session.add(PC14)
session.commit()

PC15 = ProductsCategories(product=Pd6, category=Cat1, creator=User1)
session.add(PC15)
session.commit()

PC16 = ProductsCategories(product=Pd6, category=SubSubCat2, creator=User1)
session.add(PC16)
session.commit()

PC17 = ProductsCategories(product=Pd6, category=SubCat8, creator=User1)
session.add(PC17)
session.commit()

PC18 = ProductsCategories(product=Pd6, category=Cat3, creator=User1)
session.add(PC18)
session.commit()

PC19 = ProductsCategories(product=Pd7, category=SubCat4, creator=User1)
session.add(PC19)
session.commit()

PC20 = ProductsCategories(product=Pd7, category=Cat2, creator=User1)
session.add(PC20)
session.commit()

PC21 = ProductsCategories(product=Pd8, category=SubCat4, creator=User1)
session.add(PC21)
session.commit()

PC22 = ProductsCategories(product=Pd8, category=Cat2, creator=User1)
session.add(PC22)
session.commit()

PC23 = ProductsCategories(product=Pd9, category=SubCat5, creator=User1)
session.add(PC23)
session.commit()

PC24 = ProductsCategories(product=Pd9, category=Cat2, creator=User1)
session.add(PC24)
session.commit()

PC25 = ProductsCategories(product=Pd9, category=SubSubCat5, creator=User1)
session.add(PC25)
session.commit()

PC26 = ProductsCategories(product=Pd9, category=SubCat9, creator=User1)
session.add(PC26)
session.commit()

PC27 = ProductsCategories(product=Pd9, category=Cat3, creator=User1)
session.add(PC27)
session.commit()

PC28 = ProductsCategories(product=Pd10, category=SubCat5, creator=User1)
session.add(PC28)
session.commit()

PC29 = ProductsCategories(product=Pd10, category=Cat2, creator=User1)
session.add(PC29)
session.commit()

PC30 = ProductsCategories(product=Pd10, category=SubSubCat5, creator=User1)
session.add(PC30)
session.commit()

PC31 = ProductsCategories(product=Pd10, category=SubCat9, creator=User1)
session.add(PC31)
session.commit()

PC32 = ProductsCategories(product=Pd10, category=Cat3, creator=User1)
session.add(PC32)
session.commit()

PC33 = ProductsCategories(product=Pd11, category=SubSubCat1, creator=User1)
session.add(PC33)
session.commit()

PC34 = ProductsCategories(product=Pd11, category=SubCat8, creator=User1)
session.add(PC34)
session.commit()

PC35 = ProductsCategories(product=Pd11, category=Cat3, creator=User1)
session.add(PC35)
session.commit()

PC36 = ProductsCategories(product=Pd12, category=SubSubCat1, creator=User1)
session.add(PC36)
session.commit()

PC37 = ProductsCategories(product=Pd12, category=SubCat8, creator=User1)
session.add(PC37)
session.commit()

PC38 = ProductsCategories(product=Pd12, category=Cat3, creator=User1)
session.add(PC38)
session.commit()

PC39 = ProductsCategories(product=Pd13, category=SubSubCat3, creator=User1)
session.add(PC39)
session.commit()

PC40 = ProductsCategories(product=Pd13, category=SubCat9, creator=User1)
session.add(PC40)
session.commit()

PC41 = ProductsCategories(product=Pd13, category=Cat3, creator=User1)
session.add(PC41)
session.commit()

PC42 = ProductsCategories(product=Pd14, category=SubSubCat4, creator=User1)
session.add(PC42)
session.commit()

PC43 = ProductsCategories(product=Pd14, category=SubCat9, creator=User1)
session.add(PC43)
session.commit()

PC44 = ProductsCategories(product=Pd14, category=Cat3, creator=User1)
session.add(PC44)
session.commit()

PC45 = ProductsCategories(product=Pd15, category=SubSubCat4, creator=User1)
session.add(PC45)
session.commit()

PC46 = ProductsCategories(product=Pd15, category=SubCat9, creator=User1)
session.add(PC46)
session.commit()

PC47 = ProductsCategories(product=Pd15, category=Cat3, creator=User1)
session.add(PC47)
session.commit()


print("database populated")
