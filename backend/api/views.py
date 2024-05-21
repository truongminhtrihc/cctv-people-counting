import os
import re
import subprocess
from django.conf import settings
from django.db.models import Sum, Avg
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from api.models import Camera, Metadata, DailyTotal
from api.serializers import CameraSerializer, MetadataSerializer, DailyTotalSerializer
from datetime import datetime, timedelta, timezone


@api_view(['GET'])
def get_camera_data(request: Request):
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
def change_camera_name(request: Request):
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
    date_unix = request.query_params.get('date')
    date = datetime.fromtimestamp(float(date_unix), timezone.utc) if date_unix else None
    name = request.query_params.get('name')

    video_list = []
    for root, dirs, files in os.walk(settings.MEDIA_ROOT + "Video"):
        for file in files:
            if file.endswith(".mp4"):
                video_camera_id = root[-1:]
                video_date = file[0:10]
                video_name = file[11:]
                if (camera_id and camera_id != video_camera_id) or (date and date.date() == video_date) or (name and name.lower() not in video_name.lower()):
                    continue
                if video_date is not None:
                    path = video_camera_id + "/" + file
                    video = {
                        "cameraId": video_camera_id,
                        "name": video_name,
                        "date": video_date,
                        "url": path
                    }
                    print(video)
                    video_list.append(video)

    return Response(video_list, status=status.HTTP_200_OK)

def get_traffic(start: datetime) -> dict[str, list[list[int]]]:
    pass

@api_view(["GET"])
def get_traffic_data(request: Request):
    traffic_data = {}

    date_unix = request.query_params.get("date", None)
    date = datetime.fromtimestamp(float(date_unix), timezone.utc) if date_unix else datetime.now(timezone.utc)
    
    camera_list = CameraSerializer(Camera.objects.all(), many=True).data
    for camera in camera_list:
        traffic_data[str(camera["id"])] = {}
        traffic_data[str(camera["id"])]["day"] = [[],[]]
        traffic_data[str(camera["id"])]["week"] = [[],[]]
        traffic_data[str(camera["id"])]["month"] = [[],[]]


        for i in range(24):
            curr = date - timedelta(hours=23 - i)
            d = MetadataSerializer(Metadata.objects.filter(date=curr.date(), hour=curr.hour, camera=camera["id"]), many=True).data
            if len(d) > 0:
                traffic_data[str(camera["id"])]["day"][0] += [d[0]["people_in"]]
                traffic_data[str(camera["id"])]["day"][1] += [d[0]["people_out"]]
            else:
                traffic_data[str(camera["id"])]["day"][0] += [0]
                traffic_data[str(camera["id"])]["day"][1] += [0]

        for i in range(7):
            d = DailyTotalSerializer(DailyTotal.objects.filter(date=(date - timedelta(days=6 - i)).date(), camera=camera["id"]), many=True).data
            if len(d) > 0:
                traffic_data[str(camera["id"])]["week"][0] += [d[0]["people_in"]]
                traffic_data[str(camera["id"])]["week"][1] += [d[0]["people_out"]]
            else:
                traffic_data[str(camera["id"])]["week"][0] += [0]
                traffic_data[str(camera["id"])]["week"][1] += [0]

        for i in range(30):
            d = DailyTotalSerializer(DailyTotal.objects.filter(date=(date - timedelta(days=29 - i)).date(), camera=camera["id"]), many=True).data
            if len(d) > 0:
                traffic_data[str(camera["id"])]["month"][0] += [d[0]["people_in"]]
                traffic_data[str(camera["id"])]["month"][1] += [d[0]["people_out"]]
            else:
                traffic_data[str(camera["id"])]["month"][0] += [0]
                traffic_data[str(camera["id"])]["month"][1] += [0]

    return Response(data=traffic_data)


