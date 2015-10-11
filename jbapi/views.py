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
import datetime
from django.http import StreamingHttpResponse
from oauth2client import client, crypt
from django.http import HttpResponse



@csrf_exempt   
@api_view(['GET','POST'])
###AUTHENTICATING FUNCTION#############
#GET ->Does nothing
#POST ->expects a a json containing token used for verification

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
        CLIENT_ID = "blah.apps.googleusercontent.com"
        ANDROID_CLIENT_ID = "blah.apps.googleusercontent.com"
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
###AUTHENTICATING FUNCTION#############
#GET ->Does nothing
#POST ->expects a a json containing token used for verification

def distance(latitude1,latitude2,longitude1,longitude2):
    #connect to our local mongodb
    print "About to caluculate distancer"
    distance = (latitude1-latitude2)    
    return HttpResponse("Hello")        



@csrf_exempt
@api_view(['GET','PUT','POST','DELETE'])

####LISTBOOKS FUNCTION######
#GET 
    #1->leave the parameters search_parameter and category empty it will list all paopular books according to pagenation(10 books per page...or else you can set by setting books_per_page)
    #2->set a parameter category = some category that will list all books of that category according to pagenation(10 books per page...or else you can set by setting books_per_page)
    #3->set a parameter search_parameter  and leave category empty that will result all the books containingthat search_parameter
#POST
    #1->set a parameter changes = "BOOKS_OF_USER" and POST the user_name and you will get the books added by that user
    #2->set a parameter changes = "ADD_BOOK" and POST all the book details and user_name the book will be added to the database
#PUT is for updating the book send all parameters of the book and user_name and set a parameter changes = "UPDATE" in the PUT request
#DELETE is for deleteing ta book send all parameters of the book and user_name and set a parameter changes = "BOOK_DELETE" in DELETE request 

