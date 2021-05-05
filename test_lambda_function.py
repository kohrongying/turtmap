import unittest
from lambda_function import Map


class TestMap(unittest.TestCase):
    def test_show(self):
        im = Map(north=20,
                 south=30,
                 east=40,
                 west=50,
                 central=60
                 )
        im.show()


if __name__ == "__main__":
    unittest.main()
