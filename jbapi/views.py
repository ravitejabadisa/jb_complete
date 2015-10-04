from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from models import Book
from models import User
from serializers import BookSerializer
from serializers import UserSerializer
import json
import traceback
import re
from django.http import StreamingHttpResponse
from oauth2client import client, crypt
from django.http import HttpResponse

@csrf_exempt
@api_view(['GET','POST'])

####LISTBOOKS FUNCTION######
#GET will list all paopular books according to pagenation
#POST the user_name and you will get the books added by that user

def listbooks(request):
    #connect to our local mongodb
    books = []
    book = []
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',12345)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']

    if request.method == 'GET':
        #get all books collection
        print "Inside GET"
        required_page= int(request.GET.get('required_page', '1'))
        books_per_page = int(request.GET.get('books_per_page', '4'))
        print required_page
        print books_per_page
        print required_page-1*books_per_page
        
        print "Going into for loop"
        for r in bookCollection.find().skip((required_page-1)*books_per_page).limit(books_per_page):
            #book = Book(r["_id"],r["name"],r["author"],r["image"],r["users"],r,r["sell_price"])
            print r["status"]
            if(r["status"] == "1"):
                book = Book(r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],[],[])
                books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print request.body

        received_json_data=json.loads(request.body)
        user_name = received_json_data.get("user_name",False)
        required_page = received_json_data.get("required_page",False)
        books_per_page = received_json_data.get("books_per_page",False)
        print "After parsing"
        print user_name
        print required_page
        book_list = userCollection.find({"user_name":user_name})
        print "Array of books is"
        #print  book_list["user_name"]
        #for index in range(len(book_list["books"])):
        for r in book_list :
            print r
            
            if(len(r["books"])!=0):
                for index in range(len(r["books"])):
                    try:
                        if(r["books"][index]["status"] =="1"):
                            book = Book(r["books"][index]["name"],r["books"][index]["description"],r["books"][index]["published_date"],r["books"][index]["status"],r["books"][index]["author"],r["books"][index]["image"],[],r["books"][index]["rent_price"],r["books"][index]["sell_price"])
                    #print r["books"][index]["author"]
                    #print book_list["books"][index]["author"]
                    except Exception as e:
                        print "Exception is"
                        print(e)
            else :
                return HttpResponse("This user hasn't added any books");
            books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
        
        