def list_search_modify_books(request):
    #connect to our local mongodb
    books = []
    book = []
    print "About to request Connection"
    mongoserver_uri = "blah"
    db = MongoClient(host=mongoserver_uri)
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
        books_per_page = int(request.GET.get('books_per_page', '10'))
        category = request.GET.get('category', '')
        
        if (search_parameter == ''):
            print required_page
            print books_per_page
            print (required_page-1)*books_per_page
        
            print "Going into for loop"
            a = datetime.datetime.now()
            for r in bookCollection.find().skip((required_page-1)*books_per_page).limit(books_per_page):
                #book = Book(r["_id"],r["name"],r["author"],r["image"],r["users"],r,r["sell_price"])
                #print r.count()
                if(r["status"] != "0" or r["status"] != 0):
                    print "Inside IF"
                    print r["status"]
                    book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
                    books.append(book)
            serializedList = BookSerializer(books, many=True)
            b = datetime.datetime.now()
            print "Time Taken from django to mongo is::"
            print(b-a)
            return Response(serializedList.data)
        
        elif category !='':
            for r in bookCollection.find({"category":category}).skip((required_page-1)*books_per_page).limit(books_per_page):
                #book = Book(r["_id"],r["name"],r["author"],r["image"],r["users"],r,r["sell_price"])
                #print r.count()
                if(r["status"] != "0" or r["status"] != 0):
                    print "Inside IF"
                    print r["status"]
                    book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
                    books.append(book)
            serializedList = BookSerializer(books, many=True)
            return Response(serializedList.data)
            
        else:
            print search_parameter
            print required_page
            print books_per_page
            print "Going into for loop"
           
            print "REGEX IS"
            regex = re.compile(r'.*'+search_parameter+'.*',re.IGNORECASE)
            print regex
            print regex.pattern
            
        #for r in bookCollection.find({"name":{'$regex':new_search_parameter}}):#.skip((required_page-1)*books_per_page).limit(books_per_page):
        #print bookCollection.find({"name":{'$regex':'/C/'}})
        #for r in bookCollection.find({"name":{"$regex":new_search_parameter}}):#.skip((required_page-1)*books_per_page).limit(books_per_page):
            try:
                for r in bookCollection.find({"$or":[{"name":regex},{"author":regex}]}).skip((required_page-1)*books_per_page).limit(books_per_page):
                    book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
                    books.append(book)
                print "before serializing"
                serializedList = BookSerializer(books, many=True)
                #print serializedList.data
                return Response(serializedList.data)    
            except Exception as e:
                print(e)
                return HttpResponse("Error in searching")
            
    elif request.method == 'POST':
        #get data from the request and insert the record
        #print request.body

        received_json_data=json.loads(request.body)
        changes = received_json_data.get("changes",False)
        
        if (changes == "ADD_BOOK"):
            name = received_json_data.get("name",False)
            description = received_json_data.get("description",False)
            published_date = received_json_data.get("published_date",False)
            status = received_json_data.get("status",False)
            author = received_json_data.get("author",False)
            image = received_json_data.get("image",False)
            sell_price = received_json_data.get("sell_price",False)
            rent_price = received_json_data.get("rent_price",False)
            category = received_json_data.get("category",False)
            isbn = received_json_data.get("isbn",False)
            print name
            print author
            user_name = received_json_data.get("user_name",False)
            
            book_search = bookCollection.find({"name":name,"author": author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status" : status,"users.user_name":user_name})
        
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
                    string_home_address = r["string_home_address"]
                    string_office_address = r["string_office_address"]
            
            
            
            #bookCollection.insert({"name" : name, "author": author})
                    bookCollection.update({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status":status},
                                        {'$push':
                                            {"users":{"first_name": first_name,"last_name": last_name,"email": email,"phone": phone,"qbuserid":qbuserid,"user_name": user_name,"string_home_address":string_home_address,"string_office_address":string_office_address,"home_longitude": home_longitude,"home_latitude": home_latitude,"office_longitude": office_longitude,"office_latitude": office_latitude,"sell_price": sell_price,"rent_price": rent_price }}
                                        },True)
                                    
                    userCollection.update({"first_name": first_name,"last_name": last_name,"email": email,"phone": phone,"qbuserid":qbuserid,"user_name":user_name,"string_home_address":string_home_address,"string_office_address":string_office_address,"home_longitude": home_longitude,"home_latitude": home_latitude,"office_longitude": office_longitude,"office_latitude": office_latitude},
                                        {'$push': {"books":{"name": name,"author": author,"image": image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status":status,"sell_price": sell_price,"rent_price": rent_price }}
                                        },True)
            except Exception as e:
                print(e)
                return HttpResponse("false" )
            return HttpResponse("OK")
            
            
        
        
        elif changes == "BOOKS_OF_USER":
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
                #print r
            
                if(len(r["books"])!=0):
                    for index in range(len(r["books"])):
                        try:
                            if(r["books"][index]["status"] =="1"):
                                book = Book(r["books"][index]["name"],r["books"][index]["description"],r["books"][index]["published_date"],r["books"][index]["category"],r["books"][index]["isbn"],r["books"][index]["status"],r["books"][index]["author"],r["books"][index]["image"],[],r["books"][index]["rent_price"],r["books"][index]["sell_price"])
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
        
    elif request.method == 'PUT':
        received_json_data=json.loads(request.body)
        #print received_json_data
        name = received_json_data.get("name",False)
        description = received_json_data.get("description",False)
        published_date = received_json_data.get("published_date",False)
        status = received_json_data.get("status",False)
        author = received_json_data.get("author",False)
        image = received_json_data.get("image",False)
        sell_price = received_json_data.get("sell_price",False)
        rent_price = received_json_data.get("rent_price",False)
        category = received_json_data.get("category",False)
        isbn = received_json_data.get("isbn",False)
        print name
        print author
        user_name = received_json_data.get("user_name",False)
        
        changes = received_json_data.get("changes",False)
        
        if(changes == "UPDATE"):
            try:
                
                bookCollection.update({"name":name,"author": author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status" : status,"users.user_name":user_name},
                                        {'$set':{"users.$.sell_price":sell_price,"users.$.rent_price":rent_price}})
            except Exception as e:
                        print "Exception is"
                        print(e)
                        return HttpResponse("Some exception happened")
            return HttpResponse("Book details are updated")
        else:    
            return HttpResponse("Please set the changed as UPDATE")
    elif request.method == 'DELETE':
        received_json_data=json.loads(request.body)
        #print received_json_data
        name = received_json_data.get("name",False)
        #description = received_json_data.get("description",False)
        #published_date = received_json_data.get("published_date",False)
        #status = received_json_data.get("status",False)
        author = received_json_data.get("author",False)
        #image = received_json_data.get("image",False)
        #sell_price = received_json_data.get("sell_price",False)
        #rent_price = received_json_data.get("rent_price",False)
        #category = received_json_data.get("category",False)
        #isbn = received_json_data.get("isbn",False)
        print name
        print author
        user_name = received_json_data.get("user_name",False)
        print "going to delete book of:"
        print user_name
        print name
        print author
        changes = received_json_data.get("changes",False)
        
        if(changes == "BOOK_DELETE"):
            
            try:
                userCollection.update({"user_name":user_name},
                                            {'$pull': {"books":{"name" : name, "author": author }}})
                bookCollection.update({"name" : name, "author": author},
                                        {'$pull':{"users":{"user_name":user_name}}})
                                        
                #a=bookCollection.find({"name":name,"author": author,"users" : {'$exists': True}, '$where' : "this.users.length = 0"})
                books_with_no_users=bookCollection.find({"name":name,"author": author,"users" : {'$exists': True}, '$where' : "this.users.length == 0"})
                if( books_with_no_users.count() !=0):
                    print "Inside no user book exists"
                    for r in books_with_no_users:
                        bookCollection.remove({"name":r["name"],"author":r["author"]})
                        #print r["name"]
                #return HttpResponse("This user already has this book");
                #print r["name"]
                
                         #db.books.update({"name": "TestWithStrin0g","author": "tester2"},
                                         # {$pull:{"users":{"user_name":"hij"}}})  
            except Exception as e:
                    print "Exception is"
                    print(e)
                    return HttpResponse("Some exception happened")
            return HttpResponse("Book is deleted from user's collection")
        
        else:  
            return HttpResponse("Please set the changed as BOOK_DELETE")
        
@csrf_exempt   
@api_view(['GET','PUT','DELETE','POST'])
####SIGN_UP_EDIT_AND _LIST_USERS  FUNCTION######
#GET 
    #1->leave the parameter requirement empty it will list all USERS AND DETAILS  according to pagenation(10 users per page...or else you can set by setting users_per_page)
    #2->Set a parameter requirement = "DETAILS" and add parameter user_name to get the details of that USER_NAME
    #3->Set a parameter requirement = "USER_NAMES" it will list all USERS(with their user_name only) according to pagenation(10 users per page...or else you can set by setting users_per_page)
#POST
    #1->set the parameter name empty then this method expects a user details json and adds that user to the database(Actual signup)
    #2->set the parameter name = book name of some book to get the details of list of users having that book
#PUT is for updating the user details in both user collection and books collection send all parameters of the user along with old and updated ones
    #1->You should send the old_user_name and new_user_name (If user_name is same also send both parameters with same value)
     #&->Send all the other details as new_phone(If not changed send old values only.If changed send new values)
#DELETE 

def sign_up_edit_and_list_users(request):
    #connect to our local mongodb
    books = []
    book = []
    users = []
    user = []
    print "About to request Connection"
    mongoserver_uri = "blah"
    db = MongoClient(host=mongoserver_uri)
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
        
        requirement = request.GET.get('requirement', '')
        required_page= int(request.GET.get('required_page', '1'))
        books_per_page = int(request.GET.get('books_per_page', '10'))
        
        if(requirement == ''):
            for r in userCollection.find().skip((required_page-1)*books_per_page).limit(books_per_page):
                print r
                user = User(r["first_name"],r["last_name"],r["email"],r["phone"],r["qbuserid"],r["user_name"],r["string_home_address"],r["string_office_address"],r["home_longitude"],r["home_latitude"],r["office_longitude"],r["office_latitude"],[],[],r["books"],r["borrowed_books"])
                users.append(user)
            serializedList = UserSerializer(users, many=True)
            return Response(serializedList.data)
        elif requirement == "DETAILS" :
            user_name = received_json_data.get("user_name",False)
            for r in userCollection.find({"user_name":user_name}):
                print r
                user = User(r["first_name"],r["last_name"],r["email"],r["phone"],r["qbuserid"],r["user_name"],r["string_home_address"],r["string_office_address"],r["home_longitude"],r["home_latitude"],r["office_longitude"],r["office_latitude"],[],[],r["books"],r["borrowed_books"])
                users.append(user)
            serializedList = UserSerializer(users, many=True)
            return Response(serializedList.data)
            
        elif requirement == "USER_NAMES":
            for r in userCollection.find().skip((required_page-1)*books_per_page).limit(books_per_page):
                print r
                user = User([],[],[],[],r["user_name"],[],[],[],[],[],[],[],[])
                users.append(user)
            serializedList = UserSerializer(users, many=True)
            return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print "Inside POST"
        print request.body
        print "PRINTED PAYLOAD"
        received_json_data=json.loads(request.body)
        name = received_json_data.get("name",False)
        
        if(name == '' or name == False):
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
            string_home_address = received_json_data.get("string_home_address",False)
            string_office_address = received_json_data.get("string_office_address",False)
            qbuserid = received_json_data.get("qbuserid",False)
            
          
            try:
                userCollection.insert({"first_name":first_name,"encrypted_pwd":encrypted_pwd,"last_name":last_name,"email":email,"phone":phone,"qbuserid":qbuserid,
                                    "user_name":user_name,"string_home_address":string_home_address,"string_office_address":string_office_address,
                                    "home_longitude":home_longitude,"home_latitude":home_latitude,
                                    "office_longitude":office_longitude,"office_latitude":office_latitude,
                                    "books":[],
                                    "borrowed_books":[]
                    })
            except Exception as e:
                    print "Exception is"
                    print(e)
                    return HttpResponse("Some error in signup")
            print "Returning Success of user signup"    
            return HttpResponse(user_name)
        else:
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
                            user = User(r["users"][index]["first_name"],r["users"][index]["last_name"],r["users"][index]["email"],r["users"][index]["phone"],r["users"][index]["qbuserid"],r["users"][index]["user_name"],r["users"][index]["string_home_address"],r["users"][index]["string_office_address"],r["users"][index]["home_longitude"],r["users"][index]["home_latitude"],r["users"][index]["office_longitude"],r["users"][index]["office_latitude"],r["users"][index]["rent_price"],r["users"][index]["sell_price"],[],[])
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
        
    elif request.method == 'PUT':
        print "Inside PUT"
        print request.body
        print "PRINTED PAYLOAD"
        received_json_data=json.loads(request.body)
        new_first_name = received_json_data.get("new_first_name",False)
        new_last_name = received_json_data.get("new_last_name",False)
        new_email = received_json_data.get("new_email",False)
        new_encrypted_pwd = received_json_data.get("new_encrypted_pwd",False) 
        new_user_name = received_json_data.get("new_user_name",False)
        old_user_name = received_json_data.get("old_user_name",False)
        new_home_longitude = received_json_data.get("new_home_longitude",False)
        new_home_latitude = received_json_data.get("new_home_latitude",False)
        new_office_longitude = received_json_data.get("new_office_longitude",False)
        new_office_latitude = received_json_data.get("new_office_latitude",False)
        new_phone = received_json_data.get("new_phone",False)
        new_string_home_address = received_json_data.get("new_string_home_address",False)
        new_string_office_address = received_json_data.get("new_string_office_address",False)
        new_qbuserid = received_json_data.get("new_qbuserid",False)
        
        try:
            userCollection.update({"user_name":old_user_name},
                                    {'$set':{ "first_name":new_first_name,"encrypted_pwd":new_encrypted_pwd,"last_name":new_last_name,"email":new_email,"phone":new_phone,"qbuserid":new_qbuserid,
                                    "user_name":new_user_name,"string_home_address":new_string_home_address,"string_office_address":new_string_office_address,
                                    "home_longitude":new_home_longitude,"home_latitude":new_home_latitude,
                                    "office_longitude":new_office_longitude,"office_latitude":new_office_latitude }})
            user_list =   bookCollection.find({"users.user_name":old_user_name})                      
            for r in user_list :
                #print r
                if (len(r["users"])!=0):
                    for index in range(len(r["users"])):
                        try:
                            bookCollection.update({"users.user_name":old_user_name},{'$set':{"users.index.first_name":new_first_name,"users.index.encrypted_pwd":new_encrypted_pwd,"users.index.last_name":new_last_name,"users.index.email":new_email,
                                        "users.index.phone":new_phone,"users.index.qbuserid":new_qbuserid,
                                        "users.index.user_name":new_user_name,"users.index.string_home_address":new_string_home_address,"users.index.string_office_address":new_string_office_address,
                                        "users.index.home_longitude":new_home_longitude,"users.index.home_latitude":new_home_latitude,
                                        "users.index.office_longitude":new_office_longitude,"users.index.office_latitude":new_office_latitude}}  )
                        except Exception as e:
                            print(e)
                            print "Returning Failure of user detail update in books collection"
                            return HttpResponse("Error during user update in books collection")                
            
        except Exception as e:
            print(e)
            print "Returning Failure of user detail update"
            return HttpResponse("Error during user update")   
            
#posts.update({"_id":5678},{"$pull":{"skills":"java"}})
@csrf_exempt   
@api_view(['GET','POST'])
def perform_exchange(request):
    #connect to our local mongodb
    books = []
    book = []
    print "About to request Connection"
    mongoserver_uri = "blah"
    db = MongoClient(host=mongoserver_uri)
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
            book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
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
        category = received_json_data.get("category",False)
        isbn = received_json_data.get("isbn",False)
        print "Going into try catch block to insert transaction"
        
        
        
        try:
            #bookCollection.insert({"name" : name, "author": author})
            #posts.update({"_id":5678},{"$pull":{"skills":"java"}})
            #for r in bookCollection.find({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status}):
            #    print r
            #for s in userCollection.find({"user_name":owner_user_name}):
            #    print s
            
            search_book = bookCollection.find({"name":name,"author":author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status":status,"users.user_name":owner_user_name})
            #book_search = bookCollection.find({"name":name,"author":author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status" :status,"users.user_name":user_name})
            if(search_book.count() != 0):
                bookCollection.update({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status":status},{'$pull': {"users":{"user_name":owner_user_name}}})
                userCollection.update({"user_name":owner_user_name},{'$pull': {"books":{"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status }}})
                userCollection.update({"user_name":borrower_user_name},{'$push': {"borrowed_books":{"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status }}})
                transactionCollection.insert({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status":status,"rent_price":rent_price,"sell_price":sell_price,"borrower_user_name":borrower_user_name,"owner_user_name":owner_user_name})
            else:
                return HttpResponse("This user doesnot have this book")
        except Exception as e:
            print(e)
            return HttpResponse("false" )
        return HttpResponse("OK")
        
        """
************************************        
*      COMMENTED OUT               *
************************************      
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
                    book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
                    books.append(book)
            serializedList = BookSerializer(books, many=True)
            return Response(serializedList.data)    
        else:
            print search_parameter
            print required_page
            print books_per_page
            print "Going into for loop"
           
            print "REGEX IS"
            regex = re.compile(r'.*'+search_parameter+'.*',re.IGNORECASE)
            print regex
            print regex.pattern
            
        #for r in bookCollection.find({"name":{'$regex':new_search_parameter}}):#.skip((required_page-1)*books_per_page).limit(books_per_page):
        #print bookCollection.find({"name":{'$regex':'/C/'}})
        #for r in bookCollection.find({"name":{"$regex":new_search_parameter}}):#.skip((required_page-1)*books_per_page).limit(books_per_page):
            try:
                for r in bookCollection.find({"$or":[{"name":regex},{"author":regex}]}).skip((required_page-1)*books_per_page).limit(books_per_page):
                    book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
                    books.append(book)
                print "before serializing"
                serializedList = BookSerializer(books, many=True)
                #print serializedList.data
                return Response(serializedList.data)    
            except Exception as e:
                print(e)
                return HttpResponse("Error in searching")
            
        
            for r in bookCollection.find({"name":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
                #if(r["status"] =="OK")

                book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
                books.append(book)
                
            for r in bookCollection.find({"author":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
            #if(r["status"] =="OK")
                book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
                books.append(book)
            
            for r in bookCollection.find({"description":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
            #if(r["status"] =="OK")
                book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
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
@api_view(['GET','PUT','POST'])
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
            book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
            books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        #print request.body
        received_json_data=json.loads(request.body)
        #print received_json_data
        name = received_json_data.get("name",False)
        description = received_json_data.get("description",False)
        published_date = received_json_data.get("published_date",False)
        status = received_json_data.get("status",False)
        author = received_json_data.get("author",False)
        image = received_json_data.get("image",False)
        sell_price = received_json_data.get("sell_price",False)
        rent_price = received_json_data.get("rent_price",False)
        category = received_json_data.get("category",False)
        isbn = received_json_data.get("isbn",False)
        print name
        print author
        user_name = received_json_data.get("user_name",False)
        
        changes = received_json_data.get("changes",False)
        
        if(changes == "YES"):
            bookCollection.update({"name":name,"author": author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status" : status,"users.user_name":user_name},
                                    {'$set':{"users.$.sell_price":sell_price,"users.$.rent_price":rent_price}})
            return HttpResponse("Book details are updated")
        else :
            
            
        #first_name = received_json_data.get("first_name",False)
        #last_name = received_json_data.get("last_name",False)
        #email = received_json_data.get("email",False)
        #phone = received_json_data.get("phone",False)
        #home_longitude = received_json_data.get( "home_longitude",False)
        ##home_latitude = received_json_data.get("home_latitude",False)
        #office_longitude = received_json_data.get("office_longitude",False)
        #office_latitude = received_json_data.get("office_latitude",False)
        
            book_search = bookCollection.find({"name":name,"author": author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status" : status,"users.user_name":user_name})
        
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
                    bookCollection.update({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status":status},
                                        {'$push':
                                            {"users":{"first_name": first_name,"last_name": last_name,"email": email,"phone": phone,"user_name": user_name,"home_longitude": home_longitude,"home_latitude": home_latitude,"office_longitude": office_longitude,"office_latitude": office_latitude,"sell_price": sell_price,"rent_price": rent_price }}
                                        },True)
                                    
                    userCollection.update({"first_name": first_name,"last_name": last_name,"email": email,"phone": phone,"user_name":user_name,"home_longitude": home_longitude,"home_latitude": home_latitude,"office_longitude": office_longitude,"office_latitude": office_latitude},
                                        {'$push': {"books":{"name": name,"author": author,"image": image,"description":description,"published_date":published_date,"category":category,"isbn":isbn,"status":status,"sell_price": sell_price,"rent_price": rent_price }}
                                        },True)
            except Exception as e:
                print(e)
                return HttpResponse("false" )
            return HttpResponse("OK")
    


        




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

@csrf_exempt   
@api_view(['GET','POST'])
def test_connection(request):
    #connect to our local mongodb
    books = []
    book = []
    users = []
    user = []
    print "About to request Connection"
    mongoserver_uri = "mongodb://jbuser:jbsuperpassword@urkk30b07ae8.ravitejabadisa.koding.io:12345/jb"
    db = MongoClient(host=mongoserver_uri)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']
    
    print "About to Authenticate user"
    for r in bookCollection.find():
            #if(r["status"] == "OK")
            book = Book(r["name"],r["description"],r["published_date"],r["category"],r["isbn"],r["status"],r["author"],r["image"],r["users"],[],[])
            books.append(book)
    serializedList = BookSerializer(books, many=True)
    
    return Response(serializedList.data)
    """