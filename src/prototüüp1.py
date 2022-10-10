import math
import tkinter

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
            functionName = rawinput[last:i]
            if functionName == "x":
                tokenList.append(Token("x", 0))
                tokenList.append(Token("operand", rawinput[i]))
            else:
                tokenList.append(Token("operand", rawinput[i], rawinput[last:i]))
            readerState = 0

if readerState == 1:
    tokenList.append(Token("number", float(rawinput[last:len(rawinput)])))
elif readerState == 2:
    tokenList.append(Token("x", 0))

def GetOperation(tokenList, offset, xvalue):
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
            parenthesisValue = Compute(tokenList[i + 1:closingIndex], xvalue, tokenList[i].function)
            currentOperation[j] = parenthesisValue.value
            tokenList[i] = parenthesisValue
            del tokenList[i + 1:closingIndex + 1]
            if (len(tokenList) == 1):
                break
        else:
            if tokenList[i].type == "x":
                currentOperation[j] = xvalue
            else:
                currentOperation[j] = tokenList[i].value
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

def Compute(tokenList, xvalue, rawfunction = 0):
    while len(tokenList) > 1:
        currentOperation = GetOperation(tokenList, 0, xvalue)
        if currentOperation[1] in ['*', '/']:   # Kui tehe on * või /, siis saab selle väärtuse kohe välja arvutada
            tokenList[0] = ComputeOperation(currentOperation)
            del tokenList[1:3]
        elif currentOperation[1] in ['+', '-']:
            if len(tokenList) <= 3: # Kui tehe on + või - ja see on viimane allesjäänud tehe, võib selle kohe välja arvutada
                tokenList[0] = ComputeOperation(currentOperation)
                del tokenList[1:3]
            elif GetOperation(tokenList, 2, xvalue)[1] in ['+', '-']:   # Kui + või - tehe ei ole viimane, kuid ka sellest järgmine tehe on + või -, võib kohe arvutada
                tokenList[0] = ComputeOperation(currentOperation)
                del tokenList[1:3]
            else:   # Kui + või - tehe ei ole viimane, ja sellest järgmine tehe on * või /, arvutatakse kohe välja järgmise tehte väärtus ja eelmine tehe arvutatakse välja järgmisel tsüklil, kui see siis võimalik on
                nextOperation = GetOperation(tokenList, 2, xvalue)
                tokenList[2] = ComputeOperation(nextOperation)
                del tokenList[3:5]
    
    if tokenList[0].type == "x":
        tokenList[0] = Token("number", xvalue)

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

        error = False
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
            if functionValue % 2 != 0 or tokenList[0].value >= 0:
                newvalue = tokenList[0].value ** (1/functionValue)
        elif functionName == "log":
            if tokenList[0].value > 0:
                newvalue = math.log(tokenList[0].value) / math.log(functionValue)
            else:
                error = True
        elif functionName == "ln":
            if tokenList[0].value > 0:
                newvalue = math.log(tokenList[0].value) / math.log(math.e)
            else:
                error = True
        return Token("number", newvalue, error)

master = tkinter.Tk()

canvas_width = 1000
canvas_height = 1000
w = tkinter.Canvas(master, width=canvas_width, height=canvas_height)

for x in range(0, canvas_width, 4):
    x1 = x - 4
    y1 = Compute(tokenList.copy(), x1 - canvas_width / 2)
    y2 = Compute(tokenList.copy(), x - canvas_width / 2)
    if not y1.function and not y2.function:
        w.create_line(x1, -y1.value + canvas_width - canvas_height / 2, x, -y2.value + canvas_width - canvas_height / 2)

w.pack()