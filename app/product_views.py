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

class ProductList(APIView):
    
    def get(self, req, page):
        res = None
        
        try:
            q = Product.objects.all()
            sort = Sort.from_request(req, 'id')
            qr = q.order_by(*sort)
            p = Paginator(qr, constants.PAGE_SIZE)
            px = p.page(page)
            lx = px.object_list
            pager = Pager(p.count, page, constants.PAGE_SIZE)
            ser = ProductSerializer(lx, many=True, context={ 'request': req })
            return Response({
                'products': ser.data,
                'paging_info': pager,
                'current_category': None
            })
            
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return res
    
class ProductCategoryList(APIView):
    
    def get(self, req, category, page):
        res = None
        
        try:
            q = Product.objects
            if category not in [None, '']:
                q = q.filter(category__iexact=category)
                
            else:
                q = q.all()
                
            sort = Sort.from_request(req, 'id')
            qr = q.order_by(*sort)
            p = Paginator(qr, constants.PAGE_SIZE)
            px = p.page(page)
            lx = px.object_list
            pager = Pager(p.count, page, constants.PAGE_SIZE)
            ser = ProductSerializer(lx, many=True, context={ 'request': req })
            return Response({
                'products': ser.data,
                'paging_info': pager,
                'current_category': category
            })
            
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return res
    
class CategoryList(APIView):
    
    def get(self, req):
        res = None
        
        try:
            lx = Product.objects.values_list('category', flat=True).distinct()
            return Response(lx)
            
        except Exception as e:
            logger.exception(e)
            res = Response({ 'error': 1, 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return res
    