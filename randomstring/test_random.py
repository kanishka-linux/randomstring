import re
import unittest
from randomstring import RandomString

class TestRandom(unittest.TestCase):
    
    rstring = RandomString(5)
    
    def test_simple_string(self):
        iregex = '[-+]?[0-9]{1,16}[.][0-9]{1,6}?'
        final = self.rstring.generate_random_string(iregex)
        print('\nrandom simple string = {}'.format(final))
        self.assertTrue(re.match(iregex, final))
    
    def test_random_string(self):
        iregex = '([a-f]{5}?[b-r]{9},,)|([^3-9]{4}[.])'
        final = self.rstring.generate_random_string(iregex)
        print('\nrandom string = {}'.format(final))
        self.assertTrue(re.match(iregex, final))
    
    def test_complex_string(self):
        iregex = '(1[0-2]|0[1-9])(:[0-5][0-9]){2}(A|P)M'
        final = self.rstring.generate_random_string(iregex)
        print('\nrandom complex string = {}'.format(final))
        self.assertTrue(re.match(iregex, final))
    
    def test_random_category_string(self):
        iregex = '(1[0-2]|0[1-9])(:[0-5][^\d]{4}\d[\W]+){2}(A|P)M'
        final = self.rstring.generate_random_string(iregex)
        print('\nrandom category string = {}'.format(final))
        self.assertTrue(re.match(iregex, final))
    
    def test_manual_parsing(self):
        iregex = '[-+]?[0-9]{1,16}[.][0-9]{1,6}?'
        final = self.rstring.generate_random_string(iregex, manual=True)
        print('\nrandom manually parsed string = {}'.format(final))
        self.assertTrue(re.match(iregex, final))
        
    
if __name__ == '__main__':
    unittest.main()
