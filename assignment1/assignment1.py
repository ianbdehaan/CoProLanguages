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
    while len(expression) >= 1:
        valid, value, reading_var = tokenize_and_approve(expression, reading_var)
        if not valid:
            print(value)
            tokenization = False
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

def expr():
    tree = []
    global next_token
    global lexemes
    #checking for <expr> ::= (<expr>)
    if lexemes[next_token][0] in ['left-parenthesis', 'var', 'lambda']:
        while lexemes[next_token][0] in ['left-parenthesis', 'var', 'lambda']:
            if lexemes[next_token][0] == 'left-parenthesis':
                tree.append(lexemes[next_token])
                next_token += 1
                tree.append(expr())
                if lexemes[next_token][0] == 'right-parenthesis':
                    tree.append(lexemes[next_token])
                    next_token += 1
                else:
                    print('error: no closing parenthesis')
                    return False
            #checking for <expr> ::= <var>
            elif lexemes[next_token][0] == 'var':
                tree.append(lexemes[next_token])
                next_token += 1
            elif lexemes[next_token][0] == 'lambda':
                tree.append(lexemes[next_token])
                next_token += 1
                if lexemes[next_token][0] == 'var':
                    tree.append(lexemes[next_token])
                    next_token += 1
                    tree.append(expr())
                else:
                    print('error: no var after lambda')
                    return False
            if len(tree)>1:
                tree = [tree]
        return tree
    elif lexemes[next_token][0] == 'end':
        return tree
    else:
        print(f'error: invalid sequence at {lexemes[next_token][1]}')
        return False

def display_std(tree):
    string = ''
    if type(tree) == tuple:
        string = tree[1]
    else:
        for idx in range(len(tree)):
            # print(tree[idx])
            if type(tree[idx]) == list:
                string += '('
                string += display_std(tree[idx])
                string += ')'
            else:
                if tree[idx][0] == 'var':
                    if string:
                        if string[-1].isalnum():
                            string += f' {tree[idx][1]}'
                        else:
                            string += f'{tree[idx][1]}'
                    else:
                        string += f'{tree[idx][1]}'
                elif tree[idx][0] in ['left-parenthesis', 'right-parenthesis']:
                    pass
                else:
                    string += f'{tree[idx][1]}'
    return string

                
# def substitute(bound_var, subst_var, expr):
#     if len(expr) == 1:
#         if expr[0] == bound_var:
#             return [subst_var]
#         else:
#             return expr
#     result = []
#     for idx in range(len(expr)):
#         if type(expr[idx]) == list:
#             result.append(substitute(bound_var, subst_var, expr[idx]))
#         else:
#             result.append(expr[idx])
#     return result
            
def check_and_remove_parenthesis(tree):
    idx = 0
    if len(tree) == 0:
        return tree
    elif len(tree)==1:
        tree = check_and_remove_parenthesis(tree[0])
    while idx < len(tree):
        if len(tree[idx])>1:
            if tree[idx][1] == '(':
                del tree[idx]
                del tree[idx+1]
                idx -= 1
        if type(tree[idx]) == list:
            tree[idx] = check_and_remove_parenthesis(tree[idx])
        idx += 1
    return tree

# def beta_reduction(expression):
#     if len(expression) == 2:
#         expression1 = check_and_remove_parenthesis(expression[0])
#         expression2 = expression[1]
#         if expression1[0] == '(':
#             if expression1[1][0] == '\\':
#                 expression1[1] = substitute(expression1[1][1], expression2[0][0], expression1[1][2])
#                 if len(expression2)>1:
#                     expression2 = expression2[1]
#                     return beta_reduction([expression1,expression2])
#                 else:
#                     return beta_reduction(expression1)
#         else:
#             return [beta_reduction(expression[0]), beta_reduction(expression[1])]

#     elif expression[0] == '(':
#         expression = check_and_remove_parenthesis(expression)
#         result = ['(',beta_reduction(expression[1]), ')']
#         return result
#     elif expression[0] == '\\':
#         result = ['\\', expression[1], beta_reduction(check_and_remove_parenthesis(expression[2]))]
#         return result
#     else:
#         return expression
def check_if_valid_tree(tree):
    is_valid_tree = True
    for element in tree:
        if element == False:
            is_valid_tree = False
        elif type(element) == list:
            is_valid_tree = is_valid_tree and check_if_valid_tree(element)
    return is_valid_tree
        
#open file and read it
file = open('./example.txt')
expressions = file.read()
token_names = ['space', 'left-parenthesis', 'right-parenthesis', 'lambda', 'var']
for expression in expressions.replace('\r\n','\n').replace('\r \n', '\n').split('\n')[:-1]:
    print(f'simplified expression for "{expression}":')#, end='')
    # print(f'expression: {expression}')
    #tokenize the expression
    tokenization = iterate_expression(expression)
    # print(f'tokenization: {tokenization}')
    #conduct lexical analysis
    if tokenization != False:
        lexemes = lexical_analysis(tokenization, expression)
        # print(f'lexemes:\n {lexemes}\n')
        #apply recursive-descent parsing to get the tree
        next_token = 0
        tree = expr()
        if check_if_valid_tree(tree):
            # print(tree)
            tree = check_and_remove_parenthesis(tree)
            # print(tree)
            # print(f'tree:\n {tree}\n')
            # TODO apply simplification rules 
            # print(beta_reduction(tree))
            print(display_std(tree))
