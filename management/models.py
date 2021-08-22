from django.db import models

# Create your models here.

class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    flat = models.CharField(max_length=1)
    floor = models.IntegerField()
    nid = models.IntegerField()
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    thana = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    #img = models.ImageField(upload_to='pics')
    def __str__(self):
        return self.name

class Payment(models.Model):
    name = models.ForeignKey(Owner,on_delete=models.CASCADE,null=True,blank=True)
    flat = models.CharField(max_length=1,null=True,blank=True)
    floor = models.IntegerField(default=0)
    #flat = models.ForeignKey(Owner,on_delete=models.CASCADE,null=True,blank=True)
    #floor = models.ForeignKey(Owner,on_delete=models.CASCADE,null=True,blank=True)
    water_bill = models.IntegerField(default=0)
    gas_bill = models.IntegerField(default=0)
    current_bill = models.IntegerField(default=0)
    servicecharge = models.IntegerField(default=0)
    extracharge = models.IntegerField(default=0)
    note = models.CharField(max_length=100,null=True,blank=True)

class Bill(models.Model):
    water = models.IntegerField(default=0,null=True,blank=True)
    gas = models.IntegerField(default=0,null=True,blank=True)
    current = models.IntegerField(default=0,null=True,blank=True)
    service_charge = models.IntegerField(default=0,null=True,blank=True)
    extra = models.IntegerField(default=0,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)