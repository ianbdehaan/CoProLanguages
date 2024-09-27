file = open('./example.txt')
string = file.read()
token_names = ['left_parent', 'right_parent', 'lambda', 'letter', 'digit', 'whitespace']

def tokenize(string):
    tokenization = []
    level = 0
    i = 0  
    while i < len(string): 
        char = string[i]
        if char == '(':
            level += 1
            tokenization.append(0)
        elif char == ')':
            level -= 1
            tokenization.append(1)
        elif char == '\\':
            tokenization.append(2)
        elif char.isalpha():
            tokenization.append(3)
        elif char.isnumeric():
            tokenization.append(4)
        elif char == ' ': 
            tokenization.append(5)
        else:
            return False
        if level < 0:
            return False
        i += 1 
    if level != 0:
        return False 
    return tokenization

tokenization = tokenize(string)
print(tokenization)

def approve(tokenization):
    if len(tokenization) == 0:
        return True
    token = token_names[tokenization[0]]
    final_token = False 
    if len(tokenization) > 1:
        next_token = token_names[tokenization[1]]
    else:
        final_token = True 
    if token == 'left_parent':
        if final_token:
            return False 
        elif next_token == 'left_parent' or next_token == 'lambda' or next_token == 'letter': 
            approve(tokenization[1:])
        else: 
            return False 
    elif token == 'right_parent':
        if final_token:
            return True 
        elif next_token == 'left_parent' or next_token == 'right_parent' or next_token == 'whitespace': 
            approve(tokenization[1:])
        else: 
            return False 
    elif token == 'lambda':
        if final_token:
            return False 
        elif next_token == 'letter': 
            approve(tokenization[1:])
        else: 
            return False 
    elif token == 'letter':
        if final_token:
            return True
        else:
            approve(tokenization[1:])
    elif token == 'digit':
        if final_token:
            return True
        else:
            approve(tokenization[1:])
    elif token == 'whitespace':
        if final_token:
            return False
        elif next_token == 'left_parent' or next_token == 'lambda' or next_token == 'letter': 
            approve(tokenization[1:])
        else:
            return False 

def iterate_tokens(tokenization):
    output = approve(tokenization)
    if output:
        return True  
    else:
        print('no correct input')
    return False 

if iterate_tokens(tokenization):
    approved_tokenization = tokenization
    print(approved_tokenization)