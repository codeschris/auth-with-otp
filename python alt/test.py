import random
import string

#testing the randomizing letters function test for OTP generation
def randomize():
    bets_low = string.ascii_lowercase
    bets_upper = string.ascii_uppercase
    
    num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    num_str = ''.join(num)

    #connecting lowercase and uppercase
    all = bets_low + bets_upper + num_str
    list = random.sample(all, 5)
    result = ''.join(list)
    return result

if __name__ == '__main__':
    rand_list = randomize()
    print(rand_list)