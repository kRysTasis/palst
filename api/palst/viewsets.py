from rest_framework import (
    generics,
    permissions,
    authentication,
    status,
    viewsets,
    filters
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .serializers import (
    StockSerializer,
    CompanySerializer,
)

from .models import (
    mUser,
    Stock,
    Company
)

import requests
import pytz
from datetime import (
    date,
    datetime,
    timedelta,
    timezone
)

class CompanyViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def list(self, request, *args, **kwargs):
        """
        一覧：
            直近1習慣(7個)*会社数をページに分けて
        個別：
            1社の全期間(5年)
        """

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CompanySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
