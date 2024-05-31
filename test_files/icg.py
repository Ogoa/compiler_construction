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

    def generate_ir(self):
        if self.name == "program":
            ir_code = []
            for child in self.children:
                ir_code.extend(child.generate_ir())
            return ir_code
        elif self.name == "statement_list":
            ir_code = []
            for child in self.children:
                ir_code.extend(child.generate_ir())
            return ir_code
        elif self.name == "assignment_statement":
            identifier = self.children[0].value
            expression_ir = self.children[2].generate_ir()
            ir_code = expression_ir + [f"STORE {identifier}"]
            return ir_code
        elif self.name == "conditional_statement":
            condition_ir = self.children[0].generate_ir()
            if_block_ir = self.children[1].generate_ir()
            if len(self.children) == 3:  # else block present
                else_block_ir = self.children[2].generate_ir()
                ir_code = condition_ir + [f"JUMP_IF_FALSE else_label"] + if_block_ir + [f"JUMP end_label", "else_label:"] + else_block_ir + ["end_label:"]
            else:
                ir_code = condition_ir + [f"JUMP_IF_FALSE end_label"] + if_block_ir + ["end_label:"]
            return ir_code
        elif self.name == "logical_expression":
            left_ir = self.children[0].generate_ir()
            operator = self.children[1].value
            right_ir = self.children[2].generate_ir()
            ir_code = left_ir + right_ir + [f"{operator}"]
            return ir_code
        elif self.name == "expression":
            return self.children[0].generate_ir()
        elif self.name == "term":
            if self.children[0].name in ["integer", "float", "identifier"]:
                return [f"PUSH {self.children[0].value}"]
            elif self.children[0].name == "string_literal":
                return [f"PUSH \"{self.children[0].value}\""]
        elif self.name == "block":
            return self.children[0].generate_ir()
        elif self.name == "loop_statement":
            condition_ir = self.children[0].generate_ir()
            block_ir = self.children[1].generate_ir()
            ir_code = ["loop_label:"] + condition_ir + [f"JUMP_IF_FALSE end_loop_label"] + block_ir + [f"JUMP loop_label", "end_loop_label:"]
            return ir_code
        return []
