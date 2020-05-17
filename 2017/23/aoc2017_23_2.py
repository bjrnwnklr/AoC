import math

b = 109_900
c = 126_900

def is_prime(n):
    for i in range(2,int(math.sqrt(n))+1):
        if (n % i) == 0:
            return False
    return True


count = sum(not is_prime(n) for n in range(b, c+1, 17))

print(count)  

# part 2: 913 (the count of non-prime numbers in 
# range(109_900, 126_900, 17)