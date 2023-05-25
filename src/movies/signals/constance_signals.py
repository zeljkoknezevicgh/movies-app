from constance.signals import config_updated
from django.dispatch import receiver


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    print(sender, key, old_value, new_value)
