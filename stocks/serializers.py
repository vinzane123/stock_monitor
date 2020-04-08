from django.contrib.auth.models import User
from .models import ItemList
from django.contrib.auth import authenticate,login
from rest_framework import exceptions
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username = data.get("username","")
        password = data.get("password","")

        if username and password:
            user=authenticate(username=username,password=password)
            
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Incorrect Credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Please provide your Username and Password."
            raise exceptions.ValidationError(msg)
        return data
    

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemList
        fields = ['id','user','item_name','last_updated','created_on','value']








