from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=('name','contact_details','address','vendor_code','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate')

class POSerSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields=('po_number','vendor','order_date','delivery_date','items','quantity','status','quality_rating','issue_date','acknowledgment_date')

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=HistoricalPerformance
        fields=('vendor','date','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate')

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=('name','vendor_code','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate')
        