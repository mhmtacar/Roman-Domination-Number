import matplotlib.pyplot as plt
import networkx as nx
import random
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


# This function calculates the weight of the graph.

def weight(G):
    index = 0
    sum = 0
    for node in G.nodes:
        sum += G.nodes[chr(ord("A") + index)]["Number"]
        index+=1
    return sum


# This function solves a problem through exhaustion: it goes through all possible choices until a solution is found.

def BruteForce(G):

    G2=nx.Graph()

    sum = 1000
    node_num = G.number_of_nodes()
    comb_num = 1
    count = 0
    same = 0

    rows, cols = (100000, node_num)
    arr = [[0]*cols]*rows
    rows2, cols2 = (1, node_num)
    arr2 = [0]*node_num
    control = True
    t = 0
    finish = 0

    for i in range(node_num):
        comb_num *= 3

    while finish < comb_num:
          control = True
          
          for i in range(G.number_of_nodes()):
            x = random.randint(0,2)
            arr2[i] = x
          for j in range (count):
             same = 0
             for k in range (G.number_of_nodes()):
                if arr2[k] == arr[j][k]:
                    same+=1
             if same == G.number_of_nodes():
                control = False
                break
          if control == True:
             finish += 1
             for k in range (G.number_of_nodes()):
                arr[count][k] = arr2[k]
             l = 0
             for node in G.nodes:
                G.nodes[node]["Number"] = arr[count][l]
                l+=1
             check = IsFeasible(G)
             if check == True:
                sum2 = weight(G)
                if sum2 < sum:
                    sum = sum2
                    for node in G.nodes:
                      G2.add_node(node,Number = G.nodes[node]["Number"])
                    for edge in G.edges:
                      G2.add_edge(edge[0],edge[1])
             count+=1
          
    return G2


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
G2 = nx.Graph()
Rdn = [None] * 100

count = 0
counter = 0
check = True
check2 = True

for i in range(nodeNum):
    G.add_node(chr(ord("A") + i))
    
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

G2 = BruteForce(G)

color_map = []
for node in G2.nodes:
    if G2.nodes[node]["Number"] == 0:
        color_map.append('blue')
    elif G2.nodes[node]["Number"] == 1:
        color_map.append('green') 
    else:
        color_map.append('red')


nx.draw(G2,with_labels=True,
        node_color=color_map,node_size=1000,
        font_color="white",font_size=10,font_family="Times New Roman", font_weight="bold",
        edge_color="lightgray",
        width=5)


plt.show()
