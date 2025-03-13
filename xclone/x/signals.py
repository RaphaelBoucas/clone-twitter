from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def self_following(sender, instance, created, **kwargs):
    if created:
        # Aguarda o commit final antes de adicionar ao ManyToManyField
        instance.refresh_from_db()
        instance.follows.add(instance)  # Usuário segue a si mesmo
        print(f"{instance.username} agora segue a si mesmo!") 
