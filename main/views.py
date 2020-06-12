from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from .serializers import ActualiteSerializer, ResponsableEtabSerializer, UserSerializer, RatingSerializer, CategorieSerializer, CommentSerializer
from .models import Actualite, ResponsableEtab, Categorie, Rating, Comment
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from datetime import datetime, timedelta


class ResponsableEtabViewSet(viewsets.ModelViewSet):
    queryset = ResponsableEtab.objects.all().order_by('id')
    serializer_class = ResponsableEtabSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['POST'])
    def create_account(self, request):
        username = request.data['username']
        first_name=request.data['first_name']
        last_name = request.data['last_name']
        password=request.data['password']
        if User.objects.filter(username=username).exists():
            return Response({
            'message': 'username deja existe'
        })
        user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password)
        token = Token.objects.create(user=user)
        account = UserSerializer(user).data
        return Response({
            'token': token.key,
            'id': account['id'],
            'username': account['username'],
            'First_name': account['first_name'],
            'Last_name': account['last_name'],
            'message': True
        })

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all().order_by('id')
    serializer_class = CategorieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all().order_by('id')
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def rating(self, request,pk=None):
        id_user = request.data['id']
        rate = request.data['rate']
        id_Actualite = pk
        if Rating.objects.filter(User=id_user,Actualite=id_Actualite).exists():
            Rating.objects.filter(User=id_user,Actualite=id_Actualite).update(Rate=rate)
            return Response(
            {'message': 'updated','newdatajson' : rate})
        actualite= Actualite.objects.get(id=id_Actualite)
        user= User.objects.get(id=id_user)
        Rating.objects.create(User=user,Actualite=actualite,Rate=rate)
        return Response({
            'message': 'Succed'
        })


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['GET'])
    def getComments(self, request, pk=None):
        comments = Comment.objects.filter(Actualite=pk).order_by('id').reverse()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class ActualiteViewSet(viewsets.ModelViewSet):
    queryset = Actualite.objects.all().order_by('DatePublication').reverse()
    serializer_class = ActualiteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['GET'])
    def getactualites(self, request, pk=None):
        user = Actualite.objects.filter(Categorie=pk)
        serializer = ActualiteSerializer(user, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def getactualitesbyratenumber(self, request):
        temp = sorted(Actualite.objects.all(), key=lambda a: a.avg_ratings(),reverse=True)
        serializer = ActualiteSerializer(temp, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def getactualitesbynumberrate(self, request):
        temp = sorted(Actualite.objects.all(), key=lambda a: a.no_of_ratings(),reverse=True)
        serializer = ActualiteSerializer(temp, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def getactualitesbycomments(self, request):
        temp = sorted(Actualite.objects.all(), key=lambda a: a.no_of_comments(),reverse=True)
        serializer = ActualiteSerializer(temp, many=True)
        return Response(serializer.data)
    

    @action(detail=False)
    def getactualitesby24hours(self, request):
        earlier = datetime.now() - timedelta(hours=24)
        print(datetime.now())
        print(earlier)
        temp = Actualite.objects.filter(DatePublication__range=(earlier,datetime.now())).order_by('-DatePublication')
        serializer = ActualiteSerializer(temp, many=True)
        print(serializer)
        return Response(serializer.data)
    

    @action(detail=False)
    def getactualitesbySemaine(self, request):
        earlier = datetime.now() - timedelta(days=7)
        print(datetime.now())
        print(earlier)
        temp = Actualite.objects.filter(DatePublication__range=(earlier,datetime.now())).order_by('-DatePublication')
        serializer = ActualiteSerializer(temp, many=True)
        print(serializer)
        return Response(serializer.data)
    
    @action(detail=False)
    def getactualitesbymonth(self, request):
        earlier = datetime.now() - timedelta(days=30)
        print(datetime.now())
        print(earlier)
        temp = Actualite.objects.filter(DatePublication__range=(earlier,datetime.now())).order_by('-DatePublication')
        serializer = ActualiteSerializer(temp, many=True)
        print(serializer)
        return Response(serializer.data)
    