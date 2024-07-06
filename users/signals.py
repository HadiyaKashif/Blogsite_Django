from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender = User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()

# @receiver(post_delete, sender=Profile)
# def delete_profile(sender, instance, **kwargs):
#     if instance.image != Profile.image.field.default:
#         os.remove(instance.image.path)
#something I copied from comments to delete picture too when profile or user is deleted