import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import tkinter as tk
from tkinter import simpledialog

# This function checks that there are undefended provinces with respect to the problem or not.

def IsFeasible(G):
    x = 0
    y = 0
    z = 0
    for node in G.nodes:
        if G.nodes[node]["Number"] == 0:
            y = 0
            x = x+1
            neighbor_list = [n for n in G.neighbors(node)]
            for neighbor in neighbor_list:
                z+=1
                num = G.nodes[neighbor]["Number"]
                if num == 2:
                    y = y+1
            if y == 0 and z > 0:
                break
            z = 0

    if x == 0:
         return True
    else:
        if y == 0 and z > 0:
            return False
        else:
            return True


#  This function produces an initial feasible solution X∗ by applying random changes to
#  elements of the zero vector X.

def InitialSolution(G):
    
    while (True):
        y = random.randint(1,2)
        y2 = random.randint(0,G.number_of_nodes()-1)
        a = chr(ord("A") + y2)
        G.nodes[a]["Number"] = y
        control = IsFeasible(G)
        if control == True:
            break

    for node in G.nodes:
        if G.nodes[node]["Number"] > 0:
            G.nodes[node]["Number"] -= 1
            control2 = IsFeasible(G)
            if control2 == False:
                G.nodes[node]["Number"] += 1


# This function randomly chooses an element of the solution X with positive value and decreases its value by one. If the
# resulting vector is again a feasible solution, it stores it as the new best solution
# and repeats the process until an infeasible solution is found.

def DecreasingProcedure(X,X2):
    
    while True:
                y = random.randint(0,X2.number_of_nodes()-1)
                a = chr(ord("A") + y)
                
                if X2.nodes[a]["Number"] > 0:
                    X2.nodes[a]["Number"] -= 1
                    control = IsFeasible(X2)
                    if control == False:
                        break
                    else:
                        for node in X2.nodes:
                            X.nodes[node]["Number"] = X2.nodes[node]["Number"]


def AssignGraph(X):
    X2=nx.Graph()
    for node in X.nodes:
        X2.add_node(node,Number = X.nodes[node]["Number"])
    
    for edge in X.edges:
        X2.add_edge(edge[0],edge[1])

    return X2


def Shake(X,k):

    X2=nx.Graph()
    
    for node in X.nodes:
        X2.add_node(node,Number = X.nodes[node]["Number"])
    
    for edge in X.edges:
        X2.add_edge(edge[0],edge[1])

    DecreasingProcedure(X,X2)

    for j in range (k):
        while True:
            y = random.randint(0,X2.number_of_nodes()-1)
            a = chr(ord("A") + y)
            if X2.nodes[a]["Number"] < 2:
                break
            
        while True:
            y = random.randint(0,X2.number_of_nodes()-1)
            b = chr(ord("A") + y)
            if X2.nodes[b]["Number"] > 0:
                break
            
        X2.nodes[a]["Number"] += 1
        X2.nodes[b]["Number"] -= 1
    
    control = IsFeasible(X2)
    if control == True: 
        for node in X2.nodes:
            X.nodes[node]["Number"] = X2.nodes[node]["Number"]
        DecreasingProcedure(X,X2)
    
    return X2

# This function calculates the number of undefended provinces with respect to the problem.

def penalty(X):
 y = 0
 undefended = 0
 for node in X.nodes:
    if X.nodes[node]["Number"] == 0:
        y = 0
        neighbor_list = [n for n in X.neighbors(node)]
        for neighbor in neighbor_list:
            num = X.nodes[neighbor]["Number"]
            if num == 2:
               y = y+1
        if y == 0:
            undefended+=1
 return undefended


