from __future__ import unicode_literals
from django.core.validators import RegexValidator

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.forms.models import model_to_dict
import uuid

AUTH_PROVIDERS = {'facebook': 'facebook', 
                  'google': 'google',  
                  'email': 'email'}

class User(AbstractBaseUser, PermissionsMixin):
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.")
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False,)
    firstname          = models.CharField(_('first name'),max_length = 250)
    lastname          = models.CharField(_('last name'),max_length = 250)
    email         = models.EmailField(_('email'), unique=True)
    phone         = models.CharField(_('phone'), validators=[phone_regex],max_length = 15)
    password      = models.CharField(_('password'), max_length=300)
    how_did_you_hear_about_us = models.CharField(max_length=500)
    is_staff      = models.BooleanField(_('staff'), default=False)
    is_admin      = models.BooleanField(_('admin'), default= False)
    is_active     = models.BooleanField(_('active'), default=True)
    completed_nysc = models.CharField(max_length=250, null=True, blank=True)
    nysc_not_applicable_reason = models.TextField(null=True)
    has_work_experience = models.BooleanField(_('work experience'), blank=True, null=True)
    has_laptop = models.BooleanField(null=True, blank=True) 
    take_laptop_loan = models.BooleanField(null=True, blank=True) 
    has_verified_email = models.BooleanField(default=False)
    identity_verification = models.BooleanField(default=False)
    has_added_address = models.BooleanField(default=False)
    has_added_handles = models.BooleanField(default=False)
    has_added_profile= models.BooleanField(default=False)
    has_added_employment_detail= models.BooleanField(default=False)
    has_added_academic_detail = models.BooleanField(default=False) 
    has_added_training_pathway = models.BooleanField(default=False) 
    has_added_laptop_detail = models.BooleanField(default=False)
    has_added_kyc = models.BooleanField(default=False)
    checklist_count=models.IntegerField(default=0)
    date_joined   = models.DateTimeField(_('date joined'), auto_now_add=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
    
    @property
    def address(self):
        return model_to_dict(self.addresses.filter(is_active=True).last())
    
    @property
    def employment_details(self):
        return self.employments.filter(is_active=True).values()
    
    @property
    def profile(self):
        return model_to_dict(self.profiles.filter(is_active=True).last())
    
    @property
    def social_media_handle(self):
        return model_to_dict(self.handles.filter(is_active=True).last())
    
    @property
    def tertiary_institution(self):
        return self.tertiary_institutions.filter(is_active=True).values()
    
    @property
    def high_school(self):
        return self.high_schools.filter(is_active=True).values()
    
    @property
    def training_path(self):
        return model_to_dict(self.pathway.filter(is_active=True).last())
    
    @property
    def kyc_detail(self):
        return model_to_dict(self.kyc_docs.filter(is_active=True).last())
    
class OTP(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    

    
    def __str__(self):
        return self.code