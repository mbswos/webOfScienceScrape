import ast
import codecs

f = codecs.open('textfiles/oneAuth.txt', 'r')

test_dict = ast.literal_eval(f.read())
print(test_dict)