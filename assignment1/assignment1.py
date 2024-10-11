import sys
def tokenize_and_approve(expression,reading_var = False):
    #tags each character following the obvious tag, only nuance is the reading_var property,
    #that keeps track if we're already reading a variable and makes numbers acceptable
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
    elif char == '\\' or char == 'λ':
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
    #function made to iterate through the character of the string and apply the tokenization function
    tokenization = []
    reading_var = False
    while len(expression) >= 1:
        valid, value, reading_var = tokenize_and_approve(expression, reading_var)
        #we check if we found any irregularities, if we did we print their message and return False
        if not valid:
            sys.stderr.write(f'{value}\n')
            tokenization = False
            break
        #for each character we add its correspondent tokenization to the tokenization and move forward in the expression
        else:
            tokenization.append(value)
            expression = expression[1:]
    return tokenization

def lexical_analysis(tokenization, expression):
    #simply makes a list with all the tagged lexemes, identifying changes in the tagging and splitting the expression accordingly
    lexemes = []
    start_lexeme = 0
    #special case where there's a single element in the expression
    if len(tokenization) == 1:
        lexemes.append((token_names[tokenization[0]], expression[0]))
    #checks the last element and compares the tokenization to decide if a new lexeme has started or not
    else:
        for idx in range(1,len(tokenization)): 
            #if the tokenization is different than from the last expression position or if it's a parenthesis we add the last lexeme to the list
            # and update the starting position of the current lexeme
            if (tokenization[idx] != tokenization[idx-1]) or (tokenization[idx-1] in (1,2)):
                lexemes.append((token_names[tokenization[idx-1]], expression[start_lexeme:idx]))
                start_lexeme = idx
            #if we're at the last idx we add the current lexeme to the list
            if ((idx==len(tokenization)-1)):
                lexemes.append((token_names[tokenization[idx]], expression[start_lexeme:idx+1]))

    #we append an end token for convenience moving forward
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
    #our implementation of the recursive descent parsing
    tree = []
    global next_token
    #checking if it's a valid expression start
    if lexemes[next_token][0] in ['left-parenthesis', 'var', 'lambda']:
        #loop ensures the production <expr> ::= <expr><expr>
        while lexemes[next_token][0] in ['left-parenthesis', 'var', 'lambda']:
            #production expr ::= '(',<expr>,')'
            if lexemes[next_token][0] == 'left-parenthesis':
                tree.append(lexemes[next_token])
                next_token += 1
                #recursive calls expr on the next element
                tree.append(expr())
                #check if it ended by a right parenthesis
                if lexemes[next_token][0] == 'right-parenthesis':
                    tree.append(lexemes[next_token])
                    next_token += 1
                else:
                    sys.stderr.write('error: no closing parenthesis\n')
                    return False
            #checking for <expr> ::= <var>, just append the var and increase the pointer
            elif lexemes[next_token][0] == 'var':
                tree.append(lexemes[next_token])
                next_token += 1
            #checking for <expr> ::= '\'<var><expr>
            elif lexemes[next_token][0] == 'lambda':
                tree.append(lexemes[next_token])
                next_token += 1
                #checks if next token is a variable
                if lexemes[next_token][0] == 'var':
                    tree.append(lexemes[next_token])
                    next_token += 1
                    #recursively calls expr on the next element
                    tree.append(expr())
                else:
                    sys.stderr.write('error: no var after lambda\n')
                    return False
            if len(tree)>1:
                tree = [tree]
        return tree
    elif lexemes[next_token][0] == 'end':
        sys.stderr.write('invalid sequence at the end of the line\n')
        return False
    else:
        sys.stderr.write(f'error: invalid sequence at {lexemes[next_token][1]}\n')
        return False

def display_std(tree):
    #recursively builds a display the parsed tree, every time it sees a list inside the list it adds
    #parenthesis and calls the function recursively in the sublist
    string = ''
    #if the expression has only one element the remove parenthesis leaves only the tuple
    if type(tree) == tuple:
        string = tree[1]
    #in the general case we iterate through the list
    else:
        for idx in range(len(tree)):
            #if we find a list inside the list we add parenthesis and recursively display the subtree
            if type(tree[idx]) == list:
                string += '('
                string += display_std(tree[idx])
                string += ')'
            else:
                #if it's a var after another var we need to add ' ' before the var
                if tree[idx][0] == 'var':
                    if string:
                        if string[-1].isalnum():
                            string += f' {tree[idx][1]}'
                        else:
                            string += f'{tree[idx][1]}'
                    else:
                        string += f'{tree[idx][1]}'
                #if it's something else we just append it to the string
                else:
                    string += f'{tree[idx][1]}'
    return string
 
def remove_parenthesis(tree):
    #recursively removes the parenthesis and double lists so the simplified expression is as simple as possible
    #the printing function adds the necessary parenthesis in the display again
    idx = 0
    if len(tree) == 0:
        return tree
    elif len(tree)==1:
        tree = remove_parenthesis(tree[0])
    while idx < len(tree):
        if len(tree[idx])>1:
            if tree[idx][1] == '(':
                del tree[idx]
                del tree[idx+1]
                idx -= 1
        if type(tree[idx]) == list:
            tree[idx] = remove_parenthesis(tree[idx])
        idx += 1
    return tree

def check_if_valid_tree(tree):
    #it recursively checks if in some moment in the recursive parsing some problem happend
    if tree == False:
        return False
    is_valid_tree = True
    for element in tree:
        if element == False:
            is_valid_tree = False
        elif type(element) == list:
            is_valid_tree = is_valid_tree and check_if_valid_tree(element)
    return is_valid_tree

def main():        
    #open file and read it
    global lexemes
    global next_token
    global token_names
    file = False
    #error handling for opening the file
    try:
        file = open(sys.argv[1])
        expressions = file.read()
        #token names keep track of the names of each token, names are in the correct idx position
        #i.e. token -> 0 is named space as token_names[0] == 'space' 
        token_names = ['space', 'left-parenthesis', 'right-parenthesis', 'lambda', 'var']
        program_status = 0
        for expression in expressions.replace('\r\n','\n').replace('\r \n', '\n').split('\n')[:-1]:
            sys.stdout.write(f'simplified expression for "{expression}":\n')#, end='')

            #tokenize the expression
            tokenization = iterate_expression(expression)

            if tokenization != False:
                #conduct lexical analysis if tokenization went well
                lexemes = lexical_analysis(tokenization, expression)

                #apply recursive-descent parsing to get the tree
                next_token = 0
                tree = expr()

                #check if the tree is valid
                if check_if_valid_tree(tree):
                    #check if there are unparsed lexemes
                    if (lexemes[next_token][0] != 'end'):
                        sys.stderr.write(f'error: unparsed character at {lexemes[next_token][1]}\n')
                        program_status = 1
                    else:
                        #if the expression was valid we print its simplest form
                        tree = remove_parenthesis(tree)
                        sys.stdout.write(f'{display_std(tree)}\n')
                else:
                    program_status = 1
            else:
                program_status = 1
    except:
        sys.stderr.write('The code should be run with a command line argument specifying a valid file')
        program_status = 1
    #exits with 0 if all the expressions were valid and 1 otherwise
    sys.exit(program_status)

#didn't include if __name__ == '__main__' as the evaluation tool might use weird methods to run it
main()
