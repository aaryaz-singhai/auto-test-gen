def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def multiply(a,b):
	return a*b



def even_odd(a):
      if a%2 == 0:
            return "number is even"
      else:
            return "number is odd"
      
def subtraction(a,b):
     return a-b