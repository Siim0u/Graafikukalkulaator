import math, tkinter
from tkinter import ttk
from tkinter import font

class Token:
    def __init__(self, type, value, function = 0):
        self.type = type
        self.value = value
        self.function = function

class EntryDesc:
    def __init__(self, tempText):
      self.tempText = tempText
      self.tempTextActive = True

canvas_width = 800
canvas_height = 800
CANVAS_OFFSET = 2

widgets = []

master = tkinter.Tk()
master.geometry(f"{canvas_width + 50 + CANVAS_OFFSET}x{canvas_height + 140 + CANVAS_OFFSET}")
graphWindow = tkinter.Canvas(master, width=canvas_width + CANVAS_OFFSET, height=canvas_height + CANVAS_OFFSET)
master.title("Graafik")
graphWindow.place(x=40, y=0)

UI_START_X = 40
UI_START_Y = 880

x_start = tkinter.ttk.Entry(master)
widgets.append([x_start, EntryDesc("X-telje algus")])
x_start.place(x=UI_START_X + 20, y=UI_START_Y, width=75)
x_start.insert(0, "X-telje algus")
x_start.config(foreground = 'grey')
x_end = tkinter.ttk.Entry(master)
widgets.append([x_end, EntryDesc("X-telje lõpp")])
x_end.insert(0, "X-telje lõpp")
x_end.config(foreground = 'grey')
x_end.place(x=UI_START_X + 100, y=UI_START_Y, width=75)

y_start = tkinter.ttk.Entry(master)
widgets.append([y_start, EntryDesc("Y-telje algus")])
y_start.insert(0, "Y-telje algus")
y_start.config(foreground = 'grey')
y_start.place(x=UI_START_X + 20, y=UI_START_Y + 30, width=75)
y_end = tkinter.ttk.Entry(master)
widgets.append([y_end, EntryDesc("Y-telje lõpp")])
y_end.insert(0, "Y-telje lõpp")
y_end.config(foreground = 'grey')
y_end.place(x=UI_START_X + 100, y=UI_START_Y + 30, width=75)

tkinter.Label(master, text="X:").place(x=UI_START_X, y=UI_START_Y)
tkinter.Label(master, text="Y:").place(x=UI_START_X, y=UI_START_Y + 30)
tkinter.Label(master, text="f(x) =").place(x=UI_START_X + 180, y=UI_START_Y)

entry = tkinter.ttk.Entry(master)
widgets.append([entry, EntryDesc("Funktsiooni avaldis")])
entry.insert(0, "Funktsiooni avaldis")
entry.config(foreground = 'grey')
entry.place(x=UI_START_X + 220, y=UI_START_Y, width=150)

functionValueLabel = tkinter.Label(master, text="f(x) =")
functionValueLabel.place(x=40, y=canvas_height + 50)
functionValueEntry = tkinter.ttk.Entry(master)
functionValueEntry.place(x=50 + tkinter.font.nametofont("TkDefaultFont").measure("f(x) ="), y=canvas_height + 50, width=100)

xLabels = []
yLabels = []

for x in range(int(canvas_width / 100) + 1):
    xLabels.append(tkinter.Label(master, text='0'))
    xLabels[x].place(x=x * 100 + 20, y=canvas_height+20)

for y in range(int(canvas_height / 100) + 1):
    yLabels.append(tkinter.Label(master, text='0'))
    yLabels[y].place(x=0, y=y * 100)

def OnEntryClick(event):
    widget = event.widget
    for i in widgets:
        if i[0] == widget and i[1].tempTextActive:
            widget.delete(0, "end")
            widget.insert(0, '') 
            widget.config(foreground = 'black')
            i[1].tempTextActive = False
            return
        
def OnEntryFocusOut(event):
    widget = event.widget
    for i in widgets:
        if i[0] == widget and widget.get() == '':
            widget.insert(0, i[1].tempText)
            widget.config(foreground = 'grey')
            i[1].tempTextActive = True
            return

def OnMouseMove(event, xstart, xChangePerPixel, tokenList):
    x = xstart + xChangePerPixel * event.x
    functionLabelText = f"f({str(round(x, 3))}) ="
    functionValueLabel.config(text=functionLabelText)
    functionValueEntry.delete(0, "end")
    y, error = Compute(tokenList.copy(), x)
    functionValueEntry.insert(0, "Defineerimata" if error else str(y))
    functionValueEntry.place(x=50 + tkinter.font.nametofont("TkDefaultFont").measure(functionLabelText))

x_start.bind("<FocusIn>", OnEntryClick)
x_start.bind("<FocusOut>", OnEntryFocusOut)
x_end.bind("<FocusIn>", OnEntryClick)
x_end.bind("<FocusOut>", OnEntryFocusOut)
y_start.bind("<FocusIn>", OnEntryClick)
y_start.bind("<FocusOut>", OnEntryFocusOut)
y_end.bind("<FocusIn>", OnEntryClick)
y_end.bind("<FocusOut>", OnEntryFocusOut)
entry.bind("<FocusIn>", OnEntryClick)
entry.bind("<FocusOut>", OnEntryFocusOut)

