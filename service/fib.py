#!/usr/bin/env python
import sys
import web
import argparse
import logging

urls = ('/fib/(.*)', 'fib_get')
space = ", "

parser = argparse.ArgumentParser (description = 'Simple Fibonacci numbers web service.')
parser.add_argument ('--verbose'   , action = "store_true", dest = "debug",
                     default = False, help = "Enable verbose diagnostics.")
parser.add_argument ('--cache-size', action = "store"     , dest = "cache_size",
                     type=int, default = 0, help = "Set per-process cache size.")

parser_result = parser.parse_args ()

if parser_result.debug:
    logging.basicConfig (level=logging.DEBUG)
else:
    logging.basicConfig (level=logging.ERROR)

# Return next Fibonacci number and new previous. 
def fib_get_next (cur, prev):
    return (cur + prev, cur)

# Cache class. Stores Fibonacci list of length provided.
class fib_cache:
    data = ""
    marks = []
    last = 1
    last_m1 = 1

    def __init__ (self, size):
        logging.info ("fib_cache: requested " + str (size) + " elements cache.")
        self.init_cache (size)
        if parser_result.debug:
            b = map (str, self.marks)
            logging.debug ("fib_cache: marks are " + str (b))

    def push_cache_entry (self, entry):
        self.data += entry;
        self.marks.append (len (self.data));

    def init_cache (self, cache_size):
        self.data = ""
        self.marks = []
        
        if cache_size is 0:
            return

        if cache_size is 1:
            self.push_cache_entry ("1" + space)
            return

        self.push_cache_entry ("1" + space)
        self.push_cache_entry ("1" + space)

        f_prev = 2;
        f = 3;
        for i in xrange (3, int (cache_size) + 1):           
            self.push_cache_entry (str (f_prev) + space);
            f, f_prev = fib_get_next (f, f_prev)

        self.last = f
        self.last_m1 = f_prev

    def get (self, n):
        if len (self.marks) is 0 or n <= 0:
            return ""
        mark = n - 1 # Numbering starts from 0
        if mark > len (self.marks):
            mark = len (self.marks) - 1 # Saturation: n = MIN (len_of_marks, n)
        logging.info ("== fib_cache: requested number " + str (mark + 1))
        logging.info ("== fib_cache: mark is " + str (self.marks [mark]))
        logging.info ("== fib_cache: returning " + self.data [:self.marks [mark] - len (space)])
        return self.data [:self.marks [mark] - len (space)]

# Cache instance
the_cache = fib_cache (parser_result.cache_size)
    
# Simplest error handling: always return `Bad request'.
class BadRequest (web.HTTPError):
    def __init__(self):
        status = '400'
        headers = {'Content-Type': 'text/html'}
        data = "[]"
        web.HTTPError.__init__(self, status, headers, data)

# Check that value is nonnegative integer less than MAX_INT
def parse_unsigned_int (str):
    try:
        num = int (str)
    except ValueError:
        raise BadRequest
        
    if num < 0:
        raise BadRequest

    if num > sys.maxint:
        raise BadRequest

    return num

# Worker class which handles GET request.
class fib_get:
    def GET (self, fib_num):
        global the_cache;

        fib_num = parse_unsigned_int (fib_num)

        if fib_num is 0:
            return "[]"

        output = "[" + the_cache.get (fib_num)
        # Calculate not cached items
        if fib_num > len (the_cache.marks):
            output += space
            f      = the_cache.last
            f_prev = the_cache.last_m1

            for i in xrange (len (the_cache.marks), fib_num):
                output += str (f_prev)
                if i is not fib_num - 1:
                    output += space
                f, f_prev = fib_get_next (f, f_prev)

        # Fibnonacci numbers are not secret and will unlikely change.
        web.header('Cache-Control', 'public');
        web.header('max-age', 3600 * 24 * 31) #31 days
        return output + "]"

if __name__ == "__main__":
    print "Simple Fibonacci numbers web service."
    app = web.application(urls, globals()) 
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", 8080))
