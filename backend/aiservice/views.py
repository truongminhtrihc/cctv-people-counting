from django.shortcuts import render
import shutil
import subprocess
import os
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

storage = settings.MEDIA_ROOT
ffmpeg_processes = dict()

@api_view(["GET"])
def stream_url(request: Request):
    camera_id = request.query_params.get("id")
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

    global ffmpeg_processes
    if camera_id not in ffmpeg_processes:
        ffmpeg_processes[camera_id] = subprocess.Popen(command)
    else:
        ffmpeg_processes[camera_id].kill
        ffmpeg_processes[camera_id] = subprocess.Popen(command)
    return Response(status=status.HTTP_201_CREATED)

