#!/usr/bin/env python
import os, sys

sys.path.append("../python")
from multiplication import karatsuba

if __name__ == "__main__":
    
    dummy1 = karatsuba('3','5')
    print "Dummy check 1: 3*5 = %s " % dummy1
    print "(true = %d)" % (3*5)

    dummy2 = karatsuba('1234','5678')
    print "Dummy check 2: 1234*5678 = %s " % dummy2
    print "(true = %d)"% (1234*5678)

    dummy3 = karatsuba('12345678','87654321')
    print "Dummy check 3: 12345678*87654321 = %s " % dummy3
    print "(true = %d)"% (12345678*87654321)

    dummy4 = karatsuba('213879463746','23657')
    print "Dummy check 4: 213879463746*23657 = %s " % dummy4
    print "(true = %d)"% (213879463746*23657)

    x = '3141592653589793238462643383279502884197169399375105820974944592'
    y = '2718281828459045235360287471352662497757247093699959574966967627'
    xy = karatsuba(x, y)
    print "Product between"
    print x
    print "and"
    print y
    print "Result:"
    print xy
