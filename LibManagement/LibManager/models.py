from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=20)


    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    type = models.ManyToManyField( Type , help_text="Select a type for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text="Enter a description of the book")
    copies_num = models.IntegerField()
    available_copies = models.IntegerField()
    pic=models.ImageField(blank=True, null=True, upload_to='book_image')

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])





class Language(models.Model):
    name = models.CharField(max_length=200 , help_text="Enter the book's language")

    def __str__(self):
        return self.name






class Member(models.Model):
    roll_no = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=10)
    branch = models.CharField(max_length=3)
    contact_no = models.CharField(max_length=10)
    total_books_due=models.IntegerField(default=0)
    email=models.EmailField(unique=True)
    pic=models.ImageField(blank=True, upload_to='profile_image')
    def __str__(self):
        return str(self.roll_no)



class Borrower(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)
    
    
    def __str__(self):
        # return self.member.name +" borrowed "+ self.book.title
        return self.book.title + "borrwed by" + self.member.name




class Reviews(models.Model):
    review=models.CharField(max_length=100,default="None")
    book=models.ForeignKey('Book',on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    rating=models.CharField(max_length=3, choices=CHOICES, default='1')




# post_save.connect(create_user, sender=Member)


# def create_user(sender, *args, **kwargs):
# if kwargs['created']:
#     user = User.objects.create(username=kwargs['instance'],password="dummypass")



