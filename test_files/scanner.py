import re

def lex_analyze(input_string):
  # Define regular expressions for tokens
    token_patterns = {
        'INDENT': r'\n(?=\t)',
        'NEWLINE': '\n',
        'WHITESPACE': r'\s+',
        'ARITHMETIC_OPERATOR': r'[+\-*\/%]',
        'CONDITIONAL_KEYWORD': r'if|else|elif',
        'LOOP_KEYWORD': r'for|while',
        'KEYWORD': r'print|in',
        'LOGICAL_OPERATOR': r'!=|==|>=|<=|>|<|or|and|not',
        'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'COLON': r':',
        'ASSIGNMENT_OPERATOR': r'=',
        'OPENING_PARENTHESIS': r'\(',
        'CLOSING_PARENTHESIS': r'\)',
        'STRING_LITERAL': r'".*"', # Matches any character, except newline, zero or more times
        'FLOAT': r'\b\d+\.\d+\b',  # Matches floats
        'INTEGER': r'\b\d+\b',  # Matches integers
    }
    
    # Initialize an empty list to store tokens
    tokens = []

    # Initialize an empty list to store error messages
    lexical_errors = []
    
    # Iterate through the input string
    while input_string:  # if a == 0:
        match_found = False  # Flag to show whether a valid token has been detected or not

        # Try to match each token pattern
        for token_type, pattern in token_patterns.items():
            regex = re.compile(pattern)  # Compile the regular expression
            match = regex.match(input_string)
            if match:
                token_value = match.group(0)
                tokens.append((token_type, token_value))  # Append a tuple of the (token, lexeme) to the list of identified tokens
                input_string = input_string[match.end():]  # Move the index of the 'cursor' to the character immediately after the last character of the previously identified token
                match_found = True
                break

        # If no match is found, add an error message to the list of lexical errors
        if not match_found:
            # Find the end of the lexeme until the next whitespace or newline
            end_index = min(input_string.find(' '), input_string.find('\n')) if ' ' in input_string or '\n' in input_string else len(input_string)
            lexeme = input_string[:end_index] if end_index != -1 else input_string
            lexical_errors.append(("Invalid token", f"{lexeme}"))
            input_string = input_string[end_index:] if end_index != -1 else ''

    # Return tokens if no lexical errors occurred, otherwise return error messages
    return lexical_errors if lexical_errors else tokens
