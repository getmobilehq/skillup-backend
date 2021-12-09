from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import related
from django.utils import timezone
from django.contrib.auth import get_user_model

User=get_user_model()

class UserIdentity(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True,blank=True,  related_name='identities')
    identity_type = models.CharField(max_length=200)
    identity = models.CharField(max_length=300)

class BankDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank', null=True, blank=True)
    bank_name = models.CharField(max_length=250)
    account_name = models.CharField(max_length=250)
    account_num = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_name
    
class UserEmploymentDetail(models.Model):
    company_name = models.CharField(max_length=350)
    location = models.CharField(max_length=350)
    job_title = models.CharField(max_length=360)
    employment_type = models.CharField(max_length=350)
    startdate = models.CharField(max_length=300)
    enddate = models.CharField(max_length=300, null=True, blank=True)
    currently_works_there=models.BooleanField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='employments', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    
    
    def delete(self):
        self.is_active=False
        self.save()
        return
    
    
    
class UserProfile(models.Model):
    story=models.TextField()
    application_reason = models.TextField()
    support_self=models.BooleanField()
    support_self_reason = models.TextField(null=True, blank=True)
    financial_reponsibilities=models.BooleanField()
    financial_reponsibilities_explanation = models.TextField(null=True, blank=True)
    voluntering_experience=models.BooleanField()
    voluntering_experience_detail = models.TextField(null=True, blank=True)
    volunter_year = models.CharField(max_length=300,null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING,  related_name='profiles', null=True,blank=True)
    is_active=models.BooleanField(default=True)

    
    def delete(self):
        self.is_active=False
        self.save()
        return
    
    

class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING,  related_name='addresses',null=True, blank=True)
    address = models.TextField()
    additional_info = models.TextField()
    city=models.CharField(max_length=400)
    region=models.CharField(max_length=400)
    is_active=models.BooleanField(default=True)
    
    
    def delete(self):
        self.is_active=False
        self.save()
        return

    

class SocialMedia(models.Model):
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='handles', null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin=models.URLField(null=True, blank=True)
    instagram=models.URLField(null=True, blank=True)
    twitter=models.URLField(null=True, blank=True)
    github=models.URLField(null=True, blank=True)
    behance=models.URLField(null=True, blank=True)
    is_active=models.BooleanField(default=True)
    
    
    def delete(self):
        self.is_active=False
        self.save()
        return
    
class TertiaryInstitution(models.Model):
    country = models.CharField(max_length=300)
    institution = models.CharField(max_length=3600)
    field_of_study = models.CharField(max_length=300)
    qualification = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='tertiary_institutions')
    is_active=models.BooleanField(default=True)
    
    
    def delete(self):
        self.is_active=False
        self.save()
        return
    
    
class HighSchool(models.Model):
    country = models.CharField(max_length=300)
    institution = models.CharField(max_length=3600)
    qualification = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='high_schools')
    is_active=models.BooleanField(default=True)
    
    
    def delete(self):
        self.is_active=False
        self.save()
        return
    

class TrainingPathway(models.Model):
    course = models.CharField(max_length=300)
    cohort = models.CharField(max_length=300)
    campus = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='pathway')
    is_active = models.BooleanField(default=True)
    
    def delete(self):
        self.is_active=False
        self.save()
        return
    

class KYC(models.Model):
    state_of_residence = models.CharField(max_length=300)
    address = models.TextField()
    city = models.CharField(max_length=300)
    local_gov = models.CharField(max_length=300)
    doc_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='kyc_docs')
    is_active =  models.BooleanField(default=True)
    
    
    def delete(self):
        self.is_active=False
        self.save()
        return