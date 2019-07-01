import ast
import codecs
import os

path = 'textfiles/professors'
f = codecs.open('textfiles/oneAuth.txt', 'r')

#test_dict = ast.literal_eval(f.read())
#print(test_dict)

files = []
# r=root, d=directories, f = files
for r, d, fg in os.walk(path):
    for file in fg:
        if '.txt' in file and not file == 'Professors.txt' and not file == 'NotReadProfessors.txt':
            files.append(file)

for fs in files:
    print(fs)

def storeprofessor():
	print('hi')