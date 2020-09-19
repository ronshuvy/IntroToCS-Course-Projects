
#############################################################
# Username : ronshuvy
# Full Name : Ron Shuvy
# ID : 206330193
#############################################################

import math

def golden_ratio():
    """ Prints the golden ratio """ 
    print((1 + math.sqrt(5))/2)

def six_squared():
    """ Prints the result of six squared """ 
    print(6**2) # Also can be implemented with math.pow(6,2)

def hypotenuse():
    """ Prints the hypotenuse of a right triangle with legs equals to 5 and 12."""
    print(math.sqrt(5**2 + 12**2))

def pi():
   """ Prints the mathemetical constant Pi"""
   print(math.pi)

def e():
    """ Prints the mathemetical constant e"""
    print(math.e)

def squares_area():
    """ Prints the area of squares with sides 1-10 """
    for i in range(1,10):
        print(i**2, end =" ")
    print (10**2) # Technical constraint becuase of presubmit test (no space at the end)

if __name__ == "__main__" :

    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()

