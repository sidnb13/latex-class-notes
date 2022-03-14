import math

def gcf(a,b):
    greatest = min(a,b)
    while True:
        if a % greatest == 0 and b % greatest == 0:
            return greatest
        greatest -= 1
        
def prime_factorization(n):
    # generate a sieve
    sieve = [True] * (n + 1)
    for i in range(2,math.ceil(math.sqrt(n))):
        if sieve[i] == True:
            for j in range(i**2,n + 1,i):
                sieve[j] = False
    prime_list = []
    for i,b in enumerate(sieve):
        if b: prime_list.append(i)
    prime_list = prime_list[2:]
        
    factor_dict = {}
    
    while n != 1:
        for p in prime_list:
            exp_count = 0
            while n % p == 0:
                n /= p
                print(n)
                exp_count += 1
            if exp_count > 0:
                factor_dict[p] = exp_count
    return factor_dict