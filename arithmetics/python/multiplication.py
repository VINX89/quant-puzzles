#!/usr/bin/env python

def karatsuba(x, y, debug=False):
    '''Implement Karatsuba algorithm for multiplication
    between integer numbers.
    Given two integers x and y of length nx and ny,
    each number is parameterised as
    
    x = 10^n/2 a + b
    y = 10^n/2 c + d

    where n = min(nx,ny)

    Then, the product xy is

    xy = 10^n ac + 10^n/2 (ad+bc) + bd

    where ac and bd are computed iteratively.
    
    For ad+bc, the "Gauss trick" is used:

    ad+bc = (a+b)(c+d) - ac - db

    So, only 3 iterative multiplications are needed, namely
    for ac, bd and (a+b)(c+d)

    @param x first number (as string)
    @param y second number (as string)
    @returns the product xy (as string)
    '''
    
    n_2 = len( str(min(int(x),int(y))) ) / 2
    
    if n_2 < 2:
        return str( int(x) * int(y) )

    a = x[:(len(x)-n_2)]
    b = x[-n_2:]
    c = y[:(len(y)-n_2)]
    d = y[-n_2:]

    ac = karatsuba(a, c, debug)
    bd = karatsuba(b, d, debug)
    abcd = karatsuba( str(int(a)+int(b)), str(int(c)+int(d)), debug)

    adbc = str( int(abcd) - int(ac) - int(bd) )

    xy = str( (10**(2*n_2))*int(ac) + (10**n_2)*int(adbc) + int(bd) )
    
    if debug:
        print 24*"#"
        print "Product between x=%s and y=%s" % (x,y)
        print "Min number length n = %d" % (2*n_2)
        print "x = %s" % x
        print "y = %s" % y
        print "x parameterised as 10^n/2 a + b = 10^%d %s + %s " % (n_2, a, b)
        print "y parameterised as 10^n/2 c + d = 10^%d %s + %s " % (n_2, c, d)
        print "ac = %s" % ac
        print "bd = %s" % bd
        print "(a+b)(c+d) = %s" % abcd
        print "ad+bc = (a+b)(c+d) - ac - bd = %s" % adbc
        print "xy = %s" % xy

    return xy
