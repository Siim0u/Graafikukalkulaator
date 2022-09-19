class Token:
    def __init__(self, tType, value):
        self.tokenType = tType
        self.tokenValue = value

tokenList = []
rawinput = input("Sisesta avaldis: ").strip(' ')

last = 0
for i in range(len(rawinput)):
    if (rawinput[i] in ['+', '-', '*', '/', '(', ')']):
        if i - last != 0:
            tokenList.append(Token("number", float(rawinput[last:i])))
        tokenList.append(Token("operand", rawinput[i]))
        last = i + 1

if (last != len(rawinput)):
    tokenList.append(Token("number", float(rawinput[last:len(rawinput)])))

for i in range(len(tokenList)):
    print(tokenList[i].tokenType, tokenList[i].tokenValue)
