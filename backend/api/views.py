import subprocess
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from api.models import Camera, Metadata, DailyTotal
from api.serializers import CameraSerializer, MetadataSerializer, DailyTotalSerializer
from datetime import datetime, timedelta, timezone


@api_view(['GET'])
def get_camera_data(request):
    cameras = Camera.objects.all()
    serializer = CameraSerializer(cameras, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def get_stream_url(request: Request):
    camera_id = request.query_params.get("id")
    try:
        serializer = CameraSerializer(Camera.objects.get(id=camera_id))
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if check_stream(serializer.data.get("video_ip")):
        return Response(settings.MEDIA_URL[1:] + camera_id + '/output.m3u8', status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

def check_stream(video_ip: str) -> bool:
    command = ['ffprobe', '-timeout', '10000000', '-loglevel', 'quiet', video_ip]
    process = subprocess.run(command)
    return process.returncode == 0

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
def get_video_list(request: Request):
    camera_id = request.query_params.get('id')
    date = request.query_params.get('date')
    name = request.query_params.get('name')

    # Logic to get video list

    return Response(video_list, status=status.HTTP_200_OK)

def get_traffic(start: datetime) -> dict[str, list[list[int]]]:
    pass

@api_view(["GET"])
def get_traffic_data(request: Request):
    data = {}

    date_unix = request.query_params.get("date", None)
    date = datetime.fromtimestamp(float(date_unix), timezone.utc) if date_unix else datetime.now(timezone.utc)
    
    camera_list = CameraSerializer(Camera.objects.all(), many=True).data
    for camera in camera_list:
        data[str(camera["id"])] = {}
        data[str(camera["id"])]["day"] = [[],[]]
        data[str(camera["id"])]["week"] = [[],[]]
        data[str(camera["id"])]["month"] = [[],[]]


        for i in range(24):
            curr = date - timedelta(hours=23 - i)
            d = MetadataSerializer(Metadata.objects.filter(date=curr.date(), hour=curr.hour, camera=camera["id"]), many=True).data
            if len(d) > 0:
                data[str(camera["id"])]["day"][0] += [d[0]["people_in"]]
                data[str(camera["id"])]["day"][1] += [d[0]["people_out"]]
            else:
                data[str(camera["id"])]["day"][0] += [0]
                data[str(camera["id"])]["day"][1] += [0]

        for i in range(7):
            d = DailyTotalSerializer(DailyTotal.objects.filter(date=(date - timedelta(days=6 - i)).date(), camera=camera["id"]), many=True).data
            if len(d) > 0:
                data[str(camera["id"])]["week"][0] += [d[0]["people_in"]]
                data[str(camera["id"])]["week"][1] += [d[0]["people_out"]]
            else:
                data[str(camera["id"])]["week"][0] += [0]
                data[str(camera["id"])]["week"][1] += [0]

        for i in range(30):
            d = DailyTotalSerializer(DailyTotal.objects.filter(date=(date - timedelta(days=29 - i)).date(), camera=camera["id"]), many=True).data
            if len(d) > 0:
                data[str(camera["id"])]["month"][0] += [d[0]["people_in"]]
                data[str(camera["id"])]["month"][1] += [d[0]["people_out"]]
            else:
                data[str(camera["id"])]["month"][0] += [0]
                data[str(camera["id"])]["month"][1] += [0]
    
    return Response(data=data)


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
