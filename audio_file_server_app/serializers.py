from rest_framework import serializers
from .models import *

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields= "__all__"

class PodcastSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Podcast
        fields= "__all__"


class AudiobookSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Audiobook
        fields= "__all__"


# Serializer to valide input create request
class ValidateCreateRequestSerializer(serializers.Serializer):
    # ToDo : Supported song types should be moved to a common static list
    supportedFileTypes = ('song', 'podcast', 'audiobook')
    audioFileType = serializers.ChoiceField(required=True, choices=supportedFileTypes)
    audioFileMetadata = serializers.JSONField(required=True)

    def getAudioMeta(self):
        return self.validated_data.get('audioFileMetadata')
    
    def getFileType(self):
        return self.validated_data.get('audioFileType')

# Factory method to create a Serializer object using audio file type
def SerializerFactory(audioFileType ="song", *args, **kwarg):
      
    """Factory Method"""
    serializers = {
        "song": SongSerializer,
        "podcast": PodcastSerializer,
        "audiobook": AudiobookSerializer,
    }

    if ( audioFileType in serializers):
        return serializers[audioFileType](*args, **kwarg)
    
    raise Exception(' Audio file type: {} is not supported'.format(audioFileType))

    