from django.contrib import admin
from .models import *
# register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','language', 'describtion','copies_num' ,'available_copies' ,'pic' )
    # search_fields = ('name',)
    

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', )



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
        list_display = ('name', )



@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
        list_display = ('member', )



@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
        list_display = ('roll_no','name','branch' , 'contact_no' ,'total_books_due' ,'email' ,'pic' )
    



@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
        list_display = ('book', 'review' , 'member', 'rating' )
