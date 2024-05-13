from scanner import lex_analyze as analyser

input_string = """
s1 = 34.9098 - 4598; float while = '23' * " ; if _9 != 230 print ('not')
"""

input_string_2 = """
if(i == 2.1):
    print("Two")
else:
    print("Not Two")
"""

tokens = analyser(input_string_2)
for i in tokens:
    print(i[0], ": ", i[1])