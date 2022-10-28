
import requests
import json
import os
from .models import Photo
from .serializer import PhotoSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)

        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)\

def render_view(request):
    return render(request, "index.html")

def download_image(url, file_name):
    # Send GET request
    headers = {
        "User-Agent": "Chrome/51.0.2704.103",
    }
    response = requests.get(url + '.png', headers=headers)
    # Save the image
    if response.status_code == 200:
        file_path = os.path.join(BASE_DIR, ('files/' + file_name))
        with open(file_path, "wb") as f:
            f.write(response.content)
    else:
        raise


@api_view(['GET', 'POST'])
def photos_list(request):
    if request.method == 'GET':
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def import_json(request, path):
    response = {}
    with open(os.path.join(BASE_DIR, path)) as f:
        file_data = json.loads(f.read())
        for element in file_data:
            photo = Photo(

                title=element['title'],
                album_id=element['album_id'],
                width=element['width'],
                height=element['height'],
                color=element['color'],
                url=element['url']
            )
            photo.save()
            created = photo.id
            if not created:
                response['status'] = 400
                response['message'] = 'error'
                response['credentials'] = {}
                return Response(response)
        response['status'] = 200
        response['message'] = 'success'
        response['credentials'] = {}
        return Response(response)


@api_view(['GET', 'POST', 'DELETE'])
# imports a photo from api by given id
def import_photo(request, id):
    response = {}
    params = {'id': id}
    response_api = requests.get('https://jsonplaceholder.typicode.com/photos', params=params)
    r_status = response_api.status_code

    if r_status == 200:
        try:
            last_id = Photo.objects.last().id
            file_path = str(int(last_id) + 1) + ".png"
        except:
            last_id = 1
            file_path = str(int(last_id)) + ".png"
        data = response_api.text
        parse_json = json.loads(data)
        photos = parse_json[0]
        download_image(photos['url'], file_path)  # download the image from given url
        color = (photos['url'].split("/"))[4]
        height = (photos['url'].split("/"))[3]
        width = height

        photo = Photo(
            title=photos['title'],
            album_id=photos['albumId'],
            width=width,
            height=height,
            color=color,
            url='files/' + file_path
        )

        photo.save()
        response['status'] = 200
        response['message'] = 'success'
        response['credentials'] = photos

    else:
        response['status'] = response_api.status_code
        response['message'] = 'error'
        response['credentials'] = {}

    return Response(response)


@api_view(['GET', 'PUT', 'DELETE'])
def photo_detail(request, pk):
    try:
        photo = Photo.objects.get(pk=pk)
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# classes
class PhotoAPIView(APIView):

    def get(self, request):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoDetails(APIView):

    def get_object(self, id):
        try:
            return Photo.objects.get(id=id)
        except Photo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        photo = self.get_object(id)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)

    def put(self, request, id):
        photo = self.get_object(id)
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        photo = self.get_object(id)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
