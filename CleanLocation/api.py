from models import point_location
from rest_framework import viewsets, permissions
from .serializar import api_cleanlocation
class proyectviewsset(viewsets.ModelViewSet):
    queryset= point_location.objects.all()
    permission_classes= [permissions.AllowAny]
