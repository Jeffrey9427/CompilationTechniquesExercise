import pandas as pd
import re
from anytree import Node, RenderTree

class TreeNode:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self, level=0):
        ret = " " * (level * 2) + f"{self.symbol}\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

def first(s, productions): 
    if not s:
        return set()
    
    c = s[0]
    ans = set()
    
    # check if c is a non-terminal
    if c.isupper():
        for st in productions[c]:
            if st == 'e':
                # if length is 1 and it is epsilon, add epsilon to the first set
                if len(s) == 1:
                    ans.add('e')
                    
                # if there are more, recursively call first(s[1:]) to get the first set of the rest of the string
                else: 
                    ans = ans.union(first(s[1:], productions))
                    
            else:
                # recursively call first(st) to get the first set of the production
                f = first(st, productions)
                ans = ans.union(f)
    else: 
        # if c is a terminal, add c to the first set
        ans = ans.union(c)
        
    return ans
    
def follow(s, productions, ans):
    # key: non-terminal, value: each production rule for that non-terminal
    if s not in productions:
        return ans  # if s is a terminal, no need to process further
        
    for key in productions:
        for value in productions[key]:
            f = value.find(s)
            if f != -1:
                # if s in the last position of the production rule, add follow(key) to follow(s)
                if f == len(value) - 1:
                    if key != s:
                        if key in ans:
                            temp = ans[key]
                        else:
                            ans = follow(key, productions, ans)
                            temp = ans[key]
                        ans[s] = ans[s].union(temp)
                else:
                    # if s is followed by a non-terminal, add first of that non-terminal to follow(s)
                    first_of_next = first(value[f+1:], productions)
                    # if epsilon is in the first set, recursively call follow(key) and add to follow(s)
                    if 'e' in first_of_next:
                        if key != s:
                            # if key already in ans, use that, otherwise recursively call follow(key)
                            if key in ans:
                                temp = ans[key]
                            else:
                                ans = follow(key, productions, ans)
                                temp = ans[key]
                                
                            # remove epsilon from the first set, union with follow(key) and add to follow(s)
                            ans[s] = ans[s].union(temp)
                            ans[s] = ans[s].union(first_of_next - {'e'})

                    else: 
                        # if no epsilon in the first set, union with first of next and add to follow(s)
                        ans[s] = ans[s].union(first_of_next)
                        
    return ans
            
def ll1(follow, productions):
    print("\nParsing Table\n")
    
    table = {}

    # key: non-terminal, value: each production rule for that non-terminal
    for key in productions:
        for value in productions[key]:
            # if the production rule is not epsilon ('@')
            if value != 'e':
                # get the first set of the production rule
                f = first(value, productions)
                for x in f:
                    # if x is not epsilon, add the production rule to the parsing table
                    if x != 'e':
                        table[(key, x)] = value
                    else:
                        # if x is epsilon, add follow(key) to the parsing table
                        for y in follow[key]:
                            table[(key, y)] = value
            else:
                # if the production rule is epsilon, add follow(key) to the parsing table
                for y in follow[key]:
                    table[(key, y)] = value
                    
    # print the parsing table in key-value format
    for key, val in table.items():
        print(key, "=>", val)
        
    new_table = {}
    
    for pair in table:
        if pair[0] not in new_table:
            new_table[pair[0]] = {}
        new_table[pair[0]][pair[1]] = table[pair]
        
    print("\nParsing Table\n")
    print(pd.DataFrame(new_table).fillna(''))
    print("\n")
    
    return table

def parse(user_input, start_symbol, parsingTable):
    # flag to check if string is accepted or not
    flag = 0
    node_stack = [Node(start_symbol)]

    # appending dollar to end of input
    user_input = user_input + "$"

    stack = []
    stack.append("$")
    stack.append(start_symbol)

    input_len = len(user_input)
    index = 0
    
    root = node_stack[-1]

    # continue until stack is empty
    while len(stack) > 0:

        # element at top of stack
        top = stack[len(stack)-1]
        print("\nStack =>", stack)
        print("Top =>", top)

        # current input
        current_input = user_input[index]
        print("Current_Input => ", current_input)

        # if top of stack is same as current input
        if top == current_input:
            # pop from stack
            stack.pop()
            index = index + 1    
        else:    
            # create key with the top of the stack and current input symbol
            key = top, current_input
            print("Key =>", key)

            # top of stack terminal => not accepted
            if key not in parsingTable:
                flag = 1        
                break

            # retrieve production rule for the key from parsing table
            value = parsingTable[key]
            parent_node = node_stack.pop()
            stack.pop()

            for element in reversed(value):
                if element != 'e':
                    stack.append(element)
                    new_node = Node(element, parent=parent_node)
                    node_stack.append(new_node)


    if flag == 0 and current_input == "$":
        print("String accepted!")
    else:
        print("There is error in parsing the string!")
        print("String not accepted!")

    print("\nParse Tree:")
    for pre, fill, node in RenderTree(root):
        # You can also print the type of node (non-terminal or terminal) for better clarity
        print(f"{pre}{node.name} ({'Non-terminal' if node.name.isupper() else 'Terminal'})")

  
if __name__ == "__main__":
    # initialize dictionaries to store grammar productions, FIRST, and FOLLOW sets
    productions = dict()
    file = input("Enter the grammar file name: ")
    grammar = open(file, "r") 
    first_dict = dict()  
    follow_dict = dict() 
    
    string = input("Enter the string to parse: ")

    # flag to identify the starting symbol of the grammar
    flag = 1
    start = ""  # to store the start symbol

    # read and parse each line of the grammar file
    for line in grammar:
        line = line.strip()  # strip leading/trailing whitespace
        if '->' in line:
            lhs, rhs = line.split('->')
            lhs = lhs.strip()  # clean up LHS
            rhs = rhs.strip()  # clean up RHS
            
            rhs = rhs.replace('ε', 'e')
            rhs = rhs.replace(" ", "")
            
            # set the starting symbol from the first line of the grammar
            if flag:
                flag = 0
                start = lhs
                
            # split RHS by '|' and remove any empty productions
            rhs_productions = set([prod.strip() for prod in rhs.split('|') if prod.strip()])
            
            # store the productions in the dictionary
            if lhs in productions:
                productions[lhs].update(rhs_productions)  # add new RHS to existing RHS set
            else:
                productions[lhs] = rhs_productions

    # calculate FIRST sets for each non-terminal and print them
    print('\nFirst\n')
    for lhs in productions:
        first_dict[lhs] = first(lhs, productions)
    for f in first_dict:
        print(str(f) + " : " + str(first_dict[f]))
    print("")

    # initialize FOLLOW sets and print them
    print('\nFollow\n')
    for lhs in productions:
        follow_dict[lhs] = set()  # initialize FOLLOW set for each non-terminal

    # add '$' to FOLLOW set of the start symbol
    follow_dict[start] = follow_dict[start].union('$')

    # calculate FOLLOW sets for each non-terminal using `follow` function
    for lhs in productions:
        follow_dict = follow(lhs, productions, follow_dict)
    # re-run FOLLOW function to ensure all FOLLOW sets are correctly populated
    for lhs in productions:
        follow_dict = follow(lhs, productions, follow_dict)

    # print each FOLLOW set
    for f in follow_dict:
        print(str(f) + " : " + str(follow_dict[f]))

    # generate the LL(1) parsing table using FIRST and FOLLOW sets
    ll1Table = ll1(follow_dict, productions)
    
    parse(string, start, ll1Table)