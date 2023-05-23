import sys
import pandas as pd
from anytree import Node, RenderTree

table = pd.read_csv('SLR parsing table.csv', header=2, index_col=0)
terminal = table.columns[:22]

f = open('context_free_grammar.txt', 'r')
lines = f.readlines()
f.close()
cfg = []
for line in lines:
    cfg.append(line.strip())

f = open(sys.argv[1], 'r')
input = f.read()
f.close()
input = input.split()
input.append('$')

stack = [0]
idx = 0

root = Node("CODE")
treeNode = [root]
reduceCFG = []

def printTree():
    for grmmr in reduceCFG:
        for i in reversed(range(len(treeNode))):
            if (treeNode[i].name not in terminal and len(treeNode[i].children) == 0 and treeNode[i].name != "''"):
                parent = treeNode[i]
                # print("parent:", i, parent)
                break
        for sym in grmmr[2:]:
            child = Node(sym)
            child.parent = parent
            treeNode.append(child)
        # print("treeNode:", treeNode)
    for pre, _, node in RenderTree(root):
        if node.name == "''":
            node.name = "ε"
        print("%s%s" % (pre, node.name))


while True:
    currState = stack[-1]
    nextSymbol = input[idx]

    # print(stack, nextSymbol)

    if nextSymbol in terminal:
        # ACTION
        action = table.at[currState, nextSymbol]
        if action == 'acc':
            print("Accept!")
            printTree()
            break
        elif table.isnull().at[currState, nextSymbol]:
            line = str(sys._getframe().f_lineno - 1)
            print("Reject!")
            print("SyntaxError: invalid token set (line", line + ")")
            break

        if action[0] == 's':
            # SHIFT & goto
            stack.append(int(action[1:]))
            idx += 1
        elif action[0] == 'r':
            # REDUCTION
            g = cfg[int(action[1:])].split()
            if g[-1] != "''":
                for _ in range(len(g) - 2):
                    stack.pop()
            goto = table.at[stack[-1], g[0]]
            stack.append(int(goto))
            reduceCFG.insert(0, g)

    elif nextSymbol not in terminal:
        line = str(sys._getframe().f_lineno - 1)
        print("Reject!")
        print("InputError: invalid input token", "'" + nextSymbol + "' (line", line + ")")
        break

# print(reduceCFG)
# printTree()
