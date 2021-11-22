# To print all non prime numbers upto the provided count

def isPrime(i):
	if  i == 1:
		return False
	for num in range(2, i):
		if i%num == 0:
			return False
	return True

if __name__ == "__main__":
	num = int(input("Enter a number: "))
	i = 1;
	count = 0
	while count < num:
		if not isPrime(i):
			print(i, end=" ")
			count = count + 1
		i = i + 1
