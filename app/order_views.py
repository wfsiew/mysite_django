from django.http import Http404
from django.conf import settings
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import *
from app.general_models import *
from app.serializers import *
from app import constants, make_json_serializable

from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class OrderList(APIView):
    
    def get(self, req):
        res = None
        
        try:
            q = Order.objects.exclude(shipped=True).all()
            ser = OrderSerializer(q, many=True, context={ 'request': req })
            return Response(ser.data)
        
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return res
    
class OrderMarkShipped(APIView):
    
    def post(self, req, id):
        res = None
        
        try:
            o = Order.objects.get(pk=id)
            o.shipped = True
            o.save()
            return Response({ 'success': 1 })
        
        except Order.DoesNotExist:
            res = Response({ 'error': 1, 'message': 'Order not found' }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_400_BAD_REQUEST)
            
        return res
    
class OrderCheckout(APIView):
    
    def post(self, req):
        res = None
        
        try:
            data = req.data
            order = data['order']
            lines = data['lines']
            
            with transaction.atomic():
                o = Order(
                    name=order['name'],
                    line1=order['line1'],
                    line2=order['line2'],
                    line3=order['line3'],
                    city=order['city'],
                    state=order['state'],
                    postcode=order['postcode'],
                    country=order['country'],
                    giftwrap=bool(order['giftwrap']),
                    shipped=False
                )
                o.save()
                
                for line in lines:
                    product_id = line['product']['id']
                    product = Product.objects.get(pk=product_id)
                    x = CartLine(
                        product=product,
                        quantity=int(line['quantity']),
                        order=o
                    )
                    x.save()
                    
            return Response({ 'success': 1 })
        
        except Product.DoesNotExist:
            res = Response({ 'error': 1, 'message': 'Product not found' }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_400_BAD_REQUEST)
            
        return res
    