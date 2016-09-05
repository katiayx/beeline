""""""

import unittest
from unittest import TestCase
import doctest
from server import app
import parse_dist


def load_tests(loader, tests, ignore):
    """run file-based doctests."""

    tests.addTests(doctest.DocTestSuite(parse_dist))
    return tests


class FlaskTests(TestCase):
    """Flask tests to test routes are correctly connected"""

    def setUp(self):
        """testing setup"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure homepage is rendering correctly"""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h3>Starting from?</h3>',
                        result.data)

    def test_route_map(self):
        """Test location inputs are being passed to the right route"""

        result = self.client.post('/route_map',
                                data=
                                    {'loc':
                                        ['San Francisco', 
                                        'Los Angeles', 
                                        'Oakland', 
                                        'Palo Alto',
                                        'Mission Viejo'],
                                    })
        self.assertEqual(result.status_code, 200)
        self.assertIn('New Search',
                        result.data)
        print result.data



if __name__ == "__main__":
    unittest.main()