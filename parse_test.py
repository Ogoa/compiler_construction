from our_parser import Parser

def parse_input_string(input_string):
    """Main parsing function that orchestrates the parsing process"""
    parser = Parser(input_string)
    parse_tree = parser.parse()  # Start the parsing process and get the parse tree
    
    # Check for syntax errors
    if parser.errors:
        print("Syntax errors:")
        for error in parser.errors:
            print(error)
    else:
        print("Parsing successful. No syntax errors found.\n")
        # Print the parse tree if it exists
        if parse_tree:
            print("\nParse Tree:\n")
            parse_tree.print_parse_tree()
        else:
            print("Parse tree is non-existent")

# Test the parser with input tokens generated by the scanner
input_string = """
x = 10 + 20 * y
if x > 100:
    print("x is greater than 100")
else:
    print("x is not greater than 100")
    
"""

parse_input_string(input_string)
