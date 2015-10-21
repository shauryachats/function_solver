#
#	Function Parser using Infix-Postfix method
#
#	Author : Shaurya Chats
#	shauryachats@gmail.com
#

import math
import sys #For sys.exit() 

#The operator array is to be differentiated from other characters while splitting.
operators_list_binary = ['+','-','*','/','^']

#The operators which take only one argument as an input - the predefined list.
operators_list_unary = ["sin","cos","tan","cosec","sec","cot","log"]


"""TODO : Add support for custom operators"""

#Defines a priority order of the operators, like which operator 
#should be applied before another, like the BODMAS rule.
priority_order = {
	'^' : 3,
	'*' : 2,
	'/' : 2,
	'+'	: 1,
	'-' : 1
}

#Setting priority for all unary operators to be 4
priority_order.update(dict((element,4) for element in operators_list_unary))

#This function splits the function string into a list
#of tokens, that can be processed by the postfix-er.
def string_to_token( input_string ):
	token_list = []
	iterating_index = 0 	
	
	token_list.append('(')

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

			#Check if  '.' is encountered, because the number will then have a decimal point
			if (input_string[iterating_index] == '.'):
				iterating_index += 1
				decimal_depth = 1
				while (	iterating_index < len(input_string) and input_string[iterating_index].isdigit()):
					temp += float(input_string[iterating_index]) / pow(10,decimal_depth)
					iterating_index += 1
					decimal_depth += 1
			
			token_list.append(temp)

		#Checking for the operators
		elif character in operators_list_binary or character in ['(',')']:
			token_list.append(character)
			iterating_index += 1

		#Checking for plain characters
		elif (character.isalpha()):
			temp = character
			iterating_index += 1

			while (iterating_index < len(input_string) 
				and input_string[iterating_index] not in ['(',')']
				and input_string[iterating_index].isalpha()):
				temp += input_string[iterating_index]
				iterating_index += 1

			token_list.append(temp)

	token_list.append(')')

	return token_list

#Converts the processed list of token into postfix form.
def token_to_postfix(token_list):
	postfix_list = []
	stack = []
	for token in token_list:
		
		if (token == '('):
			stack.append(token)

		elif (token == ')'):
			
			while (stack[-1] != '('):
				postfix_list.append(stack.pop())
			
			#Get rid of the '('
			stack.pop()
			
		elif token in operators_list_binary or token in operators_list_unary:
		
			while stack and stack[-1] != '(' and (priority_order[stack[-1]] >= priority_order[token]):
				postfix_list.append(stack.pop())
				
			stack.append(token)

		else:
			postfix_list.append(token)
		#print postfix_list
		#print stack

	print postfix_list
	return postfix_list

#Helper function to check if stack.pop() is a number or present in the variable dictionary,
#failing which would generate an error
def pop_from_stack(stack, variable_dict):
	val = stack.pop()
	try:
		val = float(val)
	except ValueError:
		try:
			val = variable_dict[val]
		except KeyError:
			print "The value of the variable",val,"is not found in the variable dictionary."
			sys.exit(1)
	return val

#Processes the postfix_list to obtain the value, after evaluating the values of the variables
#as defined in the variable_dict(ionary)
def postfix_to_value(postfix_list, variable_dict):
	value = 0
	stack = []
	for token in postfix_list:
		
		#print token
		print stack

		if  token in operators_list_binary:
			
			value2 = pop_from_stack(stack, variable_dict)
			value1 = pop_from_stack(stack, variable_dict)
			
			if (token == '+'):
				value = value1 + value2
			elif (token == '-'):
				value = value1 - value2
			elif (token == '*'):
				value = value1 * value2
			elif (token == '/'):
				value = value1 / value2
			elif (token == '^'):
				value == math.pow(value1, value2)
			
			stack.append(value)
		
		elif token in operators_list_unary:

			value = pop_from_stack(stack, variable_dict)

			if (token == "sin"):
				value = math.sin(value)
			elif (token == "cos"):
				value = math.cos(value)
			elif (token == "tan"):
				value = math.tan(value)
			elif (token == "cosec"):
				value = 1/math.sin(value)
			elif (token == "sec"):
				value = 1/math.cos(value)
			elif (token == "cot"):
				value = 1/math.tan(value)
			elif (token == "log"):
				value = math.log(value)

			stack.append(value)

		else:
			stack.append(token)
			
	return stack.pop()



