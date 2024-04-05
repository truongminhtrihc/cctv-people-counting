from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from report.models import Metadata
from report.serializers import MetadataSerializer
from datetime import datetime

@api_view(["GET"])
def traffic_by_time(request: Request):
    start = request.query_params.get("start")
    end = request.query_params.get("end")
    typeGraph = request.query_params.get("typeGraph")
    
    # Chuyển đổi chuỗi ngày/tháng/năm thành đối tượng datetime
    start = datetime.strptime(start, "%d-%m-%Y")
    end = datetime.strptime(end, "%d-%m-%Y")
    # Chuyển đổi đối tượng datetime thành chuỗi định dạng ISO 8601
    start = start.isoformat()
    end = end.isoformat()
    
    mappingForType = {
        "day": [24,1],
        "week": [7,24],
        "month": [30,24]
    }
    
    trafficByTime = []
    if typeGraph in mappingForType:
        rangeFor,timeAdd = mappingForType[typeGraph]
        for i in range(rangeFor):
            startTmp = start + datetime.timedelta(hours=i)
            endTmp = startTmp + datetime.timedelta(hours=i+timeAdd)
            serializer = MetadataSerializer(Metadata.objects.filter(time__gte=startTmp, time__lte=endTmp), many=True)
        listCam = {}
        for i in serializer.data:
            if i.get("camera") in listCam:
                listCam[i.get("camera")] += [i]
            else: 
                listCam[i.get("camera")] = [i]
        for key, value in listCam.items():
            filtered_value = [value[0], value[-1]]
            listCam[key] = filtered_value
        trafficByTime+=[listCam]
        
        return Response(serializer.data, status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
    # listCam trả về dict của các camera cấu trúc { <id của camera> :[matadata max, metadate min]}
    # neu type la day res cos danjg [{}{}{}...] 24 entry 1 entry tuon ung { <id của camera> :[matadata max, metadate min]}
    # neu type la week res cos danjg [{}{}{}...] 7 entry 1 entry tuon ung { <id của camera> :[matadata max, metadate min]}
    
    
    

@api_view(["GET"])
def most_least_traffic(request: Request):
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