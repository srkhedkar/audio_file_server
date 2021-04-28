from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Validator for participants list field used in model Podcast
def validate_Participants_list(value):

    if value is not None: 
        if len(value) > 10:
            raise ValidationError(
                ('Number of participants are more than 10'),
                params={'value': value},
            )
        
        for paticipant in value:
            if len(paticipant) > 100:
                raise ValidationError(
                ('Participant length is more than 100 characters'),
                params={'Participant': paticipant},
            )


# Base class to hold common attributes of Song, Podcast and Audiobook
class Base_Music(models.Model):    
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name


# class for defining Song model
class Song(Base_Music):
    pass


# class for defining Podcast model
class Podcast(Base_Music):
    host = models.CharField(max_length=100)
    Participants = models.JSONField(default=list,null=True,blank=True, validators=[validate_Participants_list])


# class for defining Audiobook model
class Audiobook(Base_Music):
    author = models.CharField(max_length=100)
    narrator = models.CharField(max_length=100)    
    
# Factory method to create a Model object using audio file type
def ModelFactory(audioFileType ="song", **kwarg):
      
    """Factory Method"""
    implemented_models = {
        "song": Song,
        "podcast": Podcast,
        "audiobook": Audiobook,
    }

    if ( audioFileType in implemented_models):
        return implemented_models[audioFileType]
    
    # if audioFileType is not supported then raise an exception
    raise Exception(' Audio file type: {} is not supported'.format(audioFileType))

