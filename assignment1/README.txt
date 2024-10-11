Group:  40
Names:  Ian de Haan 
        Angela van Delft 

The program is working correctly for all the inputs we tried 
Deviations of the assignment:
-The program does not support a dot (.) after the lambda abstraction as we used our available time to prioritize the other aspects of the assignment.

Program summary: 
First the program opens a file especified as a command line argument and reads expressions from it. 
Then it loops trough all the expressions. 
For each expression if first gets tokenized, checking for any weird characters or variable names starting with a number. 
Then if the tokenization doesn't encounter errors, the lexical analysis is performed on the tokenization for that expression and a list with lexemes is obtained. 
Then a parse tree is made using recursive descent parsing on the list with the lexemes, checking for parsing errors. 
If the parsing is successful and complete, the code simplifies the tree and writes in stdout the unambiguous version of the expression with the least ammount of spaces and parenthesis.
After all the expressions are analyzed, if any errors are encountered during the execution, a comprehensive error message is display in stderr and the program exits with code 1, else it exits with code 0 
