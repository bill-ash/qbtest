from django.db import models
from django_quickbooks.models import QBDModelMixin


class Customer(QBDModelMixin):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=10)
    street = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
	
    def _get_address(self): 
        return f'{self.street} {self.city}, {self.city} {self.zip}'


    def to_qbd_obj(self, **fields):
        from django_quickbooks.objects import Customer as QBCustomer
        # map your fields to the qbd_obj fields
        return QBCustomer(
            Name=self.__str__(),
            IsActive=True,
            Phone=self.phone,
            Email=self.email, 
            CompanyName='CompanyName', 
            AltContact='AltContact', 
            AltPhone='1233212312', 
            # FullName= [self.first_name, self.last_name],
            
            #BillAddress= self._get_address()
                
            )

    @classmethod			  
    def from_qbd_obj(cls, qbd_obj):
        # map qbd_obj fields to your model fields
        return cls(
            first_name=qbd_obj.Name,
            phone=qbd_obj.Phone,
            qbd_object_id=qbd_obj.ListID,
            qbd_object_version=qbd_obj.EditSequence
        )


from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django_quickbooks.models import QBDTask
from django_quickbooks import QUICKBOOKS_ENUMS
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Customer)
def send_customer_to_qbtask(sender, instance, **kwargs):
	QBDTask.objects.create(
        qb_operation=QUICKBOOKS_ENUMS.OPP_ADD,
        qb_resource=QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER,
        object_id=instance.id,
        content_type=ContentType.objects.get_for_model(instance),
        realm_id="8b47cd5f-5a1e-4f81-ab28-11b04ce709fd"
    )
