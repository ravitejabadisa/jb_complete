from rest_framework import serializers
from models import Book
from models import User


class Basic_UserSerializer(serializers.Serializer):

    user_name = serializers.CharField(required=True, max_length=200)
    home_longitude = serializers.CharField(required=True, max_length=200)
    home_latitude = serializers.CharField(required=True, max_length=200)
    office_longitude = serializers.CharField(required=True, max_length=200)
    office_latitude = serializers.CharField(required=True, max_length=200)
    rent_price = serializers.CharField(required=False, max_length=200)
    sell_price = serializers.CharField(required=False, max_length=200)
    first_name = serializers.CharField(required=False, max_length=200)
    last_name = serializers.CharField(required=False, max_length=200)
    email = serializers.CharField(required=False, max_length=200)
    phone = serializers.CharField(required=False, max_length=15)
    

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.user_name = attrs.get('user_name', instance.user_name)
            instance.home_longitude = attrs.get('home_longitude', instance.home_longitude)
            instance.home_latitude = attrs.get('home_latitude', instance.home_latitude)
            instance.office_longitude = attrs.get('office_longitude', instance.office_longitude)
            instance.office_latitude = attrs.get('office_latitude', instance.office_latitude)
            instance.rent_price= attrs.get('rent_price', instance.rent_price)
            instance.sell_price= attrs.get('sell_price', instance.sell_price)
            instance.first_name= attrs.get('first_name', instance.first_name)
            instance.last_name= attrs.get('last_name', instance.last_name)
            instance.email= attrs.get('email', instance.email)
            instance.phone= attrs.get('phone', instance.phone)
            return instance

        return Basic_User(attrs.get('first_name'),attrs.get('last_name'),attrs.get('email'),attrs.get('phone'),attrs.get('user_name'),attrs.get('home_longitude'),attrs.get('home_latitude'),attrs.get('office_longitude'),attrs.get('office_latitude'),attrs.get('rent_price'),attrs.get('sell_price'))     


class BookSerializer(serializers.Serializer):
    #id = serializers.CharField(required=True, max_length=50)
    name = serializers.CharField(required=True, max_length=100)
    author = serializers.CharField(required=True, max_length=200)
    image = serializers.CharField(required=True, max_length=200)
    rent_price = serializers.CharField(required=False, max_length=200)
    sell_price = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False, max_length=200)
    published_date = serializers.CharField(required=False, max_length=200)
    status = serializers.CharField(required=False, max_length=200)
    users = Basic_UserSerializer(required=False, many=True)
    
    def restore_object(self, attrs, instance=None):
        if instance:
            
            #instance.id = attrs.get('id', instance.id)
            instance.name = attrs.get('name', instance.name)
            instance.author = attrs.get('author', instance.author)
            instance.image = attrs.get('image', instance.image)
            instance.users= attrs.get('users', instance.users)
            instance.rent_price= attrs.get('rent_price', instance.rent_price)
            instance.sell_price= attrs.get('sell_price', instance.sell_price)
            instance.description= attrs.get('description', instance.description)
            instance.published_date= attrs.get('published_date', instance.published_date)
            instance.status= attrs.get('status', instance.status)
            instance.users= attrs.get('users', instance.users)
            
            return instance

        return Book(attrs.get('name'),attrs.get('description'),attrs.get('published_date'),attrs.get('status'),attrs.get('author'),attrs.get('image'),attrs.get('users'),attrs.get('rent_price'),attrs.get('sell_price'))

