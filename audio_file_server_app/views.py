from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *

# Default view. Provides the info of offered services.
@api_view(['GET'])
def index(request):
    supported_urls = {
        'Create' : 'audio-create/',
        'Detail View' : 'audio-list/<str:audioFileType>/<str:audioFileID>/',
        'List'   : 'audio-list/<str:audioFileType>/',
        'Update' : 'audio-update/<str:audioFileType>/<str:audioFileID>/',
        'Delete' : 'audio-delete/<str:audioFileType>/<str:audioFileID>/'
        }
    return Response(supported_urls)


# Create view for audio files. Supports all audio types.
@api_view(['POST'])
def audioFileCreate(request):
    
    try:
        valid_req_serializer = ValidateCreateRequestSerializer(data=request.data)
        if valid_req_serializer.is_valid():
            
            # get the corresponding serializer using input fileType.
            serializer = SerializerFactory(valid_req_serializer.getFileType(), data = valid_req_serializer.getAudioMeta())
            
            if  serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)    

            # if input metadata is not valid then return 400 ( Bad Request )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # if input request is not valid then return 400 ( Bad Request )
        return Response(valid_req_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # incase of any IntegrityError / DB error return 500 ( Internal Server Error )
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# list view to fetch all types of audio files. Supports pagination
@api_view(['GET'])
def audioFileList(request, audioFileType, audioFileID=-1):

    try:
        if audioFileID != -1:
            audio_item = ModelFactory(audioFileType).objects.get(id=audioFileID)
            serializer = SerializerFactory(audioFileType, audio_item, many=False)
        else:
            audio_list  = ModelFactory(audioFileType).objects.all()
            paginator   = PageNumberPagination()
            result_page = paginator.paginate_queryset(audio_list, request)
            serializer  = SerializerFactory(audioFileType, result_page, many=True, context={'request':request})
    
        return Response(serializer.data)
    except ObjectDoesNotExist as e:
        # if the queried object is not found then return 404 not found response.
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)

# Update view. Supports all types of audio files.
@api_view(['POST'])
def audioFileUpdate(request, audioFileType, audioFileID):
    
    try: 
        audio_item = ModelFactory(audioFileType).objects.get(id=audioFileID) 
        serializer = SerializerFactory(audioFileType, instance= audio_item, data = request.data)
            
        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)    

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    # if the queried object is not found then return 404 not found response.
    except ObjectDoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete view. Supports all types of audio files.
@api_view(['DELETE'])
def audioFileDelete(request, audioFileType, audioFileID):
    
    try: 
        audio_item = ModelFactory(audioFileType).objects.get(id=audioFileID) 
        audio_item.delete()
            
        return Response("Audio file successfully deleted.", status=status.HTTP_200_OK)      

    # if the queried object is not found then return 404 not found response.
    except ObjectDoesNotExist as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)