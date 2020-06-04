from django.contrib import admin
from .models import Actualite, ResponsableEtab, Categorie, Rating, Comment


admin.site.register(Actualite)
admin.site.register(ResponsableEtab)
admin.site.register(Categorie)
admin.site.register(Rating)
admin.site.register(Comment)
