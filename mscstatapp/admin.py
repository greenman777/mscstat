#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import UserCreationForm
from mscstatapp import models
from mscstatauth.models import User
from Crypto.Cipher import Blowfish
import binascii

from django.forms import ModelForm, PasswordInput


class MssUserForm(ModelForm):
    raw_psw = forms.CharField(label = "Пароль", widget = PasswordInput(render_value = True))
    def get_crypto(self,password):
        enc_obj = Blowfish.new( settings.SECRET_KEY )
        if password:
            return "%s" % enc_obj.decrypt( binascii.a2b_hex(password) ).rstrip()
        else:
            ""
    def __init__(self, *args, **kwargs):
        super(MssUserForm, self).__init__(*args, **kwargs)
        self.fields['raw_psw'].initial = self.get_crypto(self.instance.password)
    class Meta:
        model = models.Mss
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    def clean_username(self):
        User = get_user_model() 
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class MyUserAdmin(UserAdmin):
    
    add_form = MyUserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Персональная информация'), {'fields': ('first_name', 'last_name', 'birthday','email',
                                                   'phone','phone_other','phone_short','position',)}),
        (('Организация'), {'fields': ('organization_name', 'business_address')}),
        (('Разрешения'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'mss','groups', 'user_permissions')}),
        (('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    ) 
    list_display = ('username', 'last_name', 'first_name', 'birthday','email', 'phone',
                    'phone_other', 'organization_name', 'position', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('last_name','first_name',)
    filter_horizontal = ('mss','groups', 'user_permissions') 


class MssAdmin(admin.ModelAdmin):
    
    form = MssUserForm
    
    def set_crypto(self, psw_value):
        enc_obj = Blowfish.new( settings.SECRET_KEY )
        repeat = 8 - (len( psw_value ) % 8)
        psw_value = psw_value + " " * repeat
        return binascii.b2a_hex(enc_obj.encrypt( psw_value ))
    def save_model(self, request, obj, form, change):
        getparams = request.POST.copy()
        raw_psw =  getparams.get('raw_psw')
        obj.password = self.set_crypto(raw_psw)
        obj.save()   

class KpiAdmin(admin.ModelAdmin):
    list_display = ('name','higher_better')


class SubscribeMessagesAdmin(admin.ModelAdmin):
    list_display = ('recipient','subscribe','mss','subscribe_active')
    search_fields = ('recipient','subscribe','mss','subscribe_active')
    list_filter = ('recipient','subscribe','mss','subscribe_active')


class ThresholdsAdmin(admin.ModelAdmin):
    list_display = ('mss','kpi','value_high','value_sufficient','value_emergency','threshold_events','threshold_active')
    search_fields = ('mss','kpi','value_high','value_sufficient','value_emergency','threshold_events','threshold_active')
    list_filter = ('mss','kpi','value_high','value_sufficient','value_emergency','threshold_events','threshold_active')


class TkgThresholdsAdmin(admin.ModelAdmin):
    list_display = ('mss','kpi','object_name','value_high','value_sufficient','value_emergency','threshold_events','threshold_active')
    search_fields = ('mss','kpi','object_name','value_high','value_sufficient','value_emergency','threshold_events','threshold_active')
    list_filter = ('mss','kpi','object_name','value_high','value_sufficient','value_emergency','threshold_events','threshold_active')

    """
    def get_form(self, request, obj=None, **kwargs):

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            #     print self.get_form(request)
            if db_field.name == "object_name":
                kwargs["queryset"] = models.Object.objects.filter(type=25)
            return super(TkgThresholdsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    """

admin.site.register(User, MyUserAdmin)
admin.site.register(models.Priority)
admin.site.register(models.TaskStatus)
admin.site.register(models.Mss,MssAdmin)
admin.site.register(models.CounterNoCleaning)
admin.site.register(models.Kpi,KpiAdmin)
admin.site.register(models.Subscribes)
admin.site.register(models.SubscribeMessages,SubscribeMessagesAdmin)
admin.site.register(models.Thresholds,ThresholdsAdmin)
admin.site.register(models.TkgThresholds,TkgThresholdsAdmin)