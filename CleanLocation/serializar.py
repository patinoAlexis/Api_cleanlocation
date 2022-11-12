from rest_framework import serializers
from models import point_location

class api_cleanlocation(serializers.ModelSerializer):
    class Meta:
        model= ('id','latitud','logitud')
