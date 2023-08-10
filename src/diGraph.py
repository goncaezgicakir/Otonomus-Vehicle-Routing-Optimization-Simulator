#Author:  Gonca Ezgi Cakır
#Date:  02.05.2021
#Class:  Graduation Project II
#Project:  Kampus Ici Otonom Araclarla Ulasim Simulasyonu

#File:  diGraph.py - contains directional graph implementation for campus map

import networkx as nx

#creating directed weighted graph
graph = nx.DiGraph()


#function to implement campus map
#bus stop -> vertex
#between 2 stop -> edge
#distance between 2 stops -> weight
def implementCampusGraph():

    #Add vertices to the graph
    #All Stops------------------
    graph.add_node("s101")
    graph.add_node("s102")

    graph.add_node("s28")
    graph.add_node("s29")
    graph.add_node("s0")
    graph.add_node("s1")
    graph.add_node("s2")
    graph.add_node("s33")
    graph.add_node("s3")
    graph.add_node("s32")
    graph.add_node("s34")
    graph.add_node("s35")

    graph.add_node("s4")
    graph.add_node("s5")
    graph.add_node("s6")
    graph.add_node("s7")
    graph.add_node("s8")
    graph.add_node("s9")
    graph.add_node("s30")
    graph.add_node("s31")

    graph.add_node("s26")
    graph.add_node("s27")
    graph.add_node("s10")
    graph.add_node("s11")
    graph.add_node("s12")
    graph.add_node("s13")
    graph.add_node("s14")
    graph.add_node("s15")
    graph.add_node("s16")
    graph.add_node("s17")
    graph.add_node("s18")
    graph.add_node("s19")
    graph.add_node("s20")
    graph.add_node("s21")
    graph.add_node("s22")
    graph.add_node("s23")
    graph.add_node("s24")
    graph.add_node("s25")


    #All Distances--------------
    #area 1-------------------
    #s101(S1)
    graph.add_edge("s101", "s28", weight=80+35+110)
    graph.add_edge("s101", "s35", weight=80+228)
    #s28
    graph.add_edge("s28","s0", weight=50+280)
    graph.add_edge("s28","s4", weight=50+635+75)
    #s29
    graph.add_edge("s29","s102", weight=110+35+80)
    graph.add_edge("s29","s35", weight=110+35+228)
    #s0
    graph.add_edge("s0","s2", weight=183)
    #s1
    graph.add_edge("s1","s29", weight=280+50)

    #s2
    graph.add_edge("s2","s3", weight=30)
    graph.add_edge("s2","s5", weight=169+25)
    graph.add_edge("s2","s6", weight=169+65)
    graph.add_edge("s2","s30", weight=169+180)
    #s33
    graph.add_edge("s33","s1", weight=183)
    #s32
    graph.add_edge("s32","s33", weight=30)
    graph.add_edge("s32","s6", weight=30+169+65)
    graph.add_edge("s32","s5", weight=30+169+25)
    graph.add_edge("s32","s30", weight=30+169+180)
    #s3
    graph.add_edge("s3","s34", weight=95+284)
    #s34
    graph.add_edge("s34","s102", weight=228+80)
    #s35
    graph.add_edge("s35","s32", weight=284+95)
    graph.add_edge("s35","s101", weight=284+68+150)
    

    #area2----------------------
    #s6
    graph.add_edge("s6","s8",weight=105+135)
    graph.add_edge("s6","s9",weight=105+301+45)
    graph.add_edge("s6","s7",weight=105+301+183+115)
    #s7
    graph.add_edge("s7","s5",weight=65+25)
    graph.add_edge("s7","s30",weight=65+180)
    #s4
    graph.add_edge("s4","s6",weight=25+65)
    graph.add_edge("s4","s30",weight=25+180)
    graph.add_edge("s4","s3", weight=25+169+30)
    graph.add_edge("s4","s33",weight=25+169)
    #s5
    graph.add_edge("s5","s29",weight=75+635+50)
    #s30
    graph.add_edge("s30","s26",weight=150+30)
    graph.add_edge("s30","s25",weight=150+110)
    #s31
    graph.add_edge("s31","s3",weight=180+169+30)
    graph.add_edge("s31","s5",weight=180+25)
    graph.add_edge("s31","s6",weight=180+65)
    graph.add_edge("s31","s33",weight=180+169)

    #area3---------------------
    #s26
    graph.add_edge("s26","s10",weight=235)
    #s27
    graph.add_edge("s27","s31",weight=30+150)
    graph.add_edge("s27","s25",weight=30+110)
    #s10
    graph.add_edge("s10","s12",weight=110)
    #s11
    graph.add_edge("s11","s27",weight=235)
    #s12
    graph.add_edge("s12","s14", weight=418+119)
    graph.add_edge("s12","s16", weight=418+95+120)
    graph.add_edge("s12","s20", weight=418+95+481)
    graph.add_edge("s12","s18", weight=418+271+67)
    #s13
    graph.add_edge("s13","s11",weight=110)
    #s14
    graph.add_edge("s14","s20",weight=118+481)
    graph.add_edge("s14","s16",weight=118+120)
    #s15
    graph.add_edge("s15","s18",weight=119+271+67)
    graph.add_edge("s15","s13",weight=119+418)
    #s16
    graph.add_edge("s16","s18",weight=50+67)
    #s17
    graph.add_edge("s17","s20", weight=120+481)
    graph.add_edge("s17","s15",weight=120+118)
    graph.add_edge("s17","s13",weight=120+95+418)
    #s18
    graph.add_edge("s18","s23", weight=180+215)
    graph.add_edge("s18","s24",weight=180+85)
    #s19
    
    graph.add_edge("s19","s17",weight=67+50)
    graph.add_edge("s19","s13", weight=67+271+418)
    graph.add_edge("s19","s14",weight=67+271+119)
    #s25
    graph.add_edge("s25","s19",weight=85+180)
    graph.add_edge("s25","s23",weight=85+215)
    #s24
    graph.add_edge("s24","s31",weight=110+150)
    graph.add_edge("s24","s26",weight=110+30)
    #s22
    graph.add_edge("s22","s24",weight=215+85)
    graph.add_edge("s22","s19",weight=215+180)
    #s23
    graph.add_edge("s23","s21",weight=367)
    #s20
    graph.add_edge("s20","s22",weight=267)
    #s21
    graph.add_edge("s21","s13",weight=481+95+418)
    graph.add_edge("s21","s15",weight=481+118)
    graph.add_edge("s21","s16", weight=481+120)

    return graph


#function to print graphs
def printGraph():

    nx.draw(graph,with_labels=True)
    plt.draw()
    plt.show()
