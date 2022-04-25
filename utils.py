from operator import ne
from tkinter.messagebox import NO
import networkx as nx
from numpy import source 

def findMinCut(Gt,src,sink):
	src_val = src
	sink_val = sink
	G_orig = Gt.copy()   
	
	def bfs_traversal(s,t,Gt,parent):
		visited = set()
		queue = []
		queue.append(s)
		visited.add(s)
		curr_path = [s]
		while queue:
			u = queue.pop()
			for neightbor in Gt.neighbors(u):
				if neightbor not in visited and Gt.get_edge_data(u,neightbor)['capacity'] >0:
					queue.append(neightbor)
					#curr_path.append(neightbor)
					visited.add(neightbor)
					parent[neightbor] = u
					if neightbor ==t:
						return True  
		return False        
	parent = {}
	max_flow = 0
	source,sink = src,sink
	idx=0 
	print('Running BfS traversal')
	while bfs_traversal(source,sink,Gt,parent):
		#print('Bfs-traversal'+str(idx))
		idx+=1
		path_flow = float('inf')
		s = sink 
		while (s!=source):
			path_flow = min(path_flow,Gt.get_edge_data(parent[s],s)['capacity'])
			s = parent[s]
		max_flow+=path_flow
		v = sink 
		while (v!=source):
			u = parent[v]
			current_u_v_capacity = Gt.get_edge_data(u,v)['capacity']
			Gt.add_edge(u,v,capacity=current_u_v_capacity-path_flow)         
			Gt.add_edge(v,u,capacity=current_u_v_capacity+path_flow)
			v = parent[v]

	
	#return max_flow

#	visited=len(Gt.nodes)*[False]
	print('Number of nodes'+str(len(Gt.nodes)))
	# Finding the s-partition
	s_partition_ls = set()
	s_partition_ls.add(src)
	queue = [src]
	print('Fetching the S-partition')
	while queue:
		u = queue.pop()
		for neightbor in Gt.neighbors(u):
			if neightbor not in s_partition_ls and Gt.get_edge_data(u,neightbor)['capacity'] >0:
				queue.append(neightbor)
					#curr_path.append(neightbor)
				s_partition_ls.add(neightbor)
				parent[neightbor] = u
	print('Fetching the T-partition')
	t_partition_ls = set()
	t_partition_ls.add(sink)				
	for node in Gt.nodes():
		if node not in s_partition_ls:
			t_partition_ls.add(node)

	return s_partition_ls,t_partition_ls




	
	#dfs_traversal(src_val,float('inf'),{},[src_val],sink_val,Gt)
#    print(bfs_traversal('x','y',Gt))
		
	

	# s_partition_ls = [src_val]
	# def s_parition(src):
	#     for neigh in Gt.neighbors(src):
	#         print(Gt.get_edge_data(src,neigh)['capacity'])
	#         if Gt.get_edge_data(src,neigh)['capacity']  > 0:
	#             s_partition_ls.append(neigh)
	#             s_parition(neigh)

	# s_parition(src_val)
	# #print(s_partition_ls)
	# t_parition_ls = [sink_val]
	# for node in Gt.nodes():
	#     if not node in s_partition_ls and not node==sink_val:
	#         t_parition_ls.append(node)

	# return(s_partition_ls,t_parition_ls)
	#
# def s_partition(s,Gt):
# 	print('Fetching s-parition')
# 	visited = set()
# 	queue = []
# 	queue.append(s)
# 	visited.add(s)
# 	while queue:
# 		u = queue.pop()
# 		for neightbor in Gt.neighbors(u):
# 			if neightbor not in visited and Gt.get_edge_data(u,neightbor)['capacity'] >0:
# 				queue.append(neightbor)
# 					#curr_path.append(neightbor)
# 					visited.add(neightbor)
# 				parent[neightbor] = u
# 	t_partition_ls = []
# 	print('Fetching T-partition')
# 	print(len(Gt.nodes()))
# 	for node in Gt.nodes():
# 		if not node in visited:
# 			t_partition_ls.append(node)             
# 	return visited,t_partition_ls 

# Gt = nx.DiGraph()
# Gt.add_edge("x", "a", capacity=3.0,flow=0)
# Gt.add_edge("x", "b", capacity=1.0,flow=0)
# Gt.add_edge("a", "c", capacity=3.0,flow=0)
# Gt.add_edge("b", "c", capacity=5.0,flow=0)
# Gt.add_edge("b", "d", capacity=4.0,flow=0)
# Gt.add_edge("d", "e", capacity=2.0,flow=0)
# Gt.add_edge("c", "y", capacity=2.0,flow=0)
# Gt.add_edge("e", "y", capacity=3.0,flow=0)
# print(nx.minimum_cut(Gt,'x','y'))
# print(findMinCut(Gt,'x','y'))