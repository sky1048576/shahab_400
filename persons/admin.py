from django.contrib import admin
from .models import Home
from .models import Picture,State,City,Comment

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Member

# Define an inline admin descriptor for Member model
# which acts a bit like a singleton
class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'member'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = ['id','email','phone_number',]
    def phone_number(self, object):
        return object.member.phone_number

    inlines = (MemberInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)





class HomesAdmin(admin.ModelAdmin):
    list_display = ['__str__','id','name','address','about','state','city','timestamp','updated']
    search_fields = ['name']

admin.site.register(Home,HomesAdmin)

class PictureAdmin(admin.ModelAdmin):
    list_display = ['__str__','id','homeid','image','timestamp','updated']

admin.site.register(Picture,PictureAdmin)

# class StateAdmin(admin.ModelAdmin):
#     list_display = ['id','name']
    
# admin.site.register(State,StateAdmin)

# class CityAdmin(admin.ModelAdmin):
#     list_display = ['id','ostan','name']
    
# admin.site.register(City,CityAdmin)




class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','writer','home','text']
    
admin.site.register(Comment,CommentAdmin)



class CityInline(admin.StackedInline):
    model = City
    can_delete = False
    verbose_name_plural = 'city'

# Define a new User admin
class StateAdmin(admin.ModelAdmin):
    inlines = (CityInline, )

# Re-register UserAdmin
admin.site.register(State, StateAdmin)




