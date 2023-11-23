from django.db import models


STATUS=(('pending','Pending'),
        ('completed','completed'),
        ('cancelled','cancelled'))
# Create your models here.
class Vendor(models.Model):
    name=models.CharField(max_length=100)
    contact_details=models.TextField(blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    vendor_code=models.CharField(max_length=50,primary_key=True)
    on_time_delivery_rate=models.FloatField(default=0.0)
    quality_rating_avg=models.FloatField(default=0.0)
    average_response_time=models.FloatField(default=0.0)
    fulfillment_rate=models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f'{self.vendor_code} {self.name}'

class PurchaseOrder(models.Model):
    po_number=models.CharField(max_length=50,primary_key=True)
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date=models.DateTimeField(null=True)
    delivery_date=models.DateTimeField(null=True)
    items=models.JSONField(null=True, blank=True)
    quantity=models.IntegerField(default=0)
    status=models.CharField(choices=STATUS,max_length=50)
    quality_rating=models.FloatField(null=True,blank=True)
    issue_date=models.DateTimeField(null=True)
    acknowledgment_date=models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f'{self.po_number}'

class HistoricalPerformance(models.Model):
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date=models.DateTimeField(null=True)
    on_time_delivery_rate=models.FloatField(default=0.0)
    quality_rating_avg=models.FloatField(default=0.0)
    average_response_time=models.FloatField(default=0.0)
    fulfillment_rate=models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f'{self.vendor}'
    

