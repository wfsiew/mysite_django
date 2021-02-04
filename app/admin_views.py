from django.http import Http404
from django.conf import settings
from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import *
from app.general_models import *
from app.serializers import *
from app import constants

from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ProductList(APIView):
    
    def get(self, req):
        res = None
        
        try:
            q = Product.objects.all()
            ser = ProductSerializer(q, many=True, context={ 'request': req })
            return Response(ser.data)
        
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return res
    
class ProductEdit(APIView):
    
    def get(self, req, id):
        res = None
        
        try:
            o = Product.objects.get(pk=id)
            ser = ProductSerializer(o)
            return Response(ser.data)
            
        except Product.DoesNotExist:
            res = Response({ 'error': 1, 'message': 'Product not found' }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_400_BAD_REQUEST)
            
        return res
    
    def put(self, req, id):
        res = None
        
        try:
            data = req.data
            o = Product.objects.get(pk=id)
            o.name = data['name']
            o.description = data['description']
            o.price = data['price']
            o.category = data['category']
            o.save()
            return Response({ 'success': 1 })
        
        except Product.DoesNotExist:
            res = Response({ 'error': 1, 'message': 'Product not found' }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_400_BAD_REQUEST)
            
        return res
    
    def delete(self, req, id):
        res = None
        
        try:
            o = Product.objects.filter(pk=id).delete()
            return Response({ 'success': 1 })
            
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_400_BAD_REQUEST)
            
        return res
    
class ProductSeed(APIView):
    
    def post(self, req):
        res = None
        
        try:
            for i in range(500):
                o = Product(
                    name='Product - {0}'.format(i),
                    description='Product Desc - {0}'.format(i),
                    price=100.0 + i,
                    category='Soccer'
                )
                o.save()
                
            return Response({ 'success': 1 })
        
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return res
                