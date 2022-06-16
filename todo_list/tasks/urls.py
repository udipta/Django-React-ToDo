from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

router = DefaultRouter()

# register the drf viewsets
router.register('', TaskViewSet, basename='tasks')

urlpatterns = router.urls
