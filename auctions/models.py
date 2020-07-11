from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    start_bid = models.PositiveSmallIntegerField(default=0)
    list_image = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    TRAVEL = 'TR'
    FOOD = 'FD'
    CLOTHING = 'CL'
    ADVENTURE = 'AV'
    OTHER = 'OT'
    CATEGORY_CHOICES = [
        (TRAVEL, 'Travel'),
        (FOOD, 'Food'),
        (CLOTHING, 'Clothing'),
        (ADVENTURE, 'Adventure'),
        (OTHER, 'Other'),
    ]

    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, blank=False, null=False)
            
    def __str__(self):
        return(f'{self.title} listed by {self.user.username}')

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-value']

    def __str__(self):
        return(f'${self.value}')

class Comment(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user.username)

class Watch(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return(f'{self.item.title}')


