f = open('WebOfScienceCategories.txt', 'r')

categories_verify = []
categories_yes = []
categories_no = []
categories = []

for line in f.readlines():
	line = line.strip()
	category_pair = line.split(' - ')
	print(category_pair)
	word = category_pair[1]

	if word == 'Verify':
		categories_verify.append(category_pair)
	elif word == 'Yes':
		categories_yes.append(category_pair)
	else:
		categories_no.append(category_pair)

	categories.append(category_pair)

print(categories_yes)
for category in categories_verify:
	print(category[0])
print(len(categories_verify))