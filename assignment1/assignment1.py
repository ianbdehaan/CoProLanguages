file = open('./example.txt')
expression = file.read()
numeric = ['0','1','2','3','4','5','6','7','8','9']
token_names = ['space', 'left-parenthesis', 'right-parenthesis', 'lambda', 'var']
def tokenize_and_approve(expression,reading_var = False):
    char = expression[0]
    if char == ' ':
        return (True, 0, reading_var)
    if char == '(':
        return (True, 1, reading_var)
    elif char == ')':
        return (True, 2, reading_var)
    elif char == '\\':
        return (True, 3, reading_var)
    elif char.isalpha():
        reading_var = True
        return (True, 4, reading_var)
    elif char.isnumeric():
        if reading_var:
            return (True, 4, reading_var)
        else:
            return (False, 'error: variable starting with numeric character', reading_var)
    else:
        return (False, f'error: invalid character found in the expression ({char})', reading_var)

def iterate_expression(expression):
    tokenization = []
    reading_var = False
    while len(expression) > 1:
        valid, value, reading_var = tokenize_and_approve(expression, reading_var)
        if not valid:
            print(value)
            break
        else:
            tokenization.append(value)
            expression = expression[1:]
    return tokenization

def lexical_analysis(tokenization, expression):
    lexemes = []
    start_lexeme = 0
    for idx in range(1,len(tokenization)): 
        if (tokenization[idx] != tokenization[idx-1]) or (tokenization[idx-1] in (1,2)):
            lexemes.append((token_names[tokenization[idx-1]], expression[start_lexeme:idx]))
            start_lexeme = idx
        if ((idx==len(tokenization)-1)):
            lexemes.append((token_names[tokenization[idx]], expression[start_lexeme:idx+1]))
    return lexemes

def expression(lexemes, idx = 0):
    print('enter <expr>')
    if lexemes[idx][0] == 'left-parenthesis':
        expression(lexemes, idx+1)
        if lexemes[idx][0] == 'right-parenthesis':
            expression(lexemes, idx+1)
    elif lexemes[idx][0] == 'var':
        if lexemes[idx+1][0] == 'var':
            expression(lexemes, idx+1)
    elif lexemes[idx][0] == 'lambda':
        if lexemes[idx+1][0] == 'var':
            expression(lexemes, idx+2)
    else:
        print('error')
    if idx != len(lexemes)-1:
        expression(lexemes,idx)

tokenization = iterate_expression(expression)
print(expression)
print(lexical_analysis(tokenization,expression))
    
