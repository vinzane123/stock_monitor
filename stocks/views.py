from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer,ItemSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BaseAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import exceptions
from rest_framework import filters
from stock_monitor.config import *
from .models import ItemList
import requests
# Create your views here.


'''
    Login API which returns token 
    validating username and pass-
    -word of the user.
'''

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request,user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token":token.key},status=200)


'''
    Logout API which removes the
    sessionId from the cookies.
'''   

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self,request):
        django_logout(request)
        return Response(status=204)

''' 
    An API that returns all stock
    names matched with the keywords
    parameter.
'''

class StockSearch(APIView):
    function = "SYMBOL_SEARCH"
    apikey = api_key
    url = URL
    authentication_classes = (SessionAuthentication,TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self,request):
        re = request.query_params
        if re:
            keywords = re['keywords']
            payload = {'function':self.function,'keywords':keywords,'apikey':api_key}
            r = requests.get(self.url,params=payload)
            data = r.json()
        else:
            msg  = "Please enter your keywords."
            raise exceptions.ValidationError(msg)
        return Response(data)

''' 
    API to retrieve a specific item from the watchlist,
    an api to list all the items universal in watchlist,
    an api to remove an item from the watchlist and
    an api to add an item to the watchlist.
'''

class WatchList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    
    queryset = ItemList.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = (SessionAuthentication,TokenAuthentication)
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    function = "TIME_SERIES_INTRADAY"
    interval = "5min"
    apikey = api_key
    url = URL

    def get(self, request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)

    def delete(self,request,id=None):
        obj = ItemList.objects.get(id=id)
        print(obj.user,request.user)
        if obj.user == request.user:
            return self.destroy(request,id)
        else:
            msg = "Not enough Credentials"
            raise exceptions.ValidationError(msg)
        
    def post(self,request):
        try:
            obj_items = ItemList.objects.filter(user=request.user)
            l =[]
            if len(obj_items)>0:
                for x in obj_items:
                    l.append(x.item_name)
                if request.data['item_name'] in l:
                    msg = "Item already added to your WatchList."
                    raise exceptions.ValidationError(msg)
                else:
                    self.create(request)
                    symbol =request.data['item_name']
                    payload = {'function':self.function,'symbol':symbol,'apikey':self.apikey,'interval':self.interval}
                    r = requests.get(self.url,params=payload)
                    if len(r.json()) == 1:
                        ins = PostValues()
                        ins.delete_obj(symbol=symbol,user=request.user)
                        return Response(r.json())
                    else:
                        p = PostValues()
                        val =p.save(symbol=symbol,user=request.user,r=r)
                        return Response({'item_name':request.data['item_name'],'value':val,'response':'Added Successfully','status':201})
            else:
                self.create(request)
                symbol =request.data['item_name']
                payload = {'function':self.function,'symbol':symbol,'apikey':self.apikey,'interval':self.interval}
                r = requests.get(self.url,params=payload)
                if len(r.json()) == 1:
                    ins = PostValues()
                    ins.delete_obj(symbol=symbol,user=request.user)
                    return Response(r.json())

                else:
                    p = PostValues()
                    val=p.save(symbol=symbol,user=request.user,r=r)
                    return Response({'item_name':symbol,'value':val,'response':'Added Successfully','status':201})
        except ItemList.DoesNotExist as e:
            return Response( {"error": "Given object with user not found."}, status=404)
    
'''
    An Auxilliary Class to create/delete
    the instance of an object from the WatchList.
'''

class PostValues:
    
    def save(self,symbol,user,r):
        obj_v = ItemList.objects.get(user=user,item_name=symbol)
        res = r.json()['Time Series (5min)']
        result = list(res.values())[-1]['4. close']
        obj_v.value=result
        obj_v.save()
        return result
    
    def delete_obj(self,symbol,user):
        obj = ItemList.objects.get(user=user,item_name=symbol)
        obj.delete()

'''
    An API to return the WatchList of a user.
'''

class WatchListbyUser(generics.ListAPIView):
    serializer_class = ItemSerializer
    authentication_classes = (SessionAuthentication,TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        user = self.request._user.id
        if user:
            return ItemList.objects.filter(user=user)   
        else:
            return self.list(request,status=204)


