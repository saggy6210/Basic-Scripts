##Output: [9, 0, 6, 1, 5, 2, 4, 2]

def rearrangeArr(arr, n):
	arr.sort()
	tempArr = []
	i = 0
	j = n - 1
	while i < n or j > n:
		if(i >= j):
			break
		tempArr.append(arr[j])
		tempArr.append(arr[i])
		i+=1
		j-=1
		
		
	print (tempArr)
	
arr = [2, 4, 5, 1, 9, 6, 4, 0, 2]
n = len(arr)

rearrangeArr (arr, n)
