import collections
import heapq
import copy

def read(): #read txt file
    file = open('Input3.txt','r') #change text file name for input file
    lines = file.readlines()
    lst = []
    for line in lines:
        if line.strip().split():    
            lst.append(line.strip().split())
    return lst[0:3], lst[3:] #returns initial state and goal state.

def find(initial): #find the 0
    for y in range(len(initial)):
        for x in range(len(initial[y])):
            if initial[y][x] == "0":
                return x,y

def gather(goal): #store goal state location in a hash
    goal_coordinates = {}
    for y in range(len(goal)):
        for x in range(len(goal[y])):
            if goal[y][x] not in goal_coordinates: #store x,y coordinates in hash
                goal_coordinates[goal[y][x]] = [x,y]
    return goal_coordinates

def inbounds(x,y,initial): #check if inbound
    if 0 <= x < len(initial[0]) and 0 <= y < len(initial):
        return True
    return False

def decipher(action):
    dic = {(0,1):"Down",(0,-1):"Up",(1,0):"Right",(-1,0):"Left"}
    for i in range(len(action)):
        if action[i] in dic:
            action[i] = dic[action[i]]
    return action

def children(initial,goal_coordinates,depth,actions,f_values):
    x,y = find(initial)
    moves = [(0,1),(0,-1),(1,0),(-1,0)]
    childs = []
    for move in moves:
        newActions = copy.deepcopy(actions) #makes a copy of already happened moves
        newF_values = copy.deepcopy(f_values) #makes a copy of f values that it took to traverse
        new_x, new_y = x + move[0], y + move[1]
        if inbounds(new_x,new_y,initial):
            newActions.append(move)

            temp = copy.deepcopy(initial) #makes new board
            temp[y][x], temp[new_y][new_x] = temp[new_y][new_x],temp[y][x]
            new_manhattan = calculate(temp,goal_coordinates)

            newF_values.append(depth+new_manhattan)
            childs.append((depth+new_manhattan,temp,depth,newActions,newF_values))
    return childs

def display(board): #display board
    for i in range(len(board)):
        for k in range(len(board[i])):
            print(board[i][k], end = " ")
        print()

def move(initial,goal,goal_coordinates):
    initial_manhattan = calculate(initial,goal_coordinates)

    depth = 0
    actions = []
    f_values = [initial_manhattan]
    visited = [initial]

    heap = [(initial_manhattan,initial,depth,actions,f_values)]

    while heap:
        currHeuristic,initial,depth,actions,f_values = heapq.heappop(heap)
        depth += 1
        for child in children(initial,goal_coordinates,depth,actions,f_values):
            if child[1] not in visited:
                heapq.heappush(heap,child)
                visited.append(child[1]) #child[1] is the board
        if initial == goal:
            return actions, (len(heap)+len(visited)), f_values, initial
    print("No solutions found")
    exit()

def calculate(initial,goal_coordinates): #calculate manhattan and returns value
    manhattan_distance = []
    for i in range(len(initial)):
        column = []
        for k in range(len(initial[i])):
            if initial[i][k] in goal_coordinates:
                x,y = goal_coordinates[initial[i][k]]
                column.append((abs(x-k),abs(y-i))) #abs value or not
        manhattan_distance.append(column)
    manhattan_sum = sum([sum(sum(y) for y in x) for x in manhattan_distance])
    return manhattan_sum

def create_file(initial,actions,finished,total_nodes,f_values): #display results
    file = open("Output3.txt","w")
    for i in range(len(initial)):
        for k in range(len(initial[i])):
            file.write(initial[i][k])
            file.write(" ")
        file.write("\n")
    file.write("\n")
    for i in range(len(finished)):
        for k in range(len(finished[i])):
            file.write(finished[i][k])
            file.write(" ")
        file.write("\n")
    file.write("\n")
    file.write(str(len(actions)))
    file.write("\n")
    file.write(str(total_nodes))
    file.write("\n")
    file.write(" ".join(actions))
    file.write("\n")
    for num in f_values:
        file.write(str(num)) 
        file.write(" ")
    file.close()

def main():
    initial, goal = read()
    goal_coordinates = gather(goal)
    actions, total_nodes, f_values,finished = move(initial,goal,goal_coordinates)
    decipher(actions)
    create_file(initial,actions,finished,total_nodes,f_values)

main()
