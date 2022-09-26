class Token:
    def __init__(self, tType, value):
        self.tokenType = tType
        self.tokenValue = value

tokenList = []
readerState = 0
last = 0
rawinput = input("Sisesta avaldis: ").strip(' ')

for i in range(len(rawinput)):
    if rawinput[i] >= '0' and rawinput[i] <= '9' and readerState == 0:
        last = i
        readerState = 1
    elif rawinput[i] in ['+', '-', '*', '/', '(', ')']:
        if readerState == 1:
            tokenList.append(Token("number", float(rawinput[last:i])))
            readerState = 0
        tokenList.append(Token("operand", rawinput[i]))

if readerState == 1:
    tokenList.append(Token("number", float(rawinput[last:len(rawinput)])))

for i in range(len(tokenList)):
    print(tokenList[i].tokenType, tokenList[i].tokenValue)

def Compute(tokenList):
    i = 0
    while i != len(tokenList):
        if tokenList[i].tokenValue == '(':
            j = 0
            while tokenList[i + j].tokenValue != ')':
                print(i, j)
                print(tokenList[i + j].tokenValue)
                j += 1
            tokenList[i] = Compute(tokenList[i + 1:i + j - 1])
            del tokenList[i + 1:i + j + 1]
            i = 0
        else:
            i += 1
    return Token("number", 0)

Compute(tokenList)
print("\n")
for i in range(len(tokenList)):
    print(tokenList[i].tokenType, tokenList[i].tokenValue)