class UserSerializer(serializers.Serializer):

    user_name = serializers.CharField(required=True, max_length=200)
    home_longitude = serializers.CharField(required=True, max_length=200)
    home_latitude = serializers.CharField(required=True, max_length=200)
    office_longitude = serializers.CharField(required=True, max_length=200)
    office_latitude = serializers.CharField(required=True, max_length=200)
    rent_price = serializers.CharField(required=False, max_length=200)
    sell_price = serializers.CharField(required=False, max_length=200)
    first_name = serializers.CharField(required=False, max_length=200)
    last_name = serializers.CharField(required=False, max_length=200)
    email = serializers.CharField(required=False, max_length=200)
    phone = serializers.CharField(required=False, max_length=15)
    books = BookSerializer(required=False, many=True)
    borrowed_books = BookSerializer(required=False, many=True)
    

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.user_name = attrs.get('user_name', instance.user_name)
            instance.home_longitude = attrs.get('home_longitude', instance.home_longitude)
            instance.home_latitude = attrs.get('home_latitude', instance.home_latitude)
            instance.office_longitude = attrs.get('office_longitude', instance.office_longitude)
            instance.office_latitude = attrs.get('office_latitude', instance.office_latitude)
            instance.rent_price= attrs.get('rent_price', instance.rent_price)
            instance.sell_price= attrs.get('sell_price', instance.sell_price)
            instance.books= attrs.get('books', instance.books)
            instance.first_name= attrs.get('first_name', instance.first_name)
            instance.last_name= attrs.get('last_name', instance.last_name)
            instance.email= attrs.get('email', instance.email)
            instance.phone= attrs.get('phone', instance.phone)
            instance.borrowed_books = attrs.get('borrowed_books', instance.borrowed_books)
            return instance

        return User(attrs.get('first_name'),attrs.get('last_name'),attrs.get('email'),attrs.get('phone'),attrs.get('user_name'),attrs.get('home_longitude'),attrs.get('home_latitude'),attrs.get('office_longitude'),attrs.get('office_latitude'),attrs.get('rent_price'),attrs.get('sell_price'),attrs.get('books'),attrs.get('borrowed_books'))     
"""COMMENTED OUT
class User_having_books_Serializer(serializers.Serializer):
    user_name = serializers.CharField(required=True, max_length=200)
    home_longitude = serializers.CharField(required=True, max_length=200)
    home_latitude = serializers.CharField(required=True, max_length=200)
    office_longitude = serializers.CharField(required=True, max_length=200)
    office_latitude = serializers.CharField(required=True, max_length=200)
    rent_price = serializers.CharField(required=False, max_length=200)
    sell_price = serializers.CharField(required=False, max_length=200)
    books = BookSerializer(required=False, many=True)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.user_name = attrs.get('user_name', instance.user_name)
            instance.home_longitude = attrs.get('home_longitude', instance.home_longitude)
            instance.home_latitude = attrs.get('home_latitude', instance.home_latitude)
            instance.office_longitude = attrs.get('office_longitude', instance.office_longitude)
            instance.office_latitude = attrs.get('office_latitude', instance.office_latitude)
            instance.rent_price= attrs.get('rent_price', instance.rent_price)
            instance.sell_price= attrs.get('sell_price', instance.sell_price)
            instance.books = attrs.get('books', instance.books)
            return instance

        return User(attrs.get('id'),attrs.get('user_name'),attrs.get('home_longitude'),attrs.get('home_latitude'),attrs.get('office_longitude'),attrs.get('office_latitude'),attrs.get('rent_price'),attrs.get('sell_price'),attrs.get('books'))

class Book_having_users_Serializer(serializers.Serializer):
    
    users = UserSerializer(required=False, many=True)
    id = serializers.CharField(required=True, max_length=50)
    name = serializers.CharField(required=True, max_length=100)
    author = serializers.CharField(required=True, max_length=200)
    image = serializers.CharField(required=True, max_length=200)
    rent_price = serializers.CharField(required=False, max_length=200)
    sell_price = serializers.CharField(required=False, max_length=200)
    

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.id = attrs.get('id', instance.id)
            instance.name = attrs.get('name', instance.name)
            instance.author = attrs.get('author', instance.author)
            instance.image = attrs.get('image', instance.image)
            instance.users= attrs.get('users', instance.users)
            instance.rent_price= attrs.get('rent_price', instance.rent_price)
            instance.sell_price= attrs.get('sell_price', instance.sell_price)
            return instance

        return Book(attrs.get('id'),attrs.get('name'),attrs.get('author'),attrs.get('image'),attrs.get('users'),attrs.get('rent_price'),attrs.get('sell_price'))
 """       
   
        
        