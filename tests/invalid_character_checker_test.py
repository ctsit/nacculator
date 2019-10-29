import unittest
import re

# from nacc import redcap2nacc
from nacc.redcap2nacc import check_for_bad_characters


class field():
    name = 'FOTHMUSX'
    value = '\'O%h& \'No'


class TestInvalidCharacters(unittest.TestCase):

    
    def test_find_any_characters(self):
        found = check_for_bad_characters(field)
        self.assertTrue(found)

        
    def test_many_characters(self):
        found_many = check_for_bad_characters(field)
        many = len(found_many)
        single = [0, 1]
        self.assertNotIn(many, single)
        

    def test_closed_double_quotes(self):
        found_two_doublequotes = check_for_bad_characters(field)
        dups = found_two_doublequotes[1]
        self.assertEqual(dups, '" (2)')
        

    def test_closed_single_quotes(self):
        found_two_quotes = check_for_bad_characters(field)
        dups1 = found_two_quotes[0]
        self.assertEqual(dups1, '\' (2)')
        

    # This one ended up not mattering- 
    # the csv file takes care of closed double quotes within excel
    def test_doubles_but_no_singles(self):
        chars = check_for_bad_characters(field)
        char_search = str(chars)
        quote = re.search("'", char_search)
        dquote = re.search('"', char_search)
        self.assertFalse(quote)
        self.assertTrue(dquote)





if __name__ == "__main__":
    unittest.main()