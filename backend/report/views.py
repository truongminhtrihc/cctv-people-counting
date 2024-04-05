from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from report.models import Camera, Metadata
from report.serializers import CameraSerializer, MetadataSerializer
from datetime import datetime, timedelta


# Query parameters:
#   day: %d-%m-%y
#   type: day/week/month
#
# Response:
#   {
#       "%camera_id": [[people in 1, people out 1], [people in 2, people out 2],... [people in n, people out n]],
#       "%camera_id": [[people in 1, people out 1], [people in 2, people out 2],... [people in n, people out n]],
#   }
#
# Với n = 24/7/30 khi type = day/week/month
#
@api_view(["GET"])
def traffic_by_time(request: Request):
    date_string = request.query_params.get("day", None)
    graph_type = request.query_params.get("type", "day")
    
    # Chuyển đổi chuỗi ngày/tháng/năm thành đối tượng datetime
    date = datetime.strptime(date_string, "%d-%m-%Y") if date_string else datetime.now()
    
    mapping = {
        "day": [24,1],
        "week": [7,24],
        "month": [30,24]
    }
    # Tính ngày bắt đầu
    start = date - (timedelta(days=1) if (graph_type == "day") else timedelta(days=mapping[graph_type][0]))
    data = []

    if graph_type in mapping:
        range_for, time_add = mapping[graph_type]
        #data = [[Data trong khoảng 1], [Data trong khoảng 2],... [Data trong khoảng n]]
        for i in range(range_for):
            start_time = start + timedelta(hours=i)
            end_time = start + timedelta(hours=i+time_add)
            serializer = MetadataSerializer(Metadata.objects.filter(time__gte=start_time, time__lte=end_time), many=True)
            data += [serializer.data]

        list_cam = {}
        camera_serializer = CameraSerializer(Camera.objects.all(), many=True)
        for camera in camera_serializer.data:
            list_cam[camera["id"]] = []

        for section in data:
            for value in list_cam.values():
                value += [[]]
            for i in section:
                list_cam[i.get("camera")][-1] += [i]    
        #list_cam = {"1": [[Data 1], [Data 2],... [Data n]], "2": [[Data 1], [Data 2],... [Data n]]}
            
        for key, sections in list_cam.items():
            filtered_value = []
            for i in sections:
                if len(i) >= 1:
                    filtered_value += [(i[0]["people_in"]-i[-1]["people_in"], i[0]["people_out"]-i[-1]["people_out"])]
                else:
                    filtered_value += [None]
            list_cam[key] = filtered_value
        
        return Response(list_cam, status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


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