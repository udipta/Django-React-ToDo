from rest_framework.routers import DefaultRouter

from .views import AuthViewSet

router = DefaultRouter(trailing_slash=False)

# register the drf viewsets
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = router.urls
