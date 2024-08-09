from django.db import models
from category.models import Category
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user',default=None)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/media/images/',null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.IntegerField()
    buyers = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Comments by {self.name}"
    
    