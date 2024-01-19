from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.user.username
    

class DweetCategory(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.CASCADE
    )
    body = models.CharField(max_length=140)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    categories = models.ManyToManyField(DweetCategory, related_name='dweetcategories', blank = True)


    def __str__(self):
        return (f"{self.user.username} "
                f"({self.created_at:%Y-%m-%d %H:%M}): "
                f"{self.body[:30]}"
            )
    def total_likes(self):
        return self.likes.count()
    
    
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    dweet = models.ForeignKey(Dweet, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.dweet.body} - {self.user}'
