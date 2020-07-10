from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.PositiveSmallIntegerField(default=0)
    list_image = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    current_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, null=True, blank=True)
        
    def __str__(self):
        return(f'{self.title} listed by {self.user.username}')

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return(f'${self.value}')

class Comment(models.Model):
    post = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user.username)