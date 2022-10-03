import math

class Token:
    def __init__(self, type, value, function = 0):
        self.type = type
        self.value = value
        self.function = function

tokenList = []
readerState = 0
last = 0
rawinput = input("Sisesta avaldis: ").strip(' ')

for i in range(len(rawinput)):
    if rawinput[i] >= '0' and rawinput[i] <= '9' and readerState == 0:
        last = i
        readerState = 1
    elif rawinput[i] >= 'a' and rawinput[i] <= 'z' and readerState == 0:
        last = i
        readerState = 2
    elif rawinput[i] in ['+', '-', '*', '/', '(', ')']:
        if readerState == 1:
            tokenList.append(Token("number", float(rawinput[last:i])))
            readerState = 0
        if readerState < 2:
            tokenList.append(Token("operand", rawinput[i]))
        else:
            tokenList.append(Token("operand", rawinput[i], rawinput[last:i]))
            readerState = 0

if readerState == 1:
    tokenList.append(Token("number", float(rawinput[last:len(rawinput)])))

for i in tokenList:
    print(i.type, i.value, i.function)

def GetOperation(tokenList, offset):
    currentOperation = [0, 0, 0]
    for j in range(3):
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
            parenthesisValue = Compute(tokenList[i + 1:closingIndex], tokenList[i].function)
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

def Compute(tokenList, rawfunction = 0):
    while len(tokenList) > 1:
        currentOperation = GetOperation(tokenList, 0)
        if currentOperation[1] in ['*', '/']:   # Kui tehe on * või /, siis saab selle väärtuse kohe välja arvutada
            tokenList[0] = ComputeOperation(currentOperation)
            del tokenList[1:3]
        elif currentOperation[1] in ['+', '-']:
            if len(tokenList) <= 3: # Kui tehe on + või - ja see on viimane allesjäänud tehe, võib selle kohe välja arvutada
                tokenList[0] = ComputeOperation(currentOperation)
                del tokenList[1:3]
            elif GetOperation(tokenList, 2)[1] in ['+', '-']:   # Kui + või - tehe ei ole viimane, kuid ka sellest järgmine tehe on + või -, võib kohe arvutada
                tokenList[0] = ComputeOperation(currentOperation)
                del tokenList[1:3]
            else:   # Kui + või - tehe ei ole viimane, ja sellest järgmine tehe on * või /, arvutatakse kohe välja järgmise tehte väärtus ja eelmine tehe arvutatakse välja järgmisel tsüklil, kui see siis võimalik on
                nextOperation = GetOperation(tokenList, 2)
                tokenList[2] = ComputeOperation(nextOperation)
                del tokenList[3:5]

    if rawfunction == 0:
        return tokenList[0]
    else:
        i = 0
        while i < len(rawfunction):
            if rawfunction[i] < 'a':
                break
            i += 1
        functionName = rawfunction[0:i]
        functionValue = 0
        if i != len(rawfunction):
            functionValue = float(rawfunction[i:len(rawfunction)])
            
        newvalue = 0
        if functionName == "sin":
            newvalue = math.sin(tokenList[0].value)
        elif functionName == "cos":
            newvalue = math.cos(tokenList[0].value)
        elif functionName == "tan":
            newvalue = math.tan(tokenList[0].value)
        elif functionName == "pow":
            newvalue = tokenList[0].value ** functionValue
        elif functionName == "rt":
            newvalue = tokenList[0].value ** (1/functionValue)
        elif functionName == "log":
            newvalue = math.log(tokenList[0].value) / math.log(functionValue)
        elif functionName == "ln":
            newvalue = math.log(tokenList[0].value) / math.log(math.e)
        return Token("number", newvalue)

print(Compute(tokenList).value)
