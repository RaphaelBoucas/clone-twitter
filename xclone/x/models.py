from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE) # Associando o user ao auth User;
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)

    profile_image = models.ImageField(null=True, blank=True, upload_to='images/')
    
    ##Bio info:
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=150)
    facebook_link = models.CharField(null=True, blank=True, max_length=150)
    instagram_link = models.CharField(null=True, blank=True, max_length=150)
    linkedin_link = models.CharField(null=True, blank=True, max_length=150)

    def __str__(self):
        return self.username
    

#Tweet model:

class Tweet(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name="tweets",
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='tweet_like', blank=True)
    
    #Like counter:
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (f"{self.user} - "
                f"{self.created_at:%Y-%m,-%d %H:%M} - "
                f"{self.body}"
        )