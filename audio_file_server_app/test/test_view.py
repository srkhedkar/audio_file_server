from .test_setup import TestSetUp
from django.urls import reverse       

class TestView(TestSetUp):

    def test_create_song_record(self):
        """
        Testcase       : Create an audio file of type "song".
        Testcase Type  : Positive scenario
        """
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "song",
	        "audioFileMetadata" : {
            "name": "Vande Mataram",
		    "duration" : 300
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
    
    def test_create_record_negative(self):
        """
        Testcase       : Create an audio file of a wrong type "Song".
        Testcase Type  : Negative scenario
        """
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "Song",
	        "audioFileMetadata" : {
            "name": "Vande Mataram",
		    "duration" : 300
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 400)
    
    def test_create_record_negative_2(self):
        """
        Testcase       : Create an audio file of type "song". "audioFileType" is missing in the request
        Testcase Type  : Negative scenario
        """
        create_url = reverse('audio-create')
        data = {	        
	        "audioFileMetadata" : {
            "name": "Vande Mataram",
		    "duration" : 300
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 400)
    
    def test_create_song_record_negative(self):
        """
        Testcase       : Create an audio file of type "song". Set duration to a negative integer.
                       : Duration is a positive integer field. 
        Testcase Type  : Negative scenario
        """
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "song",
	        "audioFileMetadata" : {
            "name": "Vande Mataram",
		    "duration" : -90
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 500)

    def test_create_podcast_record(self):
        """
        Testcase       : Create an audio file of type "podcast".
        Testcase Type  : Positive scenario
        """
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "podcast",
	        "audioFileMetadata" : {
            "name": "My Podcast",
            "duration" : 320,
            "host": "Host1",
            "Participants": ["Amit", "Sumit", "Rina"]
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
    
    def test_create_podcast_record_negative(self):
        """
        Testcase       : Create an audio file of type "podcast". Provide more than 10 participants.
                       : A podcast can have at max 10 paricipants 
        Testcase Type  : negative scenario
        """
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "podcast",
	        "audioFileMetadata" : {
            "name": "My Podcast",
            "duration" : 320,
            "host": "Host1",
            "Participants": ["Amit", "Sumit", "Rina", "AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH"]
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 400)

    def test_create_audiobook_record(self):
        """
        Testcase       : Create an audio file of type "audiobook".
        Testcase Type  : Positive scenario
        """
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "audiobook",
	        "audioFileMetadata" : {
		    "name": "My Audio book",
		    "duration" : 320,
		    "author": "Ramesh Nair",
		    "narrator" : "Pavan Kumar"
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)

    def test_create_audiobook_record_negative(self):
        """
        Testcase       : Create an audio file of type "audiobook". Do not specify author which is a mandetory field.
        Testcase Type  : Positive scenario
        """
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "audiobook",
	        "audioFileMetadata" : {
		    "name": "My Audio book",
		    "duration" : 320,		    
		    "narrator" : "Pavan Kumar"
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 400)

    def test_search_song_records(self):
        """
        Testcase       : Create audio file records of type song. Fetch the records using record id and using audio type.
            A          : Search a record of type song using its id.
            B          : Fetch all records of type song.            

        Testcase Type  : Positive scenario
        """

        # Testcase A:
        # Create a song record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "song",
	        "audioFileMetadata" : {
            "name": "Summer of 69",
		    "duration" : 250
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, search the cretaed song record
        search_url = reverse('audio-detail', kwargs={'audioFileType': 'song', 'audioFileID' : res.data['id']})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 200)
        self.assertEqual(search_res.data['name'], "Summer of 69" )


        # Testcase B:
        # Create another song record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "song",
	        "audioFileMetadata" : {
            "name": "Summer of 69 v2",
		    "duration" : 250
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)

         # Now, fetch all cretaed song records
        search_url = reverse('audio-list', kwargs={'audioFileType': 'song'})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 200)
        self.assertGreaterEqual(len(search_res.data), 2 )

    def test_search_podcast_records(self):
        """
        Testcase       : Create audio file records of type podcast. Fetch the records using record id and using audio type.
            A          : Search a record of type podcast using its id.
            B          : Fetch all records of type podcast.        

        Testcase Type  : Positive scenario
        """

        # Testcase A:
        # Create a podcast record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "podcast",
	        "audioFileMetadata" : {
            "name": "My Podcast new",
            "duration" : 320,
            "host": "Host1",
            "Participants": ["John", "Peter"]
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, search the cretaed podcast record
        search_url = reverse('audio-detail', kwargs={'audioFileType': 'podcast', 'audioFileID' : res.data['id']})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 200)
        self.assertEqual(search_res.data['name'], "My Podcast new" )


        # Testcase B:
        # Create another podcast record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "podcast",
	        "audioFileMetadata" : {
            "name": "My Podcast new_2",
            "duration" : 320,
            "host": "Host1",
            "Participants": ["John", "Peterson"]
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)

         # Now, fetch all created podcast records
        search_url = reverse('audio-list', kwargs={'audioFileType': 'podcast'})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 200)
        self.assertGreaterEqual(len(search_res.data), 2 )

    
    def test_search_audiobook_records(self):
        """
        Testcase       : Create audio file records of type audiobook. Fetch the records using record id and using audio type.
            A          : Search a record of type audiobook using its id.
            B          : Fetch all records of type audiobook.
        Testcase Type  : Positive scenario
        """

        # Testcase A:
        # Create a audiobook record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "audiobook",
	        "audioFileMetadata" : {
		    "name": "Audio book 1",
		    "duration" : 420,
		    "author": "Suresh",
		    "narrator" : "Kavita"
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, search the created audiobook record
        search_url = reverse('audio-detail', kwargs={'audioFileType': 'audiobook', 'audioFileID' : res.data['id']})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 200)
        self.assertEqual(search_res.data['name'], "Audio book 1" )


        # Testcase B:
        # Create another audiobook record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "audiobook",
	        "audioFileMetadata" : {
		    "name": "Audio book 2",
		    "duration" : 420,
		    "author": "Suresh",
		    "narrator" : "Kavita"
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)

         # Now, fetch all created audiobook records
        search_url = reverse('audio-list', kwargs={'audioFileType': 'audiobook'})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 200)
        self.assertGreaterEqual(len(search_res.data), 2 )

    
    def test_update_song_record(self):
        """
        Testcase       : Create audio file records of type song. Update the created record. Change the name.
        Testcase Type  : Positive scenario
        """
  
        # Create a song record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "song",
	        "audioFileMetadata" : {
            "name": "Black and White",
		    "duration" : 550
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, update the created song record
        update_url = reverse('audio-update', kwargs={'audioFileType': 'song', 'audioFileID' : res.data['id']})

        modified_data = {  
            "name": "Black and Blue",
		    "duration" : 550
        }
        update_res = self.client.post(update_url, modified_data, format="json")
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.data['name'], "Black and Blue" )    

    def test_update_podcast_record(self):
        """
        Testcase       : Create audio file records of type podcast. Update the created record. Change the name.
        Testcase Type  : Positive scenario
        """
  
        # Create a podcast record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "podcast",
	        "audioFileMetadata" : {
            "name": "Black Berry",
            "duration" : 320,
            "host": "Host1",
            "Participants": ["John", "Peterson"]
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, update the created podcast record
        update_url = reverse('audio-update', kwargs={'audioFileType': 'podcast', 'audioFileID' : res.data['id']})

        modified_data = {  
            "name": "Blue Berry",
		    "duration" : 550,
            "host": "Host1",
        }
        update_res = self.client.post(update_url, modified_data, format="json")
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.data['name'], "Blue Berry" )   


    def test_update_audiobook_record(self):
        """
        Testcase       : Create audio file records of type audiobook. Update the created record. Change the name.
        Testcase Type  : Positive scenario
        """
  
        # Create a audiobook record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "audiobook",
	        "audioFileMetadata" : {
		    "name": "Book X",
		    "duration" : 420,
		    "author": "Suresh",
		    "narrator" : "Kavita"
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, update the created audiobook record
        update_url = reverse('audio-update', kwargs={'audioFileType': 'audiobook', 'audioFileID' : res.data['id']})

        modified_data = {  
            "name": "Book Y",
		    "duration" : 550,
            "author": "Suresh",
		    "narrator" : "Kavita"
        }
        update_res = self.client.post(update_url, modified_data, format="json")
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.data['name'], "Book Y" ) 

    def test_update_audio_records_Negative(self):
        
        """
        Testcase       : Update a record which does not exists. 
        Testcase Type  : Negative scenario
        """
        
        # Try to update a non existing song record
        update_url = reverse('audio-update', kwargs={'audioFileType': 'song', 'audioFileID' : '999'})
        
        modified_data = {  
            "name": "Black and Blue",
		    "duration" : 550
        }

        update_res = self.client.post(update_url, modified_data, format="json")
        self.assertEqual(update_res.status_code, 404)

        # Try to update a non existing podcast record
        update_url = reverse('audio-update', kwargs={'audioFileType': 'podcast', 'audioFileID' : '999'})
        modified_data = {  
            "name": "Blue Berry",
		    "duration" : 550
        }
        update_res = self.client.post(update_url, modified_data, format="json")
        self.assertEqual(update_res.status_code, 404)

        # Try to update a non existing audiobook record
        update_url = reverse('audio-update', kwargs={'audioFileType': 'audiobook', 'audioFileID' : '999'})
        
        modified_data = {  
            "name": "Book Y",
		    "duration" : 550,
            "author": "Suresh",
		    "narrator" : "Kavita"
        }

        update_res = self.client.post(update_url, modified_data, format="json")
        self.assertEqual(update_res.status_code, 404)

        # Try to update a non existing song record. Send string in audioFileID . Expected response HTTP_500
        update_url = reverse('audio-update', kwargs={'audioFileType': 'song', 'audioFileID' : 'AAA'})
        
        modified_data = {  
            "name": "Black and Blue",
		    "duration" : 550
        }

        update_res = self.client.post(update_url, modified_data, format="json")
        self.assertEqual(update_res.status_code, 500)


    
    def test_delete_song_record(self):
        """
        Testcase       : Create audio file records of type song. Delete the created record. 
        Testcase Type  : Positive scenario
        """
  
        # Create a song record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "song",
	        "audioFileMetadata" : {
            "name": "Black and White v2",
		    "duration" : 550
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, Delete the created song record
        delete_url = reverse('audio-delete', kwargs={'audioFileType': 'song', 'audioFileID' : res.data['id']})
        
        delete_res = self.client.delete(delete_url, format="json")
        self.assertEqual(delete_res.status_code, 200)

        # Now, search the deleted song record
        search_url = reverse('audio-detail', kwargs={'audioFileType': 'song', 'audioFileID' : res.data['id']})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 404)

    def test_delete_podcast_record(self):
        """
        Testcase       : Create audio file records of type podcast. Delete the created record. 
        Testcase Type  : Positive scenario
        """
  
        # Create a podcast record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "podcast",
	        "audioFileMetadata" : {
            "name": "Black Berry 21",
            "duration" : 320,
            "host": "Host1",
            "Participants": ["John", "Peterson"]
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, Delete the created podcast record
        delete_url = reverse('audio-delete', kwargs={'audioFileType': 'podcast', 'audioFileID' : res.data['id']})
        
        delete_res = self.client.delete(delete_url, format="json")
        self.assertEqual(delete_res.status_code, 200)

        # Now, search the deleted podcast record
        search_url = reverse('audio-detail', kwargs={'audioFileType': 'podcast', 'audioFileID' : res.data['id']})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 404)

    def test_delete_audiobook_record(self):
        """
        Testcase       : Create audio file records of type audiobook. Delete the created record. 
        Testcase Type  : Positive scenario
        """
  
        # Create a audiobook record
        create_url = reverse('audio-create')
        data = {
	        "audioFileType" : "audiobook",
	        "audioFileMetadata" : {
		    "name": "Book K",
		    "duration" : 420,
		    "author": "Suresh",
		    "narrator" : "Kavita"
		    }
        }
        res = self.client.post(create_url, data, format="json")
        self.assertEqual(res.status_code, 200)
   
        # Now, Delete the created audiobook record
        delete_url = reverse('audio-delete', kwargs={'audioFileType': 'audiobook', 'audioFileID' : res.data['id']})
        
        delete_res = self.client.delete(delete_url, format="json")
        self.assertEqual(delete_res.status_code, 200)

        # Now, search the deleted podcast record
        search_url = reverse('audio-detail', kwargs={'audioFileType': 'audiobook', 'audioFileID' : res.data['id']})

        search_res = self.client.get(search_url, format="json")
        self.assertEqual(search_res.status_code, 404)

    def test_delete_audio_records_Negative(self):
        """
        Testcase       :  Delete a record which does not exists. 
        Testcase Type  : Negative scenario
        """
        
        # Try to delete a non existing song record
        delete_url = reverse('audio-delete', kwargs={'audioFileType': 'song', 'audioFileID' : '999'})
        
        delete_res = self.client.delete(delete_url, format="json")
        self.assertEqual(delete_res.status_code, 404)

        # Try to delete a non existing podcast record
        delete_url = reverse('audio-delete', kwargs={'audioFileType': 'podcast', 'audioFileID' : '999'})
        
        delete_res = self.client.delete(delete_url, format="json")
        self.assertEqual(delete_res.status_code, 404)

        # Try to delete a non existing audiobook record
        delete_url = reverse('audio-delete', kwargs={'audioFileType': 'audiobook', 'audioFileID' : '999'})
        
        delete_res = self.client.delete(delete_url, format="json")
        self.assertEqual(delete_res.status_code, 404)

        

           