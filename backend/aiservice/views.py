from django.http import HttpRequest
from django.shortcuts import render
import shutil
import subprocess
import os
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from report.models import Camera
from report.serializers import CameraSerializer, MetadataSerializer

storage = settings.MEDIA_ROOT
ffmpeg_processes = dict()

"""
Query parameter:
    camera_id: str
    refresh: 1/None

Response:
    string link to hls stream file
"""
@api_view(["GET"])
def stream_url(request: Request):
    camera_id = request.query_params.get("id")
    refresh = request.query_params.get("refresh")
    try:
        serializer = CameraSerializer(Camera.objects.get(id=camera_id))
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    global ffmpeg_processes
    if check_stream(serializer.data.get("ip")):
        if camera_id in ffmpeg_processes:
            return Response("media/" + camera_id + "/output.m3u8", status.HTTP_200_OK)
        if refresh:
            create_stream(serializer.data.get("ip"), camera_id)
            return Response("media/" + camera_id + "/output.m3u8", status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

"""
Request:
{
    "port": "%camera_port"
    "camera_id": "%camera_id"
}
"""
@api_view(["POST"])
def stream(request: HttpRequest):
    port = str(request.data.get("port"))
    camera_id = str(request.data.get("id"))
    ip = 'rtsp://' + request.META.get("REMOTE_ADDR") + ':' + port + '/'
    if check_stream(ip):
        try:
            CameraSerializer(Camera.objects.get(id=camera_id), data={ip: ip}, partial=True)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        create_stream(ip, camera_id)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

"""
Request:
{
    "camera": %i,
    "people_in": %i,
    "people_out": %i
}
"""
@api_view(["POST"])
def metadata(request: Request):
    serializer = MetadataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def create_stream(ip: str, camera_id: str):
    command = [
        'ffmpeg',
        '-i', ip,
        '-vf', 'select=concatdec_select',
        '-af', 'aselect=concatdec_select,aresample=async=1',
        '-c:a', 'aac',
        '-f', 'hls',
        '-hls_time', '10',
        '-hls_list_size', '6',
        '-hls_flags', 'delete_segments',
        storage + camera_id + '/output.m3u8'
    ]

    global ffmpeg_processes
    if camera_id in ffmpeg_processes:
        ffmpeg_processes[camera_id].kill()
    shutil.rmtree(storage + camera_id, ignore_errors=True)
    os.makedirs(storage + camera_id)
    ffmpeg_processes[camera_id] = subprocess.Popen(command)

def check_stream(ip: str) -> bool:
    command = ['ffprobe', '-timeout', '1000000', ip]
    process = subprocess.run(command)
    return process.returncode == 0