def LocalSearch2(X):
    ndmin = penalty(X)
    X2 = nx.Graph()
    X3 = nx.Graph()
    X4 = nx.Graph()
    X5 = nx.Graph()
    control = False
    control2 = False
    check = False
    p = 0.5
    count = 0

    while count == 0:
     control = False
     control2 = False
     for i in range(X.number_of_nodes()):
        if X.nodes[chr(ord("A") + i)]["Number"] == 2:
            X.nodes[chr(ord("A") + i)]["Number"] -=2
            for j in range(X.number_of_nodes()):
                if X.nodes[chr(ord("A") + j)]["Number"] < 2:
                    X.nodes[chr(ord("A") + j)]["Number"] += 1
                    check = IsFeasible(X)
                    if check == True:
                        for node in X.nodes:
                                X2.add_node(node,Number = X.nodes[node]["Number"])
                            
                        for edge in X.edges:
                                X2.add_edge(edge[0],edge[1])
                        
                        DecreasingProcedure(X,X2)
                        ndmin = penalty(X2)
                        continue
                    else:
                        for k in range(X.number_of_nodes()):
                         if X.nodes[chr(ord("A") + k)]["Number"] <2:
                            X.nodes[chr(ord("A") + k)]["Number"] += 1
                            check = IsFeasible(X)
                            if check == True:
                                for node in X.nodes:
                                        X2.add_node(node,Number = X.nodes[node]["Number"])
                                    
                                for edge in X.edges:
                                        X2.add_edge(edge[0],edge[1])
                                
                                DecreasingProcedure(X,X2)
                                ndmin = penalty(X2)
                                continue

                            else:
                                nd = penalty(X)
                                if nd < ndmin:
                                    for node in X.nodes:
                                        X3.add_node(node,Number = X.nodes[node]["Number"])
                                    
                                    for edge in X.edges:
                                        X3.add_edge(edge[0],edge[1])
                                    ndmin = nd
                                    control = True
                                if nd == ndmin:
                                    num = 1/p
                                    randNum = random.randint(1,num)
                                    if randNum == num:
                                        for node in X.nodes:
                                            X4.add_node(node,Number = X.nodes[node]["Number"])
                                        
                                        for edge in X.edges:
                                            X4.add_edge(edge[0],edge[1])
                                        control2 = True
                            X.nodes[chr(ord("A") + k)]["Number"] -= 1
                X.nodes[chr(ord("A") + j)]["Number"] -=1
            X.nodes[chr(ord("A") + i)]["Number"] +=2

     if control == True:
            for node in X3.nodes:
                X.add_node(node,Number = X3.nodes[node]["Number"])
            
            for edge in X3.edges:
                X.add_edge(edge[0],edge[1])
     else:
            count+=1
            if control2 == True:
                for node in X4.nodes:
                    X.add_node(node,Number = X4.nodes[node]["Number"])
                
                for edge in X4.edges:
                    X.add_edge(edge[0],edge[1])
            else:
                break
    
    for node in X2.nodes:
        X5.add_node(node,Number = X2.nodes[node]["Number"])
    
    for edge in X2.edges:
        X5.add_edge(edge[0],edge[1])
    return X5


def LocalSearch(X):
    
    ndmin = penalty(X)
    X2 = nx.Graph()
    X3 = nx.Graph()
    X4 = nx.Graph()
    X5 = nx.Graph()
    control = False
    control2 = False
    p = 0.5
    count = 0

    while count == 0:
     control = False
     control2 = False
     for i in range(X.number_of_nodes()):
        if X.nodes[chr(ord("A") + i)]["Number"] > 0:
            X.nodes[chr(ord("A") + i)]["Number"] -=1
            check = IsFeasible(X)
            if check == True:
               for node in X.nodes:
                    X2.add_node(node,Number = X.nodes[node]["Number"])
                
               for edge in X.edges:
                    X2.add_edge(edge[0],edge[1])
               
               DecreasingProcedure(X,X2)
               ndmin = penalty(X2)
               continue
            else:
                for j in range(X.number_of_nodes()):
                   if j != i and X.nodes[chr(ord("A") + j)]["Number"] <2:
                     X.nodes[chr(ord("A") + j)]["Number"] += 1
                     nd = penalty(X)
                     if nd == 0:
                        for node in X.nodes:
                            X2.add_node(node,Number = X.nodes[node]["Number"])
                        
                        for edge in X.edges:
                            X2.add_edge(edge[0],edge[1])
                        DecreasingProcedure(X,X2)
                        ndmin = penalty(X2)
                        continue
                     else:
                        if nd < ndmin:
                           for node in X.nodes:
                             X3.add_node(node,Number = X.nodes[node]["Number"])
                        
                           for edge in X.edges:
                             X3.add_edge(edge[0],edge[1])
                           ndmin = nd
                           control = True
                        if nd == ndmin:
                            num = 1/p
                            randomNum = random.randint(1,num)
                            if randomNum == num:
                                for node in X.nodes:
                                    X4.add_node(node,Number = X.nodes[node]["Number"])
                                
                                for edge in X.edges:
                                    X4.add_edge(edge[0],edge[1])
                                control2 = True
                     X.nodes[chr(ord("A") + j)]["Number"] -= 1
            X.nodes[chr(ord("A") + i)]["Number"] +=1

     if control == True:
            for node in X3.nodes:
                X.add_node(node,Number = X3.nodes[node]["Number"])
            
            for edge in X3.edges:
                X.add_edge(edge[0],edge[1])
     else:
            count+=1
            if control2 == True:
                for node in X4.nodes:
                    X.add_node(node,Number = X4.nodes[node]["Number"])
                
                for edge in X4.edges:
                    X.add_edge(edge[0],edge[1])
            else:
                X2 = LocalSearch2(X)
    
    for node in X2.nodes:
        X5.add_node(node,Number = X2.nodes[node]["Number"])
    
    for edge in X2.edges:
        X5.add_edge(edge[0],edge[1])
    return X5
   

