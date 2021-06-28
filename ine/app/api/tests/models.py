from django.test import TestCase
from api.models import Movie, Director


class TestDirector(TestCase):
    """ should be test all cases.
        - invalid fields
        - invalid values in date, director FK
        - insert same name and it should be fail
        - delete
        - get or create
    """
    def setUp(self):
        self.director = Director.objects.get_or_create(name='Campanella')[0]

    def test_director_model(self):
        director = Director.objects.create(
            name="Matt Reeves",
        )
        self.assertEqual(str(director), "Matt Reeves")

    def test_movie_model(self):

        movie = Movie.objects.create(
            title           = 'Batman',
            release_date    = '2021-06-24T14:18:35Z',
            imdb_ranking    = 9.7,
            director        = self.director
        )
        self.assertEqual(str(movie), "Batman")