class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

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

def GetOperation(tokenList, offset):
    currentOperation = [0, 0, 0]
    for j in range(3):
        print(j)
        i = j + offset
        if tokenList[i].value == '(':
            newParenthesis = 0
            closingIndex = i + 1
            while not (tokenList[closingIndex].value == ')' and newParenthesis == 0):
                if tokenList[closingIndex].value == '(':
                    newParenthesis += 1
                elif tokenList[closingIndex].value == ')':
                    newParenthesis -= 1
                closingIndex += 1
            parenthesisValue = Compute(tokenList[i + 1:closingIndex])
            currentOperation[j] = parenthesisValue.value
            tokenList[i] = parenthesisValue
            del tokenList[i + 1:closingIndex + 1]
            if (len(tokenList) == 1):
                break
        else:
            currentOperation[j] = tokenList[i].value
        print(currentOperation)
    return currentOperation

def ComputeOperation(operation):
    value = 0
    if operation[1] == '*':
        value = operation[0] * operation[2]
    elif operation[1] == '/':
        value = operation[0] / operation[2]
    elif operation[1] == '+':
        value = operation[0] + operation[2]
    elif operation[1] == '-':
        value = operation[0] - operation[2]
    return Token("number", value)

def Compute(tokenList):
    while len(tokenList) > 1:
        currentOperation = GetOperation(tokenList, 0)
        if currentOperation[1] in ['*', '/']:   # Kui tehe on * või /, siis saab selle väärtuse kohe välja arvutada
            tokenList[0] = ComputeOperation(currentOperation)
            del tokenList[1:3]
        elif currentOperation[1] in ['+', '-']:
            if len(tokenList) <= 3: # Kui tehe on + või - ja see on viimane allesjäänud tehe, võib selle kohe välja arvutada
                tokenList[0] = ComputeOperation(currentOperation)
                del tokenList[1:3]
                #for k in tokenList:
                #    print(k.value)
            elif GetOperation(tokenList, 2)[1] in ['+', '-']:   # Kui + või - tehe ei ole viimane, kuid ka sellest järgmine tehe on + või -, võib kohe arvutada
                tokenList[0] = ComputeOperation(currentOperation)
                del tokenList[1:3]
            else:   # Kui + või - tehe ei ole viimane, ja sellest järgmine tehe on * või /, arvutatakse kohe välja järgmise tehte väärtus ja eelmine tehe arvutatakse välja järgmisel tsüklil, kui see siis võimalik on
                nextOperation = GetOperation(tokenList, 2)
                tokenList[2] = ComputeOperation(nextOperation)
                del tokenList[3:5]
    return tokenList[0]

print(Compute(tokenList).value)
