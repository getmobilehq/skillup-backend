from django.contrib import admin
from .models import Address, UserEmploymentDetail, UserIdentity,BankDetails
# Register your models here.

admin.site.register([UserIdentity, BankDetails,Address, UserEmploymentDetail])

