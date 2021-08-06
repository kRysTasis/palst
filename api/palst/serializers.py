from rest_framework import serializers
from .models import (
    mUser,
    Stock,
    Company
)
import pytz
import logging
from datetime import (
    datetime,
    timezone,
    timedelta
)
from django.utils import timezone as timezone_django
from django.db.models import Q

logging.basicConfig(
    level = logging.DEBUG,
    format = '''%(levelname)s %(asctime)s %(pathname)s:%(funcName)s:%(lineno)s
    %(message)s''')


logger = logging.getLogger(__name__)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)



class StockSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'

class CompanySerializer(DynamicFieldsModelSerializer):

    stock = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        logger.debug(kwargs)
        if 'context' in kwargs and 'detail' in kwargs['context']:
            self.detail = kwargs['context']['detail']

        super().__init__(*args, **kwargs)

    class Meta:
        model = Company
        fields = [
            'code',
            'name',
            'stock',
        ]

    def get_stock(self, obj):
        if hasattr(self, 'detail'):
            return StockSerializer(
                Stock.objects.filter( \
                    Q(code=obj.code)
                ), many=True).data
        else:
            now = datetime.now(timezone(timedelta(hours=9)))
            return StockSerializer(
                Stock.objects.filter( \
                    Q(code=obj.code) & \
                    Q(timestamp__range=[now - timedelta(days=7), now]) \
                ), many=True).data