def CreateGraph():
    tokenList = []
    readerState = 0
    last = 0
    rawinput = entry.get()
    for i in range(len(rawinput)):
        if rawinput[i] >= '0' and rawinput[i] <= '9' and (readerState & 3) == 0:
            last = i
            readerState |= 1
        elif rawinput[i] >= 'a' and rawinput[i] <= 'z' and (readerState & 3) == 0:
            last = i
            readerState |= 2
        elif rawinput[i] in ['+', '-', '*', '/', '(', ')']:
            if (readerState & 4) != 0 and rawinput[i] == '-':
                last = i
                readerState |= 1
                readerState &= ~4
            else:
                if (readerState & 1) != 0:
                    tokenList.append(Token("number", float(rawinput[last:i])))
                    readerState &= ~1
                if (readerState & 2) == 0:
                    tokenList.append(Token("operand", rawinput[i]))
                else:
                    functionName = rawinput[last:i]
                    if functionName == "x":
                        tokenList.append(Token("x", 0))
                        tokenList.append(Token("operand", rawinput[i]))
                    else:
                        tokenList.append(Token("operand", rawinput[i], rawinput[last:i]))
                    readerState &= ~2
            
        if rawinput[i] == '(':
            readerState |= 4
        elif (readerState & 4) != 0:
            readerState &= ~4

    if (readerState & 1) != 0:
        tokenList.append(Token("number", float(rawinput[last:len(rawinput)])))
    elif (readerState & 2) != 0:
        tokenList.append(Token("x", 0))
    
    xstart = float(x_start.get())
    ystart = float(y_start.get())
    xend = float(x_end.get())
    yend = float(y_end.get())
    xChangePerPixel = (abs(xend - xstart)) / canvas_width
    yChangePerPixel = (abs(yend - ystart)) / canvas_height
    
    yRatio = yend / abs(yend - ystart)
    yoffset = canvas_height * yRatio

    graphWindow.delete("all")
    graphWindow.bind("<Motion>", lambda event:OnMouseMove(event, xstart, xChangePerPixel, tokenList.copy()))
    
    for x in range(int(canvas_width / 100) + 1):
        xLabels[x].config(text=str(round(xstart + xChangePerPixel * x * 100, 3)))
        graphWindow.create_line(x * 100 + CANVAS_OFFSET, 0, x * 100 + CANVAS_OFFSET, canvas_height + CANVAS_OFFSET, fill="lightgray")
    
    for y in range(int(canvas_height / 100) + 1):
        yLabels[y].config(text=str(round(yend + yChangePerPixel * -y * 100, 3)))
        graphWindow.create_line(0, y * 100 + CANVAS_OFFSET, canvas_width + CANVAS_OFFSET, y * 100 + CANVAS_OFFSET, fill="lightgray")
    
    y2, error2 = Compute(tokenList.copy(), xstart)
    for x in range(canvas_width):
        y1 = y2
        error1 = error2
        y2, error2 = Compute(tokenList.copy(), xstart + xChangePerPixel * (x + 1))
        if not (error1 or error2):
            graphWindow.create_line(x + CANVAS_OFFSET, -(y1 / yChangePerPixel) + yoffset + CANVAS_OFFSET, x + 1 + CANVAS_OFFSET, -(y2 / yChangePerPixel) + yoffset + CANVAS_OFFSET)
         
start = tkinter.ttk.Button(master, text="Loo graafik", command=CreateGraph)
start.place(x=UI_START_X + 400, y=UI_START_Y, width=75, height=50)

def GetOperation(tokenList, offset, xvalue, globalError):
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
            error = False
            tokenVal, error = Compute(tokenList[i + 1:closingIndex], xvalue, tokenList[i].function, globalError)
            if error:
                globalError = True
            parenthesisValue = Token("number", tokenVal)
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
    return currentOperation, globalError

def ComputeOperation(operation, globalError):
    value = 0
    if operation[1] == '*':
        value = operation[0] * operation[2]
    elif operation[1] == '/':
        if operation[2] != 0:
            value = operation[0] / operation[2]
        else:
            return Token("number", 0)
    elif operation[1] == '+':
        value = operation[0] + operation[2]
    elif operation[1] == '-':
        value = operation[0] - operation[2]
    return Token("number", value)

def Compute(tokenList, xvalue, rawfunction = 0, globalError = False):
    while len(tokenList) > 1:
        currentOperation, globalError = GetOperation(tokenList, 0, xvalue, globalError)
        # Kui tehe on * või /, siis saab selle väärtuse kohe välja arvutada
        if currentOperation[1] in ['*', '/']:
            tokenList[0] = ComputeOperation(currentOperation, globalError)
            del tokenList[1:3]
        elif currentOperation[1] in ['+', '-']:
            # Kui tehe on + või - ja see on viimane allesjäänud tehe, võib selle kohe välja arvutada
            if len(tokenList) <= 3:
                tokenList[0] = ComputeOperation(currentOperation, globalError)
                del tokenList[1:3]
            # Kui + või - tehe ei ole viimane, kuid ka sellest järgmine tehe on + või -, võib kohe arvutada
            elif GetOperation(tokenList, 2, xvalue, globalError)[1] in ['+', '-']:
                tokenList[0] = ComputeOperation(currentOperation, globalError)
                del tokenList[1:3]
            # Kui + või - tehe ei ole viimane, ja sellest järgmine tehe on * või /, arvutatakse kohe välja järgmise tehte väärtus ja eelmine tehe arvutatakse välja järgmisel tsüklil, kui see on siis võimalik
            else:
                nextOperation, globalError = GetOperation(tokenList, 2, xvalue, globalError)
                tokenList[2] = ComputeOperation(nextOperation, globalError)
                del tokenList[3:5]
    
    if tokenList[0].type == "x":
        tokenList[0] = Token("number", xvalue)

    if rawfunction == 0:
        return tokenList[0].value, globalError
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
            if tokenList[0].value > 0:
                newvalue = tokenList[0].value ** (1/functionValue)
            elif tokenList[0].value < 0:
                globalError = True
        elif functionName == "log":
            if tokenList[0].value > 0:
                newvalue = math.log(tokenList[0].value, 10 if functionValue == 0 else functionValue)
            else:
                globalError = True
        elif functionName == "ln":
            if tokenList[0].value > 0:
                newvalue = math.log(tokenList[0].value, math.e)
            else:
                globalError = True
        return newvalue, globalError