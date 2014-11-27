#!/usr/bin/env python
import matplotlib.pyplot as plt
import networkx as nx

class visualization(object):
	@staticmethod
	def makeGraph():
		G=nx.star_graph(20)
		pos=nx.spring_layout(G)
		colors=range(20)
		nx.draw(G,pos,node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)
		plt.savefig("edge_colormap.png") # save as png
		plt.show() # display


