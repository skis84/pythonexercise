from django.contrib import admin
from .models import Company, Name, Address, PhoneNumber, Website

# Register your models here.
admin.site.register(Company)


class NameAdmin(admin.ModelAdmin):
    list_display = ('value', 'version', 'source', 'registration_date',
                    'end_date', 'modified',
                    'language', 'data_type', 'company')


admin.site.register(Name, NameAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'post_code', 'city',
                    'country', 'data_type', 'company')


admin.site.register(Address, AddressAdmin)


class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ('value', 'version', 'source', 'registration_date',
                    'end_date', 'modified',
                    'language', 'data_type', 'company')


admin.site.register(PhoneNumber, ContactDetailAdmin)
admin.site.register(Website, ContactDetailAdmin)
