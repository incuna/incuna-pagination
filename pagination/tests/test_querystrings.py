from django.http import QueryDict

from .utils import RequestTestCase
from ..templatetags import querystrings


class TestQuerystringUpdate(RequestTestCase):
    def setUp(self):
        """Create a request and put some GET args in it."""
        self.request = self.create_request()
        self.request.GET = QueryDict('page=3&q=search_term')

    def test_unchanged_querystring(self):
        """Test that the method returns an unchanged request.GET if kwargs is empty."""
        querystring = querystrings.querystring_update(self.request)

        # Re-parse the result into a dict because the query arguments don't appear in
        # a predictable order.
        new_querydict = QueryDict(querystring).dict()
        expected = {
            'page': '3',
            'q': 'search_term',
        }
        self.assertEqual(new_querydict, expected)

    def test_querystring_update(self):
        """Test that individual GET arguments are updated or preserved correctly."""
        search_term = 'a_different_search_term'
        querystring = querystrings.querystring_update(self.request, q=search_term)

        # Re-parse the result into a dict because the query arguments don't appear in
        # a predictable order.
        new_querydict = QueryDict(querystring).dict()
        expected = {
            'page': '3',
            'q': search_term,
        }
        self.assertEqual(new_querydict, expected)
