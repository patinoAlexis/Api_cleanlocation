from rest_framework import routers
from .api import proyectviewsset

router = routers.DefaultRouter()
router.register('api/Cleanlocation',proyectviewsset,'CleanLocation')

urlpatterns= router.urls