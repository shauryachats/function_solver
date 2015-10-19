#
#	Function Parser using Infix-Postfix method
#
#	Author : Shaurya Chats
#	shauryachats@gmail.com
#

#The operator array is to be differentiated from other characters while splitting.
	
"""TODO : Add support for custom operators, like sin() or log()"""
operators_list = ['+','-','*','/','^']

#Defines a priority order of the operators, like which operator 
#should be applied before another, like the BODMAS rule.

"""TODO : Add support for priority for custom operators"""
priority_order = {
	'^' : 3,
	'*' : 2,
	'/' : 2,
	'+'	: 1,
	'-' : 1
}

#This function splits the function string into a list
#of lexicons, that can be processed by the infix-er.

def string_split_into_lexicon( input_string ):
	lexicon_list = []
	iterating_index = 0 	
	
	lexicon_list.append('(')

	while (iterating_index < len(input_string)):
		
		character = input_string[iterating_index]

		#Checking if there is a number, we'll chomp it whole.
		if (character.isdigit()):
			temp = int(character)
			iterating_index += 1
			#Searching the next element : if it's a number, we take it in, if not, the loop exits.
			
			while (iterating_index < len(input_string) and input_string[iterating_index].isdigit()):
				temp = temp * 10 + int(input_string[iterating_index])
				iterating_index += 1

			lexicon_list.append(temp)

		#Checking for the operators
		elif character in operators_list or character in ['(',')']:
			lexicon_list.append(character)
			iterating_index += 1

		#Checking for plain characters
		elif (character.isalpha()):
			temp = character
			iterating_index += 1

			while (iterating_index < len(input_string) and input_string[iterating_index].isalpha()):
				temp += input_string[iterating_index]
				iterating_index += 1

			lexicon_list.append(temp)

	lexicon_list.append(')')

	return lexicon_list

def lexicon_list_to_postfix(lexicon_list):
	postfix_list = []
	stack = []
	for lexicon in lexicon_list:
		if lexicon not in operators_list and lexicon not in ['(',')']:
			postfix_list.append(lexicon)
		else:
			if (lexicon == '('):
				stack.append(lexicon)
			elif (lexicon == ')'):
				while (stack[-1] != '('):
					postfix_list.append(stack.pop())

				#Get rid of the '('
				stack.pop()
			
			else:
				while stack and stack[-1] != '(' and (priority_order[stack[-1]] >= priority_order[lexicon]):
					postfix_list.append(stack.pop())
				
				stack.append(lexicon)

		print postfix_list
		print stack

	return postfix_list


"""TODO : Add functionality to variables, like x and y for calculation"""

def postfix_to_value(postfix_list, variable_dict):
	value = 0
	stack = []
	for token in postfix_list:
		if  token not in operators_list:
			stack.append(token)
		else:
			value2 = stack.pop()
			value1 = stack.pop()
			
			if (not isinstance(value1, int)):
				value1 = variable_dict[value1]

			if (not isinstance(value2, int)):
				value2 = variable_dict[value2]


			if (token == '+'):
				value = value1 + value2
			elif (token == '-'):
				value = value1 - value2
			elif (token == '*'):
				value = value1 * value2
			elif (token == '/'):
				value = value1 / value2
			elif (token == '^'):
				value == value1 ** value2
			stack.append(value)
	return stack.pop()


##TEST
x = "(5+6*x)*(3*y-4)"
dicta = {
	"x" : 2,
	"y" : 3
}
print postfix_to_value(lexicon_list_to_postfix(string_split_into_lexicon(x)),dicta)

