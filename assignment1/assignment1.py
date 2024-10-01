def tokenize_and_approve(expression,reading_var = False):
    char = expression[0]
    if char == ' ':
        reading_var = False
        return (True, 0, reading_var)
    if char == '(':
        reading_var = False
        return (True, 1, reading_var)
    elif char == ')':
        reading_var = False
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
    lexemes.append(('end', ''))
    #removing spaces as they're not necessary moving forward
    lexeme_idx = 0
    while lexeme_idx < len(lexemes):
        if lexemes[lexeme_idx][0] == 'space':
            del lexemes[lexeme_idx]
        else:
            lexeme_idx += 1

    return lexemes

def expr(trace = False):
    if trace: print('enter <expr>')
    tree = []
    global next_token
    global lexemes
    #checking for <expr> ::= (<expr>)
    if lexemes[next_token][0] == 'left-parenthesis':
        tree.append(lexemes[next_token])
        next_token += 1
        if trace: print(f'next token is {lexemes[next_token][0]} next lexeme is {lexemes[next_token][1]}')
        #if trace: print('<expr>::= (<expr>)')
        tree.append(expr())
        if lexemes[next_token][0] == 'right-parenthesis':
            tree.append(lexemes[next_token])
            next_token += 1
            if trace: print(f'next token is {lexemes[next_token][0]} next lexeme is {lexemes[next_token][1]}')
        else:
            if trace: print('error')
    #checking for <expr> ::= <var>
    elif lexemes[next_token][0] == 'var':
        tree.append(lexemes[next_token])
        if trace: print('enter <var>\nexit<var>')
        next_token += 1
        if trace: print(f'next token is {lexemes[next_token][0]} next lexeme is {lexemes[next_token][1]}')
    #checking for <expr> ::= \ <var> <expr>
    elif lexemes[next_token][0] == 'lambda':
        tree.append(lexemes[next_token])
        next_token += 1
        if trace: print(f'next token is {lexemes[next_token][0]} next lexeme is {lexemes[next_token][1]}')
        if lexemes[next_token][0] == 'var':
            tree.append(lexemes[next_token])
            if trace: print("enter <var>\nexit <var>")
            next_token += 1
            if trace: print(f'next token is {lexemes[next_token][0]} next lexeme is {lexemes[next_token][1]}')
            tree.append(expr())
        else:
            if trace: print('error')
    #catching wrong productions
    elif lexemes[next_token][0] != 'end':
        if trace: print('error')
    
    #checking for <expr> ::= <expr><expr>
    if lexemes[next_token][0] in ['left-parenthesis', 'var', 'lambda']:
        tree = [tree]
        tree.append(expr())
    if trace: print('exit <expr>')
    return tree

file = open('./example.txt')
expression = file.read()
print(f'expression: {expression}')
numeric = ['0','1','2','3','4','5','6','7','8','9']
token_names = ['space', 'left-parenthesis', 'right-parenthesis', 'lambda', 'var']
tokenization = iterate_expression(expression)
print(f'tokenization: {tokenization}')
lexemes = lexical_analysis(tokenization, expression)
print(f'lexemes:\n {lexemes}\n')
next_token = 0
trace = False
if trace: print(f'next token is {lexemes[next_token][0]} next lexeme is {lexemes[next_token][1]}')
print(f'tree:\n {expr()}')

    
