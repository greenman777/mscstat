#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from mscstatapp import models
from django.contrib.auth.models import Group
from mscstatauth.models import User

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tasks

class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskHistory

class TaskCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskComments
                
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notifications

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Priority

class MssSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mss

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Object
                            
class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskStatus