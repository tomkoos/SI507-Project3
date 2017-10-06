import unittest
from si507f17_project3_code import *

# NOTE: sample_html_of_park.html, provided, must be in your directory to be able to run all these tests

# NOTE: Running these tests on your complete code may take a minute -- especially if your code to write CSVs rewrites them every time.

###########

# REMEMBER, these tests DO NOT test everything in the project.

class Part1(unittest.TestCase):
    def setUp(self):
        self.mainpage = open("nps_gov_data.html", encoding='utf8')
        self.akfile = open("arkansas_data.html", encoding='utf8')
        self.cafile = open("california_data.html", encoding='utf8')
        self.mifile = open("michigan_data.html", encoding='utf8')

    def test_files_exist(self):
        self.assertTrue(self.mainpage.read())
        self.assertTrue(self.akfile.read())
        self.assertTrue(self.cafile.read())
        self.assertTrue(self.mifile.read())

    def tearDown(self):
        self.mainpage.close()
        self.akfile.close()
        self.cafile.close()
        self.mifile.close()

class Part2(unittest.TestCase):
    def setUp(self):
        self.f = open("sample_html_of_park.html",'r')
        self.soup_park_inst = BeautifulSoup(self.f.read(),'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
        self.sample_inst = NationalSite(self.soup_park_inst)
        self.f.close()

    def test_nationalsite_constructor(self):
        self.assertIsInstance(self.sample_inst.name, str)
        self.assertTrue((self.sample_inst.type is None) or (type(self.sample_inst.type) == type("")))
        self.assertIsInstance(self.sample_inst.description, str)
        self.assertIsInstance(self.sample_inst.location, str)

    def test_nationalsite_get_address(self):
        self.assertIsInstance(self.sample_inst.get_mailing_address(),str)

    def test_nationalsite_string(self):
        self.assertEqual(self.sample_inst.__str__(), "Isle Royale | Houghton, MI")

    def test_nationalsite_contains(self):
        self.assertTrue("le" in self.sample_inst)
        self.assertTrue("Yosemite" not in self.sample_inst)

class Part3(unittest.TestCase):

    def setUp(self):
        pass

    def test_list_vars(self):
        self.assertIsInstance(arkansas_natl_sites,list)
        self.assertIsInstance(california_natl_sites, list)
        self.assertIsInstance(michigan_natl_sites, list)

    def test_list_elem_types(self):
        self.assertIsInstance(arkansas_natl_sites[0],NationalSite)
        self.assertIsInstance(arkansas_natl_sites[-1],NationalSite)
        self.assertIsInstance(california_natl_sites[0],NationalSite)
        self.assertIsInstance(michigan_natl_sites[0],NationalSite)


class Part4(unittest.TestCase):
    
    def setUp(self):
        self.ak = open("arkansas.csv",'r')
        self.mi = open("michigan.csv",'r')
        self.ca = open("california.csv",'r')

    def test_csv_files_exist(self):
        self.assertTrue(self.ak.read())
        self.assertTrue(self.ca.read())
        self.assertTrue(self.mi.read())

    def tearDown(self):
        self.ak.close()
        self.ca.close()
        self.mi.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)