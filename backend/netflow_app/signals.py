from django.db.models.signals import post_migrate
from netflow_app.models import Parameters
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_parameters(sender, **kwargs):
    if not Parameters.objects.exists():
        Parameters.objects.create(timesteps=0) 