import shutil
import subprocess
import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from report.models import Metadata
from report.serializers import MetadataSerializer
import datetime

storage = "D:/TestStream/"

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

@api_view(["GET"])
def stream_url(request: Request):
    camera_id = request.query_params.get("id")
    print(camera_id)
    if camera_id and os.path.exists(storage + camera_id):
        return Response("media/" + camera_id + "/output.m3u8", status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def stream(request: Request):
    ip = request.data.get("ip")
    camera_id = request.data.get("id")
    shutil.rmtree(storage + camera_id, ignore_errors=True)
    os.makedirs(storage + camera_id)
    command = [
        'ffmpeg',
        '-i', ip,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-f', 'hls',
        '-hls_time', '10',
        '-hls_list_size', '6',
        '-hls_flags', 'delete_segments',
        storage + camera_id + '/output.m3u8'
    ]
    subprocess.Popen(command)
    return Response(status=status.HTTP_201_CREATED)
