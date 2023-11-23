from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from datetime import datetime
# Create your views here.

@api_view(['GET', 'POST'])
def vendors(request):
    if request.method == 'GET':
        all_vendors=Vendor.objects.all()
        all_vendors_serializer=VendorSerializer(all_vendors,many=True)
        return JsonResponse(all_vendors_serializer.data,safe=False)
    elif request.method == 'POST':
        vendor_data=JSONParser().parse(request)
        vendor_serializer=VendorSerializer(data=vendor_data)
        if vendor_serializer.is_valid():
            vendor_serializer.save()
            return JsonResponse(vendor_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(vendor_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','DELETE'])
def vendorDetail(request,pk):
    try:
        required_vendor=Vendor.objects.get(vendor_code=pk)
    except:
        return JsonResponse({'message':'Vendor not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        required_vendor_serializer=VendorSerializer(required_vendor)
        return JsonResponse(required_vendor_serializer.data)
    elif request.method == 'PUT':
        required_vendor_data=JSONParser().parse(request)
        required_vendor_serializer=VendorSerializer(required_vendor,data=required_vendor_data)
        if required_vendor_serializer.is_valid():
            required_vendor_serializer.save()
            return JsonResponse(required_vendor_serializer.data)
        return JsonResponse(required_vendor_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        required_vendor.delete()
        return JsonResponse({'message':'Vendor deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def purchaseOrders(request):
    if request.method == 'GET':
        all_purchase_orders=PurchaseOrder.objects.all()
        vendor=request.query_params.get('vendor',None)
        if vendor is not None:
            try:
                vendor=Vendor.objects.get(vendor_code=vendor)
                all_purchase_orders=all_purchase_orders.filter(vendor=vendor)
            except:
               return JsonResponse({'message':'Specified vendor is not found'},status=status.HTTP_400_BAD_REQUEST) 
        all_purchase_serializer=POSerSerializer(all_purchase_orders,many=True)
        return JsonResponse(all_purchase_serializer.data,safe=False)
    elif request.method=='POST':
        purchase_order_data=JSONParser().parse(request)
        purchase_order_serializer=POSerSerializer(data=purchase_order_data)
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save()
            return JsonResponse(purchase_order_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(purchase_order_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def purchaseOrderDetail(request,pk):
    try:
        required_purchase_order=PurchaseOrder.objects.get(po_number=pk)
    except:
        return JsonResponse({'message':'Purchase order not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        required_purchase_order_serializer=POSerSerializer(required_purchase_order)
        return JsonResponse(required_purchase_order_serializer.data)
    elif request.method=='PUT':
        required_purchase_order_data=JSONParser().parse(request)
        required_purchase_order_serializer=POSerSerializer(required_purchase_order,data=required_purchase_order_data)
        if required_purchase_order_serializer.is_valid():
            required_purchase_order_serializer.save()
            vendor=required_purchase_order.vendor
            vendor_completed_po=PurchaseOrder.objects.filter(status='completed',vendor=vendor)
            vendor_po=PurchaseOrder.objects.filter(vendor=vendor)
            if 'status' in required_purchase_order_data:
                vendor.fulfillment_rate=len(vendor_completed_po)/len(vendor_po)
            vendor.save()
            if required_purchase_order.status=='completed':
                po_delivered_on_before_del_date=len(PurchaseOrder.objects.filter(status='completed',delivery_date__gte=datetime.now()))
                count=po_delivered_on_before_del_date/len(vendor_completed_po)
                vendor.on_time_delivery_rate=count
                vendor.quality_rating_avg=sum([p.quality_rating for p in vendor_completed_po])/len(vendor_completed_po)
                vendor.save()
            return JsonResponse(required_purchase_order_serializer.data)
        return JsonResponse(required_purchase_order_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        required_purchase_order.delete()
        return JsonResponse({'message':'Purchase order deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def vendorPerformance(request,pk):
    try:
        required_vendor=Vendor.objects.get(vendor_code=pk)
    except:
        return JsonResponse({'message':'Vendor not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        required_vendor_serializer=MetricSerializer(required_vendor)
        return JsonResponse(required_vendor_serializer.data)

@api_view(['POST'])
def acknowledgePO(request,pk):
    try:
        required_purchase_order=PurchaseOrder.objects.get(po_number=pk)
    except:
        return JsonResponse({'message':'Purchase order not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method=='POST':
        required_purchase_order_data=JSONParser().parse(request)
        required_purchase_order.acknowledgment_date=datetime.now()
        required_purchase_order.save()
        vendor=required_purchase_order.vendor
        vendor_po=PurchaseOrder.objects.filter(vendor=vendor)
        vendor.average_response_time=sum([abs((v.issue_date-v.acknowledgment_date).days) for v in vendor_po])/len(vendor_po)
        vendor.save()
        purchase_order_serializer=POSerSerializer(required_purchase_order,data=required_purchase_order_data)
        if purchase_order_serializer.is_valid():
            purchase_order_serializer.save()
            return JsonResponse(purchase_order_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(purchase_order_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