##SEARCHBOOK FUNCTION#####
#GET for a serach_parameter it can be anythiong like book name or author or description
#If user clicks on one of the results from the above get then POST the book name and you will get the list of users having that book
@api_view(['GET','POST'])
def searchbook(request):
    #connect to our local mongodb
    books = []
    users = []
    book = []
    user = []
    
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',12345)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']

    if request.method == 'GET':
        #get all books collection
        print "Inside GET"
        search_parameter = request.GET.get('search_parameter', '')
        required_page= int(request.GET.get('required_page', '1'))
        books_per_page = int(request.GET.get('books_per_page', '4'))
        
        if (search_parameter == ''):
            for r in bookCollection.find():
                if(r["status"] == "1"):
                    book = Book(r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],[],[])
                    books.append(book)
            serializedList = BookSerializer(books, many=True)
            return Response(serializedList.data)    
        else:
            print search_parameter
            print required_page
            print books_per_page
            print "Going into for loop"
           
            print "REGEX IS"
            regex = re.compile(r'.*'+search_parameter+'.*')
            print regex
            
        #for r in bookCollection.find({"name":{'$regex':new_search_parameter}}):#.skip((required_page-1)*books_per_page).limit(books_per_page):
        #print bookCollection.find({"name":{'$regex':'/C/'}})
        #for r in bookCollection.find({"name":{"$regex":new_search_parameter}}):#.skip((required_page-1)*books_per_page).limit(books_per_page):
            for r in bookCollection.find({"name":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
                #if(r["status"] =="OK")
                book = Book(r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],[],[])
                books.append(book)
                
            for r in bookCollection.find({"author":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
            #if(r["status"] =="OK")
                book = Book(r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],[],[])
                books.append(book)
            
            for r in bookCollection.find({"description":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
            #if(r["status"] =="OK")
                book = Book(r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],[],[])
                books.append(book)    
            print "before serializing"
            serializedList = BookSerializer(books, many=True)
            #print serializedList.data
            return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print request.body
        received_json_data=json.loads(request.body)
        
        name = received_json_data.get("name",False)
        user_list = bookCollection.find({"name":name})
        print "Array of USERS is"
        #print  book_list["user_name"]
        #for index in range(len(book_list["books"])):
        for r in user_list :
            #print r
            if (len(r["users"])!=0):
                for index in range(len(r["users"])):
                    try:
                    #if(r["users"][index]["status"] ==1)
                        user = User(r["users"][index]["user_name"],r["users"][index]["first_name"],r["users"][index]["last_name"],r["users"][index]["email"],r["users"][index]["phone"],r["users"][index]["home_longitude"],r["users"][index]["home_latitude"],r["users"][index]["office_longitude"],r["users"][index]["office_latitude"],r["users"][index]["rent_price"],r["users"][index]["sell_price"],[],[])
                            #print r["books"][index]["author"]
                    #print book_list["books"][index]["author"]
                    except Exception as e:
                        print "Exception is"
                        print(e)
            else:
                return HttpResponse("Book is not available as of now" )
            users.append(user)
        serializedList = UserSerializer(users, many=True)
        return Response(serializedList.data)
        

####ADDBOOK FUNCTION####
#GET method is useless as of now
#POST METHOD IS THE ACTUAL LOGIC CONTAINING ADD BOOK
@csrf_exempt      
@api_view(['GET','POST'])
def addbook(request):
    #connect to our local mongodb
    books = []
    book = []
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',12345)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']

    if request.method == 'GET':
        #get all books collection
        print "Inside GET"
        print "Going into for loop"
        for r in bookCollection.find():
            #if(r["status"] == "OK")
            book = Book(r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],[],[])
            books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print request.body
        received_json_data=json.loads(request.body)
        print received_json_data
        name = received_json_data.get("name",False)
        description = received_json_data.get("description",False)
        published_date = received_json_data.get("published_date",False)
        status = received_json_data.get("status",False)
        author = received_json_data.get("author",False)
        image = received_json_data.get("image",False)
        sell_price = received_json_data.get("sell_price",False)
        rent_price = received_json_data.get("rent_price",False)
        print name
        print author
        user_name = received_json_data.get("user_name",False)
        #first_name = received_json_data.get("first_name",False)
        #last_name = received_json_data.get("last_name",False)
        #email = received_json_data.get("email",False)
        #phone = received_json_data.get("phone",False)
        #home_longitude = received_json_data.get( "home_longitude",False)
        ##home_latitude = received_json_data.get("home_latitude",False)
        #office_longitude = received_json_data.get("office_longitude",False)
        #office_latitude = received_json_data.get("office_latitude",False)
        
        book_search = bookCollection.find({"name":name,"author": author,"image":image,"description":description,"published_date":published_date,"status" : status,"users.user_name":user_name})
        
        if( book_search.count() !=0):
            print "Inside already exists block"
            return HttpResponse("This user already has this book");
            
        print "Going into try catch block to insert books"
        
        try:
            #FInd user details of that user_name
            user_details = userCollection.find({"user_name":user_name})
            
            print user_details
            for r in user_details:
                
                #print r
                first_name = r["first_name"]
                last_name = r["last_name"]
                email = r["email"]
                phone = r["phone"]
                home_longitude = r["home_longitude"]
                home_latitude = r["home_latitude"]
                office_longitude = r["office_longitude"]
                office_latitude = r["office_latitude"]
            
            
            
            #bookCollection.insert({"name" : name, "author": author})
                bookCollection.update({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status},
                                    {'$push':
                                        {"users":{"first_name": first_name,"last_name": last_name,"email": email,"phone": phone,"user_name": user_name,"home_longitude": home_longitude,"home_latitude": home_latitude,"office_longitude": office_longitude,"office_latitude": office_latitude,"sell_price": sell_price,"rent_price": rent_price }}
                                    },True)
                                    
                userCollection.update({"first_name": first_name,"last_name": last_name,"email": email,"phone": phone,"user_name":user_name,"home_longitude": home_longitude,"home_latitude": home_latitude,"office_longitude": office_longitude,"office_latitude": office_latitude},
                                    {'$push': {"books":{"name": name,"author": author,"image": image,"description":description,"published_date":published_date,"status":status,"sell_price": sell_price,"rent_price": rent_price }}
                                    },True)
        except Exception as e:
            print(e)
            return HttpResponse("false" )
        return HttpResponse("OK")

@csrf_exempt   
@api_view(['GET','POST'])
def authenticating(request):
    #connect to our local mongodb
    print "About to Authenticate user"
    if request.method == 'GET':
        #get our collection
        print "Inside GET"
        return HttpResponse("OK")
    elif request.method == 'POST':
        #get data from the request and insert the record
        print "Inside POST"
        print request.body
        print "PRINTED PAYLOAD"
        received_json_data=json.loads(request.body)
        token = received_json_data.get("token",False)
        print token
        CLIENT_ID = "979314773329-m6j6e9la8u2o9rt15q8655uqnuuolko5.apps.googleusercontent.com"
        ANDROID_CLIENT_ID = "979314773329-e7kl7cavu9e85hclbbfscruhmtb4t685.apps.googleusercontent.com"
        IOS_CLIENT_ID = ' '
        WEB_CLIENT_ID = ' '
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)
            if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            if idinfo['hd'] != APPS_DOMAIN_NAME:
                raise crypt.AppIdentityError("Wrong hosted domain.")
        except crypt.AppIdentityError:
            traceback.print_exc()
            # Invalid token
            print "Returning Failure of user auth"
            return HttpResponse("ERROR")
        userid = idinfo['sub']
        print "Returning Success of user auth"    
        return HttpResponse(userid)
        
@csrf_exempt   
@api_view(['GET','POST'])
#GET FOR LIST OF ALL THE users
#POST FOR ADDING A NEW USER
def sign_up_and_list_users(request):
    #connect to our local mongodb
    books = []
    book = []
    users = []
    user = []
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',12345)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']
    
    print "About to Authenticate user"
    if request.method == 'GET':
        #get USERS list 
        print "Inside GET"
        print "Going into for loop"
        for r in userCollection.find():
            print r
            user = User(r["first_name"],r["last_name"],r["email"],r["phone"],r["user_name"],r["home_longitude"],r["home_latitude"],r["office_longitude"],r["office_latitude"],[],[],r["books"],r["borrowed_books"])
            users.append(user)
        serializedList = UserSerializer(users, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print "Inside POST"
        print request.body
        print "PRINTED PAYLOAD"
        received_json_data=json.loads(request.body)
        first_name = received_json_data.get("first_name",False)
        last_name = received_json_data.get("last_name",False)
        email = received_json_data.get("email",False)
        encrypted_pwd = received_json_data.get("encrypted_pwd",False) 
        user_name = received_json_data.get("user_name",False)
        home_longitude = received_json_data.get("home_longitude",False)
        home_latitude = received_json_data.get("home_latitude",False)
        office_longitude = received_json_data.get("office_longitude",False)
        office_latitude = received_json_data.get("office_latitude",False)
        phone = received_json_data.get("phone",False)
      
        try:
            userCollection.insert({"first_name":first_name,"encrypted_pwd":encrypted_pwd,"last_name":last_name,"email":email,"phone":phone,
                                   "user_name":user_name,"home_longitude":home_longitude,"home_latitude":home_latitude,
                                   "office_longitude":office_longitude,"office_latitude":office_latitude,
                                   "books":[],
                                   "borrowed_books":[]
                })
        except crypt.AppIdentityError:
            traceback.print_exc()
            # Invalid token
            print "Returning Failure of user signup"
            return HttpResponse("ERROR")
        print "Returning Success of user signup"    
        return HttpResponse(user_name)    
    

#posts.update({"_id":5678},{"$pull":{"skills":"java"}})
@csrf_exempt   
@api_view(['GET','POST'])
def perform_exchange(request):
    #connect to our local mongodb
    books = []
    book = []
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',12345)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']
    transactionCollection = dbconn['transactions']

    if request.method == 'GET':
        #get all books collection
        print "Inside GET"
        print "Going into for loop"
        for r in bookCollection.find():
            book = Book(r["_id"],r["name"],r["author"],r["image"],r["users"])
            books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print request.body
        received_json_data=json.loads(request.body)
        owner_user_name = received_json_data.get("owner_user_name",False)
        borrower_user_name = received_json_data.get("borrower_user_name",False)
        
        name = received_json_data.get("name",False) 
        description = received_json_data.get("description",False)
        published_date = received_json_data.get("published_date",False)
        status = received_json_data.get("status",False)
        author = received_json_data.get("author",False)
        image = received_json_data.get("image",False)
        sell_price = received_json_data.get("sell_price",False)
        rent_price = received_json_data.get("rent_price",False)
        print "Going into try catch block to insert transaction"
        
        
        
        try:
            #bookCollection.insert({"name" : name, "author": author})
            #posts.update({"_id":5678},{"$pull":{"skills":"java"}})
            #for r in bookCollection.find({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status}):
            #    print r
            #for s in userCollection.find({"user_name":owner_user_name}):
            #    print s
            bookCollection.update({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status},{'$pull': {"users":{"user_name":owner_user_name}}})
            userCollection.update({"user_name":owner_user_name},{'$pull': {"books":{"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status }}})
            userCollection.update({"user_name":borrower_user_name},{'$push': {"borrowed_books":{"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status }}})
            transactionCollection.insert({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status,"rent_price":rent_price,"sell_price":sell_price,"borrower_user_name":borrower_user_name,"owner_user_name":owner_user_name})
        except Exception as e:
            print(e)
            return HttpResponse("false" )
        return HttpResponse("OK")
""" COMMENTED OUT
@csrf_exempt        
def authenticating(request):
    #connect to our local mongodb
    print "About to Authenticate user"
    if request.method == 'GET':
        #get our collection
        print "Inside GET"
        return HttpResponse("OK")
    elif request.method == 'POST':
        #get data from the request and insert the record
        print "Inside POST"
        print request.body
        print "PRINTED PAYLOAD"
        received_json_data=json.loads(request.body)
        token = received_json_data.get("token",False)
        print token
        CLIENT_ID = "979314773329-m6j6e9la8u2o9rt15q8655uqnuuolko5.apps.googleusercontent.com"
        ANDROID_CLIENT_ID = "979314773329-e7kl7cavu9e85hclbbfscruhmtb4t685.apps.googleusercontent.com"
        IOS_CLIENT_ID = ' '
        WEB_CLIENT_ID = ' '
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)
            if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            if idinfo['hd'] != APPS_DOMAIN_NAME:
                raise crypt.AppIdentityError("Wrong hosted domain.")
        except crypt.AppIdentityError:
            traceback.print_exc()
            # Invalid token
            print "Returning Failure of user auth"
            return HttpResponse("ERROR")
        userid = idinfo['sub']
        print "Returning Success of user auth"    
        return HttpResponse(userid)
"""
