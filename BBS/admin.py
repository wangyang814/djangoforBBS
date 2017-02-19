from django.contrib import admin
from BBS import models
from django.contrib.auth.models import User
# Register your models here.
class BBS_admin(admin.ModelAdmin):
    list_display = ('title','summary','sig',)
    list_filter = ('create_at','author')
    search_fields = ('title','author__user__username')
    def sig(self,obj):
        return obj.author.signature
    sig.short_description = "qian ming"
class BBS_user_photo(admin.ModelAdmin):
    list_display = ('user','photo',)
class BBS_title_set(admin.ModelAdmin):
    list_display = ("name","info")
class BBS_Cate(admin.ModelAdmin):
    list_display = ("name","administrator")


admin.site.register(models.BBS,BBS_admin)
admin.site.register(models.Category,BBS_Cate)
admin.site.register(models.BBS_user,BBS_user_photo)



