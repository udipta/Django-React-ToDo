from rest_framework.routers import DefaultRouter

from .views import AuthViewSet

router = DefaultRouter()

# register the drf viewsets
router.register('', AuthViewSet, basename='auth')

urlpatterns = router.urls
