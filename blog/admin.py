from django.contrib import admin
from .models import Subject,Category,MyCategory,MyProduct
from post.models import Post

admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(Post)



@admin.register(MyCategory)
class MyCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(MyProduct)
class MyProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock")
    list_filter = ("category",)
    search_fields = ("name",)
