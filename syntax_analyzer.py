import sys
import pandas as pd
from anytree import Node, RenderTree

# SLR_parsing_table.csv을 불러와서 'table'에 저장
table = pd.read_csv('SLR_parsing_table.csv', header=2, index_col=0)
# terminal을 'terminal' 리스트에 저장
terminal = list(table.columns[:22])
terminal.append("''")

# context free grammar를 'cfg' 리스트에 저장
cfg = []
f = open('context_free_grammar.txt', 'r')
lines = f.readlines()
f.close()
for line in lines:
    cfg.append(line.strip())

# input 파일을 불러와서 토큰 단위로 'input' 리스트에 저장
f = open(sys.argv[1], 'r')
input = f.read()
f.close()
input = input.split()
input.append('$')

# parse tree의 root 노드 생성
root = Node("CODE")
treeNode = [root]
# reduce할 때 사용된 cfg rule을 저장할 리스트
reduceRule = []

# parse tree 출력 함수
def printTree():
    sys.stdout = open('output.txt', 'w', encoding='utf-8')
    print("Accept!")
    for rule in reduceRule:
        # parent node 구하기
        for i in reversed(range(len(treeNode))):
            if (treeNode[i].name not in terminal and len(treeNode[i].children) == 0):
                parentNode = treeNode[i]
                break
        # child node 생성 및 parent node 지정
        for symbol in rule[2:]:
            childNode = Node(symbol, parent=parentNode)
            treeNode.append(childNode)

    # parse tree 출력
    for pre, _, node in RenderTree(root):
        if node.name == "''":
            node.name = "ε"
        print("%s%s" % (pre, node.name))
    sys.stdout.close()


# 초기 설정
stack = [0]
idx = 0

# SLR parsing 구현
while True:
    # current state = top of stack
    currState = stack[-1]
    # next input symbol = 'input' 리스트의 'idx'번째 인덱스
    nextSymbol = input[idx]

    # 유효한 input token인지를 확인
    if nextSymbol in terminal:
        # ACTION table
        action = table.at[currState, nextSymbol]

        # accept인 경우
        if action == 'acc':
            printTree()
            break
        # reject인 경우
        elif table.isnull().at[currState, nextSymbol]:
            sys.stdout = open('output.txt', 'w', encoding='utf-8')
            print("Reject!")
            print("SyntaxError: invalid token set")
            sys.stdout.close()
            break

        # shift & goto
        if action[0] == 's':
            stack.append(int(action[1:]))
            idx += 1
        # reduce
        elif action[0] == 'r':
            rule = cfg[int(action[1:])].split()
            if rule[-1] != "''":
                for _ in range(len(rule) - 2):
                    stack.pop()
            goto = table.at[stack[-1], rule[0]]
            stack.append(int(goto))
            reduceRule.insert(0, rule)

    # 유효하지 않은 input token에 대한 예외처리
    elif nextSymbol not in terminal:
        sys.stdout = open('output.txt', 'w', encoding='utf-8')
        print("Reject!")
        print("InputError: invalid input token", "'" + nextSymbol + "'")
        sys.stdout.close()
        break
