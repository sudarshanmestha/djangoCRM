from django.contrib import admin
from .models import User, Lead, Agent, UserProfile, Category

class AuthorAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Category, AuthorAdmin)
admin.site.register(User, AuthorAdmin)
admin.site.register(UserProfile, AuthorAdmin)
admin.site.register(Lead, AuthorAdmin)
admin.site.register(Agent, AuthorAdmin)