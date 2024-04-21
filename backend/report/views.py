from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from report.models import Camera, Metadata
from report.serializers import CameraSerializer, MetadataSerializer
from datetime import datetime, timedelta


def get_traffic(start: datetime, range_for: int, time_add: int) -> dict[str, list[list[int]]]:
    data = []
    list_cam = {}
    traffic_by_time = {}
    #data = [[Data trong khoảng 1], [Data trong khoảng 2],... [Data trong khoảng n]]
    for i in range(range_for):
        start_time = start + timedelta(hours=i*time_add)
        end_time = start + timedelta(hours=(i+1)*time_add)
        serializer = MetadataSerializer(Metadata.objects.filter(time__gte=start_time, time__lte=end_time), many=True)
        data += [serializer.data]
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
        traffic_by_time[key] = [[], []]
        for i in sections:
            if len(i) > 1:
                filtered_value = [i[0]["people_in"]-i[-1]["people_in"], i[0]["people_out"]-i[-1]["people_out"]]
            elif len(i) == 1 and prev != None:
                filtered_value = [i[0]["people_in"]-prev[-1]["people_in"], i[0]["people_out"]-prev[-1]["people_out"]]
            else:
                filtered_value = [0, 0]
            traffic_by_time[key][0] += [filtered_value[0]]
            traffic_by_time[key][1] += [filtered_value[1]]
            prev = i
    
    return traffic_by_time

"""
Query parameters:
    day: %d-%m-%y
    type: day/week/month

Response:
{
    "%camera_id1": [[people in 1, people in 2,...people in n], [people out 1, people out 2,...people out n]]
    "%camera_id2": [[people in 1, people in 2,...people in n], [people out 1, people out 2,...people out n]],
}

Với n = 24/7/30 khi type = day/week/month
"""
@api_view(["GET"])
def traffic_by_time(request: Request):
    date_string = request.query_params.get("day", None)
    graph_type = request.query_params.get("type", "day")
    
    # Chuyển đổi chuỗi ngày/tháng/năm thành đối tượng datetime
    date = datetime.strptime(date_string, "%d-%m-%Y") if date_string else datetime.now()
    
    mapping = {
        "day": [24, 1],
        "week": [7, 24],
        "month": [30, 24]
    }
    # Tính ngày bắt đầu
    start = date - (timedelta(days=1) if (graph_type == "day") else timedelta(days=mapping[graph_type][0]))

    if graph_type in mapping:
        range_for, time_add = mapping[graph_type]
        return Response(get_traffic(start, range_for, time_add), status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)



# Tìm trong 1 ngày/1 tuần/1 tháng khoảng thời gian nào (giờ/ngày/ngày) có số lượng người ra/vào lớn/nhỏ nhất tương ứng từng camera
@api_view(["GET"])
def most_least_traffic(request: Request):
    date_string = request.query_params.get("day", None)
    time_type = request.query_params.get("timetype", "day")
    inOrOut_type = request.query_params.get("inouttype", "in")
    maxOrMin_type = request.query_params.get("maxormin","max")
    # Chuyển đổi chuỗi ngày/tháng/năm thành đối tượng datetime
    date = datetime.strptime(date_string, "%d-%m-%Y") if date_string else datetime.now()
    
    mapping = {
        "day": [24, 1],
        "week": [7, 24],
        "month": [30, 24]
    }
    # Tính ngày bắt đầu
    start = date - (timedelta(days=1) if (time_type == "day") else timedelta(days=mapping[time_type][0]))
    

    if time_type in mapping:
        range_for, time_add = mapping[time_type]
        traffic_by_time = get_traffic(start, range_for, time_add)
        
        mapping_most = {
        "in": 0,
        "out":1,
        "max": max,
        "min": min
        }
        most_traffic = {}
        for camera_id, records in traffic_by_time.items():
            max_pair = mapping_most[maxOrMin_type](records, key=lambda x: x[mapping_most[inOrOut_type]])
            most_traffic[camera_id] = max_pair

        
        return Response(most_traffic, status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


"""
Query parameter:
    type: day/week/month
    range: %i

Response:
[Average 1, Average 2,... Average n]

Với n = 24/7/30 khi type = day/week/month
"""
@api_view(["GET"])
def average_traffic(request: Request):
    pass

# @api_view(["GET"])
# def camera(request: Request):
#     serializer = CameraSerializer(Camera.objects.all(), many=True)
#     return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
def get_camera_data(request):
    cameras = Camera.objects.all()
    serializer = CameraSerializer(cameras, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
def change_camera_name(request):
    data = request.data
    camera_id = data.get('id')
    new_name = data.get('name')
    try:
        camera = Camera.objects.get(id=camera_id)
    except Camera.DoesNotExist:
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    camera.name = new_name
    camera.save()
    return Response({"message": "Camera name updated successfully"})

@api_view(['GET'])
def get_stream_url(request):
    camera_id = request.query_params.get('id')
    try:
        camera = Camera.objects.get(id=camera_id)
    except Camera.DoesNotExist:
        return Response({"error": "Camera not found"}, status=status.HTTP_404_NOT_FOUND)

    stream_url = f"media/{camera_id}/output.m3u8"
    return Response({"url": stream_url}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_video_list(request):
    camera_id = request.query_params.get('id')
    date = request.query_params.get('date')
    name = request.query_params.get('name')

    # Logic to get video list

    return Response(video_list, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def get_traffic_data(request):
#     date = request.query_params.get('date')

#     # Logic to get traffic data

#     return Response(traffic_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_average_traffic_data(request):
    # Logic to get average traffic data

    return Response(average_traffic_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_total_traffic_data(request):
    date = request.query_params.get('date')

    # Logic to get total traffic data

    return Response(total_traffic_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_average_total_traffic_data(request):
    # Logic to get average total traffic data

    return Response(average_total_traffic_data, status=status.HTTP_200_OK)
