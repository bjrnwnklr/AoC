import re

op_precedence = {
    '+': 2,
    '*': 1,
    '(': 3,
    ')': 3
}


def eval_rpn(e):
    stack = []
    while e:
        term = e.pop(0)
        if term in ['*', '+']:
            # operator, so take the last two arguments off of the stack, evaluate the expression
            # and push the result to the stack
            stack.append(eval(str.format('{}{}{}', stack.pop(), term, stack.pop())))
        else:
            stack.append(term)
    return stack[-1]


def shunting_yard(expression):
    output_queue = []
    operator_stack = []
    while expression:
        term = expression.pop(0)
        if term.isnumeric():
            output_queue.append(int(term))
        elif term in ['*', '+']:
            while (operator_stack
                   and op_precedence[operator_stack[-1]] >= op_precedence[term]
                   and operator_stack[-1] != '('
            ):
                output_queue.append(operator_stack.pop())
            operator_stack.append(term)
        elif term == '(':
            operator_stack.append(term)
        elif term == ')':
            while operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack[-1] == '(':
                operator_stack.pop()

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue


f_name = 'ex1.txt'
# f_name = 'input.txt'

with open(f_name, 'r') as f:
    expressions = [list(re.sub(r'\s', '', l.strip('\n'))) for l in f.readlines()]

for e in expressions:
    # print(e)
    rpn_expression = shunting_yard(e)
    # print(rpn_expression)
    print(eval_rpn(rpn_expression))

# part1 = sum(evaluate_expression(e) for e in expressions)
# print(f'Part 1: {part1}')


# Part 1: 86311597203806
# Part 2: 276894767062189
