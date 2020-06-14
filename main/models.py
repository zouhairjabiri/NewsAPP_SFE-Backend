from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()

class ResponsableEtab(User):
    NomEtablissement = models.CharField(max_length=60)
    is_Responsable  =  models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Categorie(models.Model):
    Nom = models.CharField(max_length=80)
    icon = models.CharField(max_length=80,default='name')
    Description = models.TextField()

    def __str__(self):
        return self.Nom

        
class Actualite(models.Model):
    auteur = models.ForeignKey(ResponsableEtab, related_name='Actualites', on_delete=models.CASCADE)
    Categorie = models.ForeignKey(Categorie, on_delete = models.CASCADE) 
    Titre = models.CharField(max_length=200)
    image = models.ImageField(storage=gd_storage)
    DatePublication = models.DateTimeField(auto_now_add=True)
    etat = models.IntegerField(default=0)
    Description = models.TextField(default="Description")

    def __str__(self):
        return self.Titre

    def no_of_ratings(self):
        rating = Rating.objects.filter(Actualite=self)
        return len(rating)


    def avg_ratings(self):
        sum = 0
        ratings = Rating.objects.filter(Actualite=self)
        for rating in ratings:
            sum += rating.Rate
        
        if len(ratings) > 0:
            return sum / len(ratings)
        else: 
            return 0

    def no_of_comments(self):
        Comments = Comment.objects.filter(Actualite=self)
        return len(Comments)
    

class Rating(models.Model):
    Actualite = models.ForeignKey(Actualite, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Rate = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])

    class Meta :
        unique_together = ('User' , 'Actualite')
    
    def __str__(self):
        return str(self.id)
    

class Comment(models.Model):
    Actualite = models.ForeignKey(Actualite,on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Commentaire = models.TextField()
    Date = models.DateTimeField(auto_now=True,auto_now_add=False)


    def __str__(self):
        return str(self.id)


