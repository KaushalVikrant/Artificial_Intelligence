
myDict={"Baddi":1, "Baddi@":2 }

print myDict.keys()
print myDict.get(myDict.keys()[0])

myList=["a","b","Z"]

myList.append("p")
print myList

myList.remove("Z")
print myList


def findMaxLen(string):
    n = len(string)

    # Create a stack and push -1 as initial index to it.
    stk = []
    stk.append(-1)

    # Initialize result
    result = 0

    # Traverse all characters of given string
    for i in xrange(n):

        # If opening bracket, push index of it
        if string[i] == '(':
            stk.append(i)

        else:    # If closing bracket, i.e., str[i] = ')'

            # Pop the previous opening bracket's index
            stk.pop()

            # Check if this length formed with base of
            # current valid substring is more than max
            # so far
            if len(stk) != 0:
                result = max(result, i - stk[len(stk)-1])

            # If stack is empty. push current index as
            # base for next valid substring (if any)
            else:
                stk.append(i)

    return result
# Driver program
string = "((()()(()"
print findMaxLen(string)

string = "()(()))))"
print findMaxLen(string)