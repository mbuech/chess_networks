import time
from collections import deque
import networkx as nx 
import matplotlib.pyplot as plt
import sys
import os

# Add this app to the path so imports work as expected
APP_PATH = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(APP_PATH)

from lib.chess import *


if __name__ == "__main__":
    file_pgn = open('data/Kasparov.pgn')
    game = Game()
    game.import_pgn(file_pgn)
    moves = [x.split(".")[-1] for x in game.movetext.split(" ")]
    last_index = moves.index('')
    q = deque(moves[0:last_index])
    count = 0
    winner = None
    if game.tags['Result'] == '1-0':
        winner = WHITE
    elif game.tags['Result'] == '0-1':
        winner = BLACK
    fout = open('network_data.tsv', 'w')
    headers = ['move', 'side', 'strongly_connected_components',\
     'weakly_connected_components', 'average_shortest_path_length',\
     'winner?']
    for head in headers:
        fout.write(head + '\t')
    fout.write('\n')    
    while q:
        move = q.popleft()
        game.board.move(move)
        count += 1
        #WHITE=0, BLACK=1
        for side in (WHITE, BLACK):
            G = nx.DiGraph()
            for i in game.board.occupied_squares(side):
                for ranks in RANKS:
                    for files in FILES:
                        file_rank = (files + ranks).lower()
                        if i.can_potentialy_attack(game.board, Coord.from_notation(file_rank)) == True:
                            from_node_position = str(i.position)
                            to_node_position = file_rank
                            to_node = game.board.piece(Coord.from_notation(file_rank))
                            if from_node_position == to_node_position:
                                pass
                            else:
                                if side == 1:
                                    G.add_node(from_node_position, side="BLACK")
                                elif side == 0:
                                    G.add_node(from_node_position, side="WHITE")
                                try:
                                    if to_node.is_white:
                                        G.add_node(to_node_position, side="WHITE")
                                    elif to_node.is_black:
                                        G.add_node(to_node_position, side="BLACK")
                                except AttributeError:
                                    G.add_node(to_node_position, side="UNDEFINED")
                                if to_node == None:
                                    G.add_edge(from_node_position, to_node_position, weight=0.0)
                                elif i.is_opponent(to_node):
                                    G.add_edge(from_node_position, to_node_position, weight=-1.0)
                                else:
                                    G.add_edge(from_node_position, to_node_position, weight=1.0)                        
            fout.write(move + '\t')                
            fout.write(str(side) + '\t') 
            fout.write(str(nx.number_strongly_connected_components(G)) + '\t')
            fout.write(str(nx.number_weakly_connected_components(G)) + '\t')
            try:
                fout.write(str(nx.average_shortest_path_length(G)) + '\t')
            except:
                fout.write("Not connected" + '\t')
            fout.write(str(side == winner) + '\n')
            '''
            edefensive=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >= 0.0]
            #eoffensive=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <= 0.0]

            pos=nx.circular_layout(G) # positions for all nodes

            # nodes
            if side == 1:
                nx.draw_networkx_nodes(G,pos,nodelist=[node for (node,d) in G.nodes(data=True) if d['side'] == "BLACK"], node_color='blue',node_size=300)
                nx.draw_networkx_nodes(G,pos,nodelist=[node for (node,d) in G.nodes(data=True) if d['side'] == "UNDEFINED"], node_color='blue',node_size=300)
            elif side == 0:
                nx.draw_networkx_nodes(G,pos,nodelist=[node for (node,d) in G.nodes(data=True) if d['side'] == "WHITE"], node_color='red',node_size=300)
                nx.draw_networkx_nodes(G,pos,nodelist=[node for (node,d) in G.nodes(data=True) if d['side'] == "UNDEFINED"], node_color='red',node_size=300)

            # edges
            nx.draw_networkx_edges(G,pos,edgelist=edefensive, width=3, alpha=0.6, edge_color='black',arrows=True)
            #nx.draw_networkx_edges(G,pos,edgelist=eoffensive, width=3, alpha=0.6, edge_color='blue',style='dashed')

            # labels
            nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif')

            plt.axis('off')
            plt.savefig("weighted_graph" + "_" + str(side) + "_" + str(count) + ".png")
            plt.clf()
            '''
fout.close()

    #import all games in .pgn file                        
    #file_pgn = file("john.pgn")
    #
    #while True:
    #    game = Game()
    #    if not game.import_pgn(file_pgn):
    #        break
    #    print game.board

