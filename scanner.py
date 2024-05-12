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
        'PARENTHESIS': r'\(|\)', # Matches '(' or ')'
        'STRING_LITERAL': r'".*"', # Matches any character, except newline, zero or more times
        'FLOAT': r'\b\d+\.\d+\b',  # Matches floats
        'INTEGER': r'\b\d+\b',  # Matches integers
    }
    
    # Initialize an empty list to store tokens
    tokens = []
    
    # Iterate through the input string
    while input_string: # if a == 0:
        match = None
        
        # Try to match each token pattern
        for token_type, pattern in token_patterns.items():
            regex = re.compile(pattern) # Compile the regular expression
            match = regex.match(input_string)
            if match:
                token_value = match.group(0)
                tokens.append((token_type, token_value)) # Append a tuple of the (token, lexeme) to the list of identfied tokens
                
                '''
                After identifying a valid token, move the index of the 'cursor' to the character
                immediately after the last character of the previously identified token.
                '''
                input_string = input_string[match.end():]
                break
        
        # If no match is found, raise an error
        if not match:
            raise Exception(f"Invalid token at position {len(input_string)}: {input_string[:10]}...")
    
    return tokens
