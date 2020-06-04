from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('Actualite', views.ActualiteViewSet)
router.register('ResponsableEtab', views.ResponsableEtabViewSet)
router.register('User', views.UserViewSet)
router.register('Categorie', views.CategorieViewSet)
router.register('Rating', views.RatingViewSet)
router.register('Comment', views.CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
   path('', include(router.urls)),
]


