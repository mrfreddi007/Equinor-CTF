

def primecheck(numb):
    # Program to check if a number is prime or not

    # To take input from the user
    #num = int(input("Enter a number: ")
    num = int(numb)
    flag = False
    if num == 1:
        flag = True
    # prime numbers are greater than 1
    if num > 1:
        # check for factors
        for i in range(2, num):
            if (num % i) == 0:
                # if factor is found, set flag to True
                flag = True
                # break out of loop
                break
    # check if flag is True
    if flag:
        return 0
    else:
        return 1
        
# Using readlines()
file1 = open('./numbers_and_letters.txt', 'r')
Lines = file1.readlines()
flagget=""
for num in Lines:
    test = primecheck(num[:-2])
    if test:
        flagget = flagget + num[-2:-1]
flagget = flagget + "}"
        
print(flagget)