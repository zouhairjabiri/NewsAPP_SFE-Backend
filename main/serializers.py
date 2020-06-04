from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Actualite, ResponsableEtab, Categorie, Rating, Comment
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password']
        required_fields = fields
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            },
        }


class ResponsableEtabSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableEtab
        fields = [
            'id', 'first_name', 'last_name', 'username', 'password',
            'NomEtablissement'
        ]
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'


class ActualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actualite
        fields = [
            'id', 'Categorie', 'auteur', 'image', 'Titre', 'Description',
            'DatePublication','no_of_ratings','avg_ratings',
        ]

    def to_representation(self, instance):
        self.fields['Categorie'] = CategorieSerializer(read_only=False)
        self.fields['auteur'] = ResponsableEtabSerializer(read_only=True)
        return super(ActualiteSerializer, self).to_representation(instance)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
   

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id','Commentaire','User','Actualite','Date',
        ]

    def to_representation(self, instance):
        self.fields['User'] = UserSerializer(read_only=True)
        return super(CommentSerializer, self).to_representation(instance)    

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'First_name': user.first_name,
            'Last_name': user.last_name,
            'message': 'Succed'
        })