@api_view(['GET'])
def get_average_traffic_data(request: Request):
    # Logic to get average traffic data
    average_traffic_data = {}

    camera_list = CameraSerializer(Camera.objects.all(), many=True).data
    for camera in camera_list:
        average_traffic_data[str(camera["id"])] = {}
        average_traffic_data[str(camera["id"])]["day"] = [[],[]]
        average_traffic_data[str(camera["id"])]["week"] = [[],[]]
        average_traffic_data[str(camera["id"])]["month"] = [[],[]]


        for i in range(24):
            d = MetadataSerializer(Metadata.objects.filter(hour=i, camera=camera["id"]), many=True).data
            if len(d) > 0:
                sum_in = 0
                sum_out = 0
                for x in d:
                    sum_in += x["people_in"]
                    sum_out += x["people_out"]

                average_traffic_data[str(camera["id"])]["day"][0] += [sum_in / len(d)]
                average_traffic_data[str(camera["id"])]["day"][1] += [sum_out / len(d)]
            else:
                average_traffic_data[str(camera["id"])]["day"][0] += [0]
                average_traffic_data[str(camera["id"])]["day"][1] += [0]

        for i in range(7):
            d = DailyTotalSerializer(DailyTotal.objects.filter(date__week_day=i, camera=camera["id"]), many=True).data
            if len(d) > 0:
                sum_in = 0
                sum_out = 0
                for x in d:
                    sum_in += x["people_in"]
                    sum_out += x["people_out"]

                average_traffic_data[str(camera["id"])]["week"][0] += [sum_in / len(d)]
                average_traffic_data[str(camera["id"])]["week"][1] += [sum_out / len(d)]
            else:
                average_traffic_data[str(camera["id"])]["week"][0] += [0]
                average_traffic_data[str(camera["id"])]["week"][1] += [0]

        for i in range(1, 32):
            d = DailyTotalSerializer(DailyTotal.objects.filter(date__day = i, camera=camera["id"]), many=True).data
            if len(d) > 0:
                sum_in = 0
                sum_out = 0
                for x in d:
                    sum_in += x["people_in"]
                    sum_out += x["people_out"]
                    
                average_traffic_data[str(camera["id"])]["month"][0] += [sum_in / len(d)]
                average_traffic_data[str(camera["id"])]["month"][1] += [sum_out / len(d)]
            else:
                average_traffic_data[str(camera["id"])]["month"][0] += [0]
                average_traffic_data[str(camera["id"])]["month"][1] += [0]

    return Response(average_traffic_data)


@api_view(['GET'])
def get_total_traffic_data(request: Request):
    total_traffic_data = {
        "label": [],
        "day": [[],[]],
        "week": [[],[]],
        "month": [[],[]]
    }

    date_unix = request.query_params.get("date", None)
    date = datetime.fromtimestamp(float(date_unix), timezone.utc) if date_unix else datetime.now(timezone.utc)
    
    camera_list = CameraSerializer(Camera.objects.all(), many=True).data
    for camera in camera_list:
        total_traffic_data["label"] += [camera["name"]]

        d = DailyTotalSerializer(DailyTotal.objects.filter(date=date.date(), camera=camera["id"]), many=True).data
        if len(d) > 0:
            total_traffic_data["day"][0] += [d[0]["people_in"]]
            total_traffic_data["day"][1] += [d[0]["people_out"]]
        else:
            total_traffic_data["day"][0] += [0]
            total_traffic_data["day"][1] += [0]

        
        d = DailyTotalSerializer(DailyTotal.objects.filter(date__gte=(date - timedelta(days=6)).date(), date__lte=date.date(), camera=camera["id"]), many=True).data
        if len(d) > 0:
            sum_in = 0
            sum_out = 0
            for x in d:
                sum_in += x["people_in"]
                sum_out += x["people_out"]
            total_traffic_data["week"][0] += [sum_in]
            total_traffic_data["week"][1] += [sum_out]
        else:
            total_traffic_data["week"][0] += [0]
            total_traffic_data["week"][1] += [0]

        d = DailyTotalSerializer(DailyTotal.objects.filter(date__gte=(date - timedelta(days=29)).date(), date__lte=date.date(), camera=camera["id"]), many=True).data
        if len(d) > 0:
            sum_in = 0
            sum_out = 0
            for x in d:
                sum_in += x["people_in"]
                sum_out += x["people_out"]
            total_traffic_data["month"][0] += [sum_in]
            total_traffic_data["month"][1] += [sum_out]
        else:
            total_traffic_data["month"][0] += [0]
            total_traffic_data["month"][1] += [0]
    return Response(total_traffic_data)


@api_view(['GET'])
def get_average_total_traffic_data(request):
    average_total_traffic_data = {
        "label": [],
        "day": [[],[]],
        "week": [[],[]],
        "month": [[],[]]
    }

    camera_list = CameraSerializer(Camera.objects.all(), many=True).data
    for camera in camera_list:
        average_total_traffic_data["label"] += [camera["name"]]

    d = DailyTotal.objects.values("camera").annotate(people_in=Avg('people_in'), people_out=Avg('people_out'))
        
    for x in d:
        average_total_traffic_data["day"][0] += [x["people_in"]]
        average_total_traffic_data["day"][1] += [x["people_out"]]
            

    return Response(average_total_traffic_data)
