from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

router = DefaultRouter(trailing_slash=False)

# register the drf viewsets
router.register('', TaskViewSet, basename='/')

urlpatterns = router.urls
