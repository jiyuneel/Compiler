import sys
import pandas as pd

table = pd.read_csv('SLR parsing table.csv', header=2, index_col=0)
terminal = table.columns[:22]
# nonterminal = table.columns[22:]

f = open('CFG.txt', 'r')
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
print(input)

stack = [0]
idx = 0

while True:
    currState = stack[-1]
    nextSymbol = input[idx]

    # print(stack)
    # print(nextSymbol)

    if nextSymbol in terminal:
        # ACTION
        action = table.at[currState, nextSymbol]
        if action == 'acc':
            print('accept!')
            break
        elif table.isnull().at[currState, nextSymbol]:
            print('reject')
            break

        if action[0] == 's':
            # SHIFT & goto
            stack.append(int(action[1:]))
            idx += 1
        elif action[0] == 'r':
            # REDUCTION
            g = cfg[int(action[1:])].split()
            for _ in range(len(g) - 2):
                stack.pop()
            
            currState = stack[-1]
            goto = table.at[currState, g[0]]
            stack.append(int(goto))

        # else reject

    # elif nextSymbol in nonterminal:
        # reject
