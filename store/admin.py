from django.contrib import admin
from store.models import Product, ContactSubmission, Cart

# Register your models here.
admin.site.register(ContactSubmission)
admin.site.register(Product)
admin.site.register(Cart)