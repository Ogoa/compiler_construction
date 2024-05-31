from scanner import lex_analyze
class Node:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        
    def print_tree(self, depth=0):
        indent = "  " * depth
        print(f"{indent}{self.name}: {self.value}")
        for child in self.children:
            child.print_tree(depth + 1)

class Parser:
    def __init__(self, input_string):
        self.tokens = lex_analyze(input_string)
        self.current_token = None
        self.index = 0
        self.errors = []

    def parse(self):
        self.consume_token()
        parse_tree = self.program()
        if not self.errors:
            return parse_tree
        else:
            return self.errors

    def consume_token(self):
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
        else:
            self.current_token = None

    def program(self):
        program_node = Node("program")
        statement_list_node = self.statement_list()
        if statement_list_node:
            program_node.add_child(statement_list_node)
        else:
            self.errors.append(f"Expected a statement_list, found {self.current_token[0] if self.current_token else 'end of input'}")
        return program_node

    def statement_list(self):
        statement_list_node = Node("statement_list")
        while self.current_token:
            statement_node = self.statement()
            if statement_node:
                statement_list_node.add_child(statement_node)
            else:
                break
        return statement_list_node

    def statement(self):
        statement_node = None
        self.skip_whitespace()
        if self.match_token('IDENTIFIER'):
            statement_node = self.assignment_statement()
        elif self.match_token('CONDITIONAL_KEYWORD'):
            statement_node = self.conditional_statement()
        elif self.match_token('LOOP_KEYWORD'):
            statement_node = self.loop_statement()
        else:
            self.errors.append(f"Expected a statement type, found {self.current_token[0]}: {self.current_token[1]}")
            self.consume_token()  # Advance token index if no statement matches
        self.skip_newline()  # Consume newline after each statement
        return statement_node

    def skip_whitespace(self):
        while self.match_token('WHITESPACE'):
            self.consume_token()

    def skip_newline(self):
        while self.match_token('NEWLINE'):
            self.consume_token()

    def assignment_statement(self):
        assignment_node = None
        if self.match_token('IDENTIFIER'):
            identifier_node = Node("identifier", self.current_token[1])
            self.consume_token()
            self.skip_whitespace()
            self.expect_token('ASSIGNMENT_OPERATOR')
            assignment_operator_node = Node("assignment_operator", self.current_token[1])
            self.consume_token()
            self.skip_whitespace()
            expression_node = self.expression()
            if expression_node:
                assignment_node = Node("assignment_statement")
                assignment_node.add_child(identifier_node)
                assignment_node.add_child(assignment_operator_node)
                assignment_node.add_child(expression_node)
            else:
                self.errors.append(f"Expected an expression, found {self.current_token[0]}: {self.current_token[1]}")
        else:
            self.errors.append(f"Expected an identifier, found {self.current_token[0]}: {self.current_token[1]}")
        return assignment_node

    def conditional_statement(self):
        conditional_node = None
        if self.match_token('CONDITIONAL_KEYWORD') and self.current_token[1] == 'if':
            conditional_node = Node("conditional_statement", self.current_token[1])
            self.consume_token()
            self.skip_whitespace()
            self.expect_token('OPENING_PARENTHESIS')
            self.consume_token()
            self.skip_whitespace()
            logical_expression_node = self.logical_expression()
            self.skip_whitespace()
            self.expect_token('CLOSING_PARENTHESIS')
            self.consume_token()
            self.skip_whitespace()
            if logical_expression_node:
                conditional_node.add_child(logical_expression_node)
                self.skip_whitespace()
                self.expect_token('COLON')
                self.consume_token()
                self.skip_whitespace()
                block_node = self.block()
                if block_node:
                    conditional_node.add_child(block_node)
                    self.skip_whitespace()
                    if self.match_token('CONDITIONAL_KEYWORD') and self.current_token[1] == 'else':
                        else_node = Node("conditional_statement", self.current_token[1])
                        self.consume_token()
                        self.skip_whitespace()
                        self.expect_token('COLON')
                        self.consume_token()
                        self.skip_whitespace()
                        else_block_node = self.block()
                        if else_block_node:
                            else_node.add_child(else_block_node)
                            conditional_node.add_child(else_node)
                        else:
                            self.errors.append(f"Expected a block, found {self.current_token[0]}: {self.current_token[1]}")
                else:
                    self.errors.append(f"Expected a block, found {self.current_token[0]}: {self.current_token[1]}")
            else:
                self.errors.append(f"Expected a logical expression, found {self.current_token[0]}: {self.current_token[1]}")
        else:
            self.errors.append(f"Expected 'if', found {self.current_token[0]}: {self.current_token[1]}")
        return conditional_node

    def loop_statement(self):
        loop_node = None
        if self.match_token('LOOP_KEYWORD'):
            loop_node = Node("loop_statement", self.current_token[1])
            self.consume_token()
            self.skip_whitespace()
            logical_expression_node = self.logical_expression()
            if logical_expression_node:
                loop_node.add_child(logical_expression_node)
                self.skip_whitespace()
                self.expect_token('COLON')
                self.consume_token()
                self.skip_whitespace()
                block_node = self.block()
                if block_node:
                    loop_node.add_child(block_node)
                else:
                    self.errors.append(f"Expected a block, found {self.current_token[0]}: {self.current_token[1]}")
            else:
                self.errors.append(f"Expected a logical expression, found {self.current_token[0]}: {self.current_token[1]}")
        else:
            self.errors.append(f"Expected a loop keyword, found {self.current_token[0]}: {self.current_token[1]}")
        return loop_node

    def block(self):
        block_node = Node("block")
        while self.current_token and (self.match_token('IDENTIFIER') or self.match_token('KEYWORD') or self.match_token('CONDITIONAL_KEYWORD') or self.match_token('LOOP_KEYWORD')):
            statement_node = self.statement()
            if statement_node:
                block_node.add_child(statement_node)
            else:
                break
        return block_node

    def expression(self):
        expression_node = None
        term_node = self.term()
        if term_node:
            expression_node = Node("expression")
            expression_node.add_child(term_node)
            while self.match_token('ARITHMETIC_OPERATOR'):
                operator_node = Node("arithmetic_operator", self.current_token[1])
                self.consume_token()
                self.skip_whitespace()
                term_node = self.term()
                if term_node:
                    expression_node.add_child(operator_node)
                    expression_node.add_child(term_node)
                else:
                    self.errors.append(f"Expected a term, found {self.current_token[0]}: {self.current_token[1]}")
                    break
        else:
            self.errors.append(f"Expected a term, found {self.current_token[0]}: {self.current_token[1]}")
        return expression_node

    def logical_expression(self):
        logical_expression_node = None
        term_node = self.term()
        if term_node:
            logical_expression_node = Node("logical_expression")
            logical_expression_node.add_child(term_node)
            while self.match_token('LOGICAL_OPERATOR'):
                operator_node = Node("logical_operator", self.current_token[1])
                self.consume_token()
                self.skip_whitespace()
                term_node = self.term()
                if term_node:
                    logical_expression_node.add_child(operator_node)
                    logical_expression_node.add_child(term_node)
                else:
                    self.errors.append(f"Expected a term, found {self.current_token[0]}: {self.current_token[1]}")
                    break
        else:
            self.errors.append(f"Expected a term, found {self.current_token[0]}: {self.current_token[1]}")
        return logical_expression_node

    def term(self):
        term_node = None
        if self.match_token('INTEGER'):
            term_node = Node("integer", self.current_token[1])
            self.consume_token()
        elif self.match_token('FLOAT'):
            term_node = Node("float", self.current_token[1])
            self.consume_token()
        elif self.match_token('IDENTIFIER'):
            term_node = Node("identifier", self.current_token[1])
            self.consume_token()
        elif self.match_token('STRING_LITERAL'):
            term_node = Node("string_literal", self.current_token[1])
            self.consume_token()
        elif self.match_token('OPENING_PARENTHESIS'):
            self.consume_token()
            term_node = self.expression()
            self.skip_whitespace()
            self.expect_token('CLOSING_PARENTHESIS')
        else:
            self.errors.append(f"Expected a term, found {self.current_token[0]}: {self.current_token[1]}")
        return term_node

    def newline(self):
        if self.match_token('NEWLINE'):
            self.consume_token()

    def match_token(self, token_type):
        return self.current_token and self.current_token[0] == token_type

    def expect_token(self, token_type):
        if not self.match_token(token_type):
            self.errors.append(f"Expected {token_type}, found {self.current_token[0] if self.current_token else 'end of input'}")
        self.consume_token()

# Test function to validate the parser
def test_parser(input_string):
    parser = Parser(input_string)
    parse_tree = parser.parse()
    if isinstance(parse_tree, Node):
        print("Parse tree:")
        parse_tree.print_tree()
    else:
        print("Errors encountered during parsing:")
        for error in parse_tree:
            print(error)

# Example usage
input_string1 = """x = 10
if (x>5):
    print("small")
else:
    print("large")
"""

input_string2 = "x = 10"

input_string3 = "x = 10 if x > 5:print('small') else:print('large')"

print("Testing input_string1:")
test_parser(input_string1)
print("\nTesting input_string2:")
test_parser(input_string2)
print("\nTesting input_string3:")
test_parser(input_string3)
