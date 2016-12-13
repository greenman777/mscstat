#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group
from mscstatauth.models import User
from django.db.models import Q
from mscstatapp import models
from rest_framework import viewsets
from mscstatapp import serializers
from mscstatapp import views
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from rest_framework import generics

class TasksViewSet(viewsets.ModelViewSet):
    queryset = models.Tasks.objects.all()
    serializer_class = serializers.TasksSerializer
    def list(self, request):
        getparams = request.GET.copy()
        author_id =  getparams.get('author_id')
        performer_id =  getparams.get('performer_id')
        tasks_filter = Q()
        if author_id != None:
            tasks_filter = tasks_filter | Q(author=author_id)
        if performer_id != None:
            tasks_filter = tasks_filter | Q(performer=performer_id)
        queryset = self.queryset.filter(tasks_filter)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class TaskHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.TaskHistory.objects.all()
    serializer_class = serializers.TaskHistorySerializer
    def list(self, request):
        task = request.GET['task']
        queryset = self.queryset.filter(task=task)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class TaskCommentsViewSet(viewsets.ModelViewSet):
    queryset = models.TaskComments.objects.all()
    serializer_class = serializers.TaskCommentsSerializer
    def list(self, request):
        task = request.GET['task']
        queryset = self.queryset.filter(task=task)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = models.Notifications.objects.all()
    serializer_class = serializers.NotificationsSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user =  request.user
        if user != None:
            filter_Q = Q()
            filter_Q = filter_Q | Q(user=user) | Q(sender=user)
            queryset = queryset.filter(filter_Q)
        else:
            queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class ObjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Object.objects.all()
    serializer_class = serializers.ObjectSerializer
    def list(self, request):
        getparams = request.GET.copy()
        mss = getparams.get('mss')
        typeapp = getparams.get('typeapp')
        if (mss!=None) and (typeapp != None):
            queryset = self.queryset.filter(id__in=views.main.get_object_list(mss,typeapp))
        else:
            queryset = self.queryset.order_by('name')
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
            
class MssViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Mss.objects.all()
    serializer_class = serializers.MssSerializer
    def list(self, request):
        queryset = request.user.mss.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
                    
class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer

class PriorityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Priority.objects.all()
    serializer_class = serializers.PrioritySerializer

class TaskStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TaskStatus.objects.all()
    serializer_class = serializers.TaskStatusSerializer 