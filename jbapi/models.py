from django.db import models

# Create your models here.
class Basic_User(object):
    def __init__(self, first_name,last_name,email,phone,qbuserid,user_name,string_home_address,string_office_address, home_longitude, home_latitude,office_longitude, office_latitude,rent_price,sell_price):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.string_home_address = string_home_address
        self.string_office_address = string_office_address
        self.home_longitude = home_longitude
        self.home_latitude = home_latitude
        self.office_longitude = office_longitude
        self.office_latitude = office_latitude
        self.rent_price = rent_price
        self.sell_price = sell_price
        self.qbuserid = qbuserid
        
class User(object):
    def __init__(self, first_name,last_name,email,phone,qbuserid,user_name,string_home_address,string_office_address, home_longitude, home_latitude,office_longitude, office_latitude,rent_price,sell_price,books,borrowed_books):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.string_home_address = string_home_address
        self.string_office_address = string_office_address
        self.home_longitude = home_longitude
        self.home_latitude = home_latitude
        self.office_longitude = office_longitude
        self.office_latitude = office_latitude
        self.rent_price = rent_price
        self.sell_price = sell_price
        self.books = books
        self.borrowed_books = borrowed_books
        self.qbuserid = qbuserid

class Book(object):
    def __init__(self, name, description,published_date,category,isbn,status,author,image ,users,rent_price,sell_price):
        
        self.description = description
        self.published_date = published_date
        self.status = status
        self.name = name
        self.author = author
        self.image = image
        self.users = users
        self.rent_price = rent_price
        self.sell_price = sell_price
        self.category = category
        self.isbn = isbn
        
        
