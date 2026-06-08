from django.db.models.signals import post_save
from core.models import Items,Quantity
from django.dispatch import receiver

@receiver(post_save,sender=Items)
def sync_actualprice_price(sender,created,instance,**kwargs):
    if created:
        print('updated')
    else:
        quantity=Quantity.objects.filter(quantity_items=instance)
        for quantity in quantity:
            quantity.actual_price=instance.price
            quantity.save()

        
     
