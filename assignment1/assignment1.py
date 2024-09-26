file = open('./example.txt')
string = file.read()
numeric = ['0','1','2','3','4','5','6','7','8','9']
token_names = ['parenthesis', 'lambda', 'var']
def tokenize_and_approve(string,level,reading_var = False):
    char = string[0]
    if char == '(':
        level += 1
        return (0, level, reading_var)
    elif char == ')':
        level -= 1
        return (0, level, reading_var)
    elif char == '\\':
        return (1, level, reading_var)
    elif char.isalpha():
        reading_var = True
        return (2, level, reading_var)
    elif char.isnumeric():
        if reading_var:
            return (2, level, reading_var)
        else:
            return False
    else:
        return False
    if level < 0:
        return False

def iterate_string(string):
    tokenization = []
    reading_var = False
    level = 0
    while len(string) > 1:
        output = tokenize_and_approve(string, level, reading_var)
        if output:
            token, level, reading_var = output 
        else:
            print('error')
        tokenization.append(token)
        string = string[1:]
        print(tokenization)
        print(level)
    if level != 0:
        print('error')
    return tokenization

tokenization = iterate_string(string)
    