# This function calculates the weight of the graph.

def weight(G):
    sum = 0
    for node in G.nodes:
           sum += G.nodes[node]["Number"]
    return sum


ROOT = tk.Tk()

ROOT.withdraw()

while(True):
 nodeNum = simpledialog.askstring(title="Test",
                                  prompt="Enter vertex number:")
 if nodeNum.isdigit():
    nodeNum = int(nodeNum)
    maxEdgeNum = (nodeNum * nodeNum-1)/2
    break

while(True):
 edgeNum = simpledialog.askstring(title="Test",
                                  prompt="Enter edge number:")

 if edgeNum.isdigit():
    edgeNum = int(edgeNum)
    if edgeNum <= maxEdgeNum:
       break


G = nx.Graph()
G2=nx.Graph()
G3=nx.Graph()
X = nx.Graph()

max_time = 0
kmin = 1
kmax = 30
kstep = 1
tmax = 1
k = 0
p = 0.5
count = 0
check = True
check2 = True


for i in range(nodeNum):
    G.add_node(chr(ord("A") + i),Number = 0)
    
for j in range(edgeNum):
    while True:
     num1 = random.randint(0,nodeNum-1)
     ch1 = chr(ord("A") + num1)
     num2 = random.randint(0,nodeNum-1)
     ch2 = chr(ord("A") + num2)

     if ch1 != ch2:
        for edge in G.edges:
            if ch1 != edge[0] or ch2 != edge[1]:
               if ch1 != edge[1] or ch2 != edge[0]:
                  check2 = True
               else:
                  check2 = False
                  break
            else:
                check2 = False
                break
        if check2 == True:
            G.add_edge(ch1,ch2)
            break
        check2 = True


start_time = time.time()
InitialSolution(G)
sum = weight(G)
 
while k <= kmax and max_time<=7200:

    k = kmin
    
    while k <= kmax:
            G2 = nx.Graph()
            for node in G.nodes:
                G2.add_node(node,Number = G.nodes[node]["Number"])
            
            for edge in G.edges:
                G2.add_edge(edge[0],edge[1])

            X = Shake(G2,k)
            Y = LocalSearch(X)
            check = IsFeasible(Y)
            sum2 = weight(Y)
            
            if sum2 < sum and check == True:
                    sum = sum2
                    for node2 in Y.nodes:
                        G.add_node(node,Number = Y.nodes[node2]["Number"])
                    for edge in Y.edges:
                        G.add_edge(edge[0],edge[1])
                    k = kmin
            else:
                count+=1
                k += kstep
    max_time = time.time() - start_time


color_map = []
for node in G.nodes:
    if G.nodes[node]["Number"] == 0:
        color_map.append('blue')
    elif G.nodes[node]["Number"] == 1:
        color_map.append('green') 
    else:
        color_map.append('red')

nx.draw(G,with_labels=True,
        node_color=color_map,node_size=1000,
        font_color="white",font_size=10,font_family="Times New Roman", font_weight="bold",
        edge_color="lightgray",
        width=5)


plt.show()




