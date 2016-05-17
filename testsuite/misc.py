import unittest
import fib

class test_fib_get_next (unittest.TestCase):
    def test_fib_initial (self):
        self.assertEqual(fib.fib_get_next (1, 1), (2, 1))

    def test_fib_rec (self):
        self.assertEqual(fib.fib_get_next (2, 1), (3, 2))

class test_fib_cache (unittest.TestCase):
     cache = fib.fib_cache (5)
     cache_z = fib.fib_cache (0)
     def test_data_init (self):
        self.assertEqual (self.cache.data, "1, 1, 2, 3, 5, ")
        self.assertEqual (self.cache_z.data, "")

     def test_marks_init (self):
        self.assertEqual (self.cache.marks, [3, 6, 9, 12, 15])
        self.assertEqual (self.cache_z.marks, [])

     def test_lasts (self):
        self.assertEqual (self.cache.last, 13)
        self.assertEqual (self.cache.last_m1, 8)

        self.assertEqual (self.cache_z.last, 1)
        self.assertEqual (self.cache_z.last_m1, 1)

     def test_get (self):
        self.assertEqual (self.cache.get (0), "")
        self.assertEqual (self.cache.get (1), "1")
        self.assertEqual (self.cache.get (2), "1, 1")
        self.assertEqual (self.cache.get (10), "1, 1, 2, 3, 5")

        self.assertEqual (self.cache_z.get (1), "")
        self.assertEqual (self.cache_z.get (0), "")

class parse_unsigned_int (unittest.TestCase):
    def test_normal (self):
        self.assertEqual (fib.parse_unsigned_int ("1"), 1)
        
    def test_negative (self):
        with self.assertRaises (Exception): fib.parse_unsigned_int ("-1")

    def test_symbol (self):
        with self.assertRaises (Exception): fib.parse_unsigned_int ("a")

    def test_max_int (self):
        with self.assertRaises (Exception): fib.parse_unsigned_int ("100000000000000000000000000")

def suite ():
	test = unittest.TestLoader ()
        test.loadTestsFromTestCase (test_fib_get_next)
	test.loadTestsFromTestCase (test_fib_cache)
        test.loadTestsFromTestCase (parse_unsigned_int)
	return test

if __name__ == '__main__':
	unittest.main()
