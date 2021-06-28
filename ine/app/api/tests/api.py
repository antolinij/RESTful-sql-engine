# utils tools
import ipdb
import json
from urllib.parse import urlencode

# Django
from django.test import TestCase
from django.urls import reverse
from django.core import serializers

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

# Models
from django.contrib.auth.models import User
from api.models import Director, Movie


class CreateNewMovieTestCase(TestCase):
    def setUp(self):

        self.client = APIClient()

        user = User(
            email='testing_login@cosasdedevs.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )

        user.set_password('admin123')
        user.save()

        self.token, created = Token.objects.get_or_create(user=user)

    def test_create_movie_valid_payload(self):
        """ 201 CREATED. Create a movie with valid payload """

        director = Director.objects.get_or_create(name='Campanella')[0]

        valid_payload = {
            'title': 'Batman',
            'release_date': '2021-06-24T14:18:35Z',
            'imdb_ranking': 9.7,
            'director': director.id
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Movie'})
        
        response = self.client.post(
            url, 
            data=json.dumps(valid_payload), 
            content_type='application/json'
        )

        result = json.loads(response.content)

        if 'id' in result:
            del result['id']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result, valid_payload)

    def test_create_movie_invalid_payload(self):
        """ BAD REQUEST. Body invalid, director is empty. """
        empty_field_payload = {
            'title': 'Batman',
            'release_date': '2021-06-24T14:18:35Z',
            'imdb_ranking': 9.7,
            'director': ''
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Movie'})

        response = self.client.post(
            url, 
            data=json.dumps(empty_field_payload), 
            content_type='application/json'
        )
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result, {'director': ['This field may not be null.'], 'status_code': 400})

    def test_create_movie_incomplete_payload(self):
        """ BAD REQUEST. Body invalid, director is MISSING. """

        incomplete_payload = {
            'title': 'Batman',
            'release_date': '2021-06-24T14:18:35Z',
            'imdb_ranking': 9.7,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Movie'})
        
        response = self.client.post(
            url, 
            data=json.dumps(incomplete_payload), 
            content_type='application/json'
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result, {'detail': 'IntegrityError(\'null value in column "director_id" violates not-null constraint\\nDETAIL:  Failing row contains (1, Batman, 2021-06-24 14:18:35+00, 9.7, null).\\n\')', 'status_code': 400})

class GetMovieTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()
    
        user = User(
            email='testing_login@cosasdedevs.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )

        user.set_password('admin123')
        user.save()

        self.token, created = Token.objects.get_or_create(user=user)

        self.director = Director.objects.get_or_create(name='Campanella')[0]
        self.movie = Movie.objects.get_or_create(
            title           = 'Batman',
            release_date    = '2021-06-24T14:18:35Z',
            imdb_ranking    = 9.7,
            director        = self.director
        )[0]
    
    def test_get_with_invalid_fields_in_params(self):
        """ 400 BAD REQEST. Get inexistent fields in Model Movie """
        #ipdb.set_trace()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        base_url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Movie'})

        # add some invalid fields 
        query_kwargs={'fields': 'po'}        
        url = '{}?{}'.format(base_url, urlencode(query_kwargs))
        
        response = self.client.get(url)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result,'Field name `po` is not valid for model `Movie`.')
    
    def test_get_all_movies(self):
        """ 200 OK. Get all movies """
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Movie'})     
        
        # should use mockFactory like bakery or in setUp
        
        response = self.client.get(url)
        result = json.loads(response.content)

        # convert result without id
        movies_result = []
        for res in result:
            if 'id' in res:
                del res['id']
                movies_result.append(res)

        movies = json.loads( 
            serializers.serialize("json", Movie.objects.all())
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movies_result, [movie['fields'] for movie in movies])

    def test_get_movies_whitout_results(self):
        """ 200 OK. Get movies in empty database. """
        
        Movie.objects.all().delete()
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Movie'})     
        
        response = self.client.get(url)
        result = json.loads(response.content)

        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result,[])


    def test_get_movie_without_token(self):
        """ 401 UNAUTHORIZED. Request whitout token in header """

        url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Movie'})

        director = Director.objects.get_or_create(name='Campanella')[0]
        valid_payload = {
            'title': 'Batman',
            'release_date': '2021-06-24T14:18:35Z',
            'imdb_ranking': 9.7,
            'director': director.id
        }  
        
        response = self.client.post(
            url, 
            data=json.dumps(valid_payload), 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ExtraFunctionalityTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()
    
        user = User(
            email='testing_login@cosasdedevs.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )

        user.set_password('admin123')
        user.save()

        self.token, created = Token.objects.get_or_create(user=user)

    def test_without_token(self):
        """ 401 UNAUTHORIZED. Request whitout token in header """

        url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Movie'})

        director = Director.objects.get_or_create(name='Campanella')[0]
        valid_payload = {
            'title': 'Batman',
            'release_date': '2021-06-24T14:18:35Z',
            'imdb_ranking': 9.7,
            'director': director.id
        }  
        
        response = self.client.post(
            url, 
            data=json.dumps(valid_payload), 
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_table_doesnot_exist(self):

        
        url = reverse('general_models', kwargs={'database_name':'ine_database','table_name': 'Foo'})        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.get(url)

