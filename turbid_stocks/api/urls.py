from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'instruments', views.InstrumentViewSet,
                basename='instrument')
router.register(r'users', views.UserViewSet, basename='user')
