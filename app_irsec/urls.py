from django.urls import path, include
from . import views
from .views import CategoryViewSet, TopicViewSet
from rest_framework.routers import DefaultRouter


from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TopicViewSet, CategoryGetOrCreateView, TopicGetOrCreateView



app_name = 'app_irsec'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'topics', TopicViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('get-topic-content/<int:topic_id>/', views.get_topic_content, name='get_topic_content'),
    path('api/categories/get_or_create/', CategoryGetOrCreateView.as_view(), name='category-get-or-create'),
    path('api/topics/get_or_create/', TopicGetOrCreateView.as_view(), name='topic-get-or-create'),
    path('api/', include(router.urls)), 
]

