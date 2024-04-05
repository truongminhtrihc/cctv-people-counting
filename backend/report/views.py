from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from report.models import Metadata
from report.serializers import MetadataSerializer
import datetime

@api_view(["GET"])
def traffic_by_time(request: Request):
    time_span = request.query_params.get("by", "day")
    if time_span == "day":
        time = datetime.datetime.now() - datetime.timedelta(days=1)
    elif time_span == "week":
        time = datetime.datetime.now() - datetime.timedelta(days=7)
    elif time_span == "month":
        time = datetime.datetime.now() - datetime.timedelta(days=30)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = MetadataSerializer(Metadata.objects.filter(time__gte = time), many=True)
    return Response(serializer.data, status.HTTP_200_OK)
    

@api_view(["GET"])
def most_least_traffic(request: Request):
    pass