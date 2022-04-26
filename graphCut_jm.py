from http.client import IM_USED
import math
from random import random, randrange
from PIL import Image
from numpy import array
import networkx as nx 
from networkx.algorithms.flow import shortest_augmenting_path
from utils import findMinCut
from scipy.sparse import csr_matrix
import sys
#sys.setrecursionlimit(5000)
import os, shutil

def deleteFiles(folder_name):
	
	folder = os.getcwd()+'/'+str(folder_name)
	print(folder)
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		#print(file_path)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.remove(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))


# Restricting the adjacency matrix if number of nodes is less than the limit since file writing takes heavy time
def printAdjMatrix(G,file_name,limit):
	#print(nx.adjacency_matrix(G))
	if len(G.nodes) <=limit:
		arr_matrix = (csr_matrix(nx.adjacency_matrix(G)).toarray()) 
		row_len = len(arr_matrix)
		col_len = len(arr_matrix[0])
		file_obj = open(file_name,"w")
		curr_idx = 0 
		file_obj.write("\t")
		for idx in range(col_len):
			file_obj.write(str(idx))
			file_obj.write("\t")
		file_obj.write("\n")
		for idx_i in range(row_len):
			file_obj.write(str(curr_idx)+"\t")
			for idx_j in range(col_len):
				matrix_val = arr_matrix[idx_i][idx_j]
				file_obj.write(str(matrix_val))
				file_obj.write("\t")
			file_obj.write("\n")
			curr_idx+=1
		file_obj.close()

class pixelNode:

	def __init__(self,x_index,y_index) -> None:
		self.x_index  = x_index
		self.y_index = y_index

def createImageFromArr(arr):
	#print(len(arr))
	im_output = Image.fromarray(arr)
	return im_output



def createImage(height,width):
	im= Image.new('RGB', (height, width))
	new_pxls_arr=[]
	for _ in range(height*width):
		new_pxls_arr.append((255,255,255))
	#im.putdata([(255,0,0), (0,255,0), (0,0,255)])
	im.putdata(new_pxls_arr)
	im.save('outputTexture.jpg')
	return im

def canMoveRight(cur_idx_val,width):
	if cur_idx_val+1 > width -1:
		return False 
	return True

def canMoveDown(cur_idx_val,height):
	if cur_idx_val+1 > height - 1:
		return False 
	return True 

def canMoveDiag(cur_idx_i_val,cur_idx_j_val,height,width):
	if cur_idx_i_val +1 > height -1 or cur_idx_j_val +1 > width -1 :
		return False 
	return True 

def checkifinitCol(index_j):
	if index_j == 0:
		return True 
	return False 

def checkiffinalCol(index_j,width):
	if index_j == width - 1:
		return True 
	return False 

def fecthRandomPatch(src_img_height,src_img_width,limit):
	patch_start_px_x = randrange(1,src_img_height-limit)
	patch_start_px_y = randrange(1,src_img_width-limit)
	return (patch_start_px_x,patch_start_px_y)

# For Overlap Region
def findleftHeight (index_i,index_j,hmap):
	left_height = 0
	while (index_i,index_j) in hmap and index_j>=0:
		index_j-=1
		left_height+=1
	return left_height

# For Overlap region

def findUpHeight(index_i,index_j,hmap):
	up_height = 0
	#print('Up Height'+str(index_i))
	while (index_i,index_j) in hmap and index_i>=0:
		index_i-=1
		up_height+=1
	#print('Up Height'+str(index_i))    
	return up_height

def findDownHeight(index_i,index_j,hmap,output_height):
	down_height = 0
	#print('Down'+str(output_height))
	while (index_i,index_j) in hmap and index_i <=output_height:
		index_i+=1
		down_height+=1
	return down_height-1

# For Overlap Region
# 
def findRightHeight(index_i,index_j,hmap,output_width):
	right_height = 0 
	#print('Right-height'+str(index_j))
	while (index_i,index_j) in hmap and index_j<=output_width:
		index_j+=1
		right_height+=1
	#print('Right-height'+str(index_j))    
	return right_height -1

output_txture_map = {}
patch_texture_map = {}

def computeOverlapRegion(patch_start_index_x,patch_start_index_y,img_arr,src_patch_pixel):
	# Compare output Texture with patch 
	#start_pixel = [patch_start_index_x][patch_start_index_y]
	src_patch_x = src_patch_pixel[0]
	src_patch_y = src_patch_pixel[1]
	overlap_region_fnd = False
	overlap_region_height,overlap_region_width,overlap_region_init_px = 0,0,[0,0]
	for index_i in range(patch_start_index_x,patch_start_index_x+patch_height):
		src_patch_y = src_patch_pixel[1]
		for index_j in range(patch_start_index_y,patch_start_index_y+patch_width):
			curr_pixel = img_arr[index_i][index_j]
			
			if (index_i,index_j) in output_txture_map and not overlap_region_fnd:
				#print('Overlap initial',str(index_i),str(index_j))
				if (index_i,index_j) in patch_texture_map:
					#overlap_pixels.append((index_i,index_j))
					# Go left 
					curr_index_i,curr_index_j = index_i,index_j 
					#left_height = findleftHeight(curr_index_i,curr_index_j,patch_texture_map)
					#print(curr_index_i,curr_index_j,left_height)
					#up_height = findUpHeight(curr_index_i,curr_index_j,patch_texture_map)
					#print(up_height)
					right_height = findRightHeight(curr_index_i,curr_index_j,patch_texture_map,patch_start_index_y+patch_width)
					#print(right_height)
					bottom_height = findDownHeight(curr_index_i,curr_index_j,patch_texture_map,patch_start_index_x+patch_height)
					while (curr_index_i,curr_index_j) in patch_texture_map and curr_index_j>=0:
						curr_index_j-=1
						
					# Go up 
					while (curr_index_i,curr_index_j) in patch_texture_map and curr_index_i>=0:
						curr_index_i-=1
						
					# Go right 
					overlap_region_init_px = [patch_start_index_x,patch_start_index_y]
					overlap_region_height =  bottom_height
					overlap_region_width =  right_height 
					overlap_region_fnd = True
					#return overlap_region_height,overlap_region_width,overlap_region_init_px
				else:
					patch_texture_map[(index_i,index_j)] = True 
			else:
				output_txture_map[(index_i,index_j)] = True 
				patch_texture_map[(index_i,index_j)] = True
				#print(src_patch_x,src_patch_y)
				ar_output[index_i-1][index_j-1] = ar_src[src_patch_x-1][src_patch_y-1]
			src_patch_y+=1
		src_patch_x+=1
	return overlap_region_height,overlap_region_width,overlap_region_init_px


deleteFiles('Overlap')
deleteFiles('adjMatrix')
	
output_width,output_height = 500,500
patch_height,patch_width = 200,200
#im_src = Image.open('Images/olives.jpeg')
im_src = Image.open('Images/olives.jpeg')
#im_src = Image.open('kboard.png')
ar_src = array(im_src)
height,width = (ar_src.shape[0],ar_src.shape[1])
print(height,width)

# for index_i in range(height):
#     for index_j in range(width):
#         #print(ar_src[index_i][index_j])
#         pass

G = nx.Graph()


im_output = createImage(output_height,output_width)
ar_output = array(im_output)
im_output = Image.fromarray(ar_output)




#print((height,width))
# im_dest = Image.open('target.jpg')
# ar_tgt = array(im_dest)
# height_d,width_d = (ar_tgt.shape[0],ar_tgt.shape[1])
# output_height,output_width = (height_d,width_d)
# ar_output = ar_tgt
# for index_i in range(height_d):
#     for index_j in range(width_d):
#         #print(ar_tgt[index_i][index_j])
#         #G.add_node(pixelNode(index_i,index_j))
#         pass
		

# Question: How to show the pixel
#im= Image.new('RGB', (1024, 1024))
#im.putdata([(255,0,0), (0,255,0), (0,0,255)])
#im.save('test.png')
#new_image = Image.fromarray(ar_tgt)
#new_image.save('tgt.jpg')

# Compute the weighing cost. 
 



# Compute Weighing cost only for overlap patches
def computeweighingCost(px1,px2,old_patch,new_patch,overlap_pxl_hmap):
	# Test it at 100,100,101,101 ||A(s) - B(s) || + ||A(t) - B(t)
	as_r,as_g,as_b = old_patch[overlap_pxl_hmap[px1][0]][overlap_pxl_hmap[px1][1]]
	at_r,at_g,at_b = old_patch[overlap_pxl_hmap[px2][0]][overlap_pxl_hmap[px2][1]]
	bs_r,bs_g,bs_b = new_patch[px1[0]][px1[1]]
	bt_r,bt_g,bt_b = new_patch[px2[0]][px2[1]]
	rs_r = math.sqrt(abs(int(int(as_r) - int(bs_r)))) + math.sqrt(abs(int(int(at_r) - int(bt_r))))
	rs_g = math.sqrt(abs(int(int(as_g) - int(bs_g)))) + math.sqrt(abs(int(int(at_g) - int(bt_g))))
	#print(at_b,at_g)
	rs_b = math.sqrt(abs(int(int(as_b) - int(bs_b)))) + math.sqrt(abs(int(int(at_b) - int(bt_b))))
	return (rs_r+rs_g+rs_b)
	
#print(computeweighingCost([50,51],[51,51],ar_src,ar_output))

def fetchOverlapRegion(patch_start_index_x,patch_start_index_y,img_arr,src_patch_pixel):
	# Compare output Texture with patch 
	#start_pixel = [patch_start_index_x][patch_start_index_y]
	src_patch_x = src_patch_pixel[0]
	src_patch_y = src_patch_pixel[1]
	patch_b_hmap = {}
	overlap_pxls_ls = []
	overlap_pxl_hmap = {}
	for index_i in range(patch_start_index_x,patch_start_index_x+patch_height):
		src_patch_y = src_patch_pixel[1]
		for index_j in range(patch_start_index_y,patch_start_index_y+patch_width):
			curr_pixel = img_arr[index_i][index_j]
			if (index_i,index_j) in output_txture_map:
				#print('Overlap initial',str(index_i),str(index_j))
				overlap_pxls_ls.append((index_i,index_j))
				overlap_pxl_hmap[(index_i,index_j)] = (src_patch_x-1,src_patch_y-1)
			else:
				output_txture_map[(index_i,index_j)] = True 
				patch_texture_map[(index_i,index_j)] = True
				#print(src_patch_x,src_patch_y)
				ar_output[index_i-1][index_j-1] = ar_src[src_patch_x-1][src_patch_y-1]
				patch_b_hmap[(index_i,index_j)] = True
			src_patch_y+=1
		src_patch_x+=1
	return overlap_pxls_ls,overlap_pxl_hmap,patch_b_hmap






# 0,0 0,1 0,2 
# 21,21  : Neighboring pixels [20,21] [21,22] [21,20][22,21]
# Each pixel will act as a Node and you can compute the weighing cost accordingly.

# G = nx.DiGraph()
# G.add_node(1)
# G.add_node(2)
# G.add_edge(1,2)
# print(G.graph)
# print([n for n in G if n < 3])
# print(G.edges)

# The only directions possible for flow are [down,right,diagonal]

# Gt = nx.DiGraph()
# Gt.add_edge("x", "a", capacity=3.0)
# Gt.add_edge("x", "b", capacity=1.0)
# Gt.add_edge("a", "c", capacity=3.0)
# Gt.add_edge("b", "c", capacity=5.0)
# Gt.add_edge("b", "d", capacity=4.0)
# Gt.add_edge("d", "e", capacity=2.0)
# Gt.add_edge("c", "y", capacity=2.0)
# Gt.add_edge("e", "y", capacity=3.0)
# #flow_value, flow_dict = nx.maximum_flow(G, "x", "y")
# print(nx.minimum_cut(Gt,"x","y"))
#print(flow_value)
#print(flow_dict["x"]["b"])
#print([n for n in G])
#print(len(G.nodes))

#height_d=10
#width_d=10

def computeGraph(overlap_region_height,overlap_region_width,overlap_region_pixel):
	overlap_region_init_col = overlap_region_pixel[1]
	overlap_region_fin_col = overlap_region_init_col + overlap_region_width
	#print(overlap_region_fin_col)
	missing_nodes,loop_cnt=0,0
	for index_i in range(overlap_region_pixel[0],overlap_region_pixel[0]+overlap_region_height):
		for index_j in range(overlap_region_pixel[1],overlap_region_pixel[1]+overlap_region_width):
			# dst_pxl_val = ar_output[index_i][index_j]
			# src_pxl_val = ar_src[index_i][index_j]
			test_bool = False
			if canMoveRight(index_j,overlap_region_pixel[1]+overlap_region_width):
				G.add_edge((index_i,index_j),(index_i,index_j+1),capacity= (computeweighingCost([index_i,index_j],[index_i,index_j+1],ar_src,ar_output)),flow=0)
				#test_bool = True 
			if canMoveDown(index_i,overlap_region_pixel[0]+overlap_region_height):
				G.add_edge((index_i,index_j),(index_i+1,index_j),capacity= (computeweighingCost([index_i,index_j],[index_i+1,index_j],ar_src,ar_output)),flow=0)
				#test_bool = True
			if canMoveDiag(index_i,index_j,overlap_region_pixel[0]+overlap_region_height,overlap_region_pixel[1]+overlap_region_width):
				G.add_edge((index_i,index_j),(index_i+1,index_j+1),capacity= (computeweighingCost([index_i,index_j],[index_i+1,index_j+1],ar_src,ar_output)),flow=0)
				#test_bool =  True
			# if not test_bool:
			#     #print((index_i,index_j))
			#     missing_nodes+=1
			if overlap_region_init_col == (index_j):
				G.add_edge('s',(index_i,index_j),capacity=float('inf'))
			if overlap_region_fin_col-1 == index_j:
				G.add_edge((index_i,index_j),'t',capacity=float('inf'))
			#loop_cnt+=1
	flow_value, flow_dict = (nx.minimum_cut(G,'s','t'))

def belongstoNewPatch(patch_b_hmap,curr_pxl):
	if curr_pxl in patch_b_hmap:
		return True 
	return False

def createOverlapImage(ar_output_ov,overlap_img_name,overlap_pxl_hmap,s_partition,t_partition):
	height_overlap = ar_output_ov.shape[0]
	width_overlap = ar_output_ov.shape[1]
	r_color = (255,51,51)
	g_color = (0,255,0)
	for idx_i in range(height_overlap):
		for idx_j in range(width_overlap):
			curr_pxl = (idx_i,idx_j)
			if curr_pxl in overlap_pxl_hmap and curr_pxl in s_partition:
				ar_output_ov[idx_i][idx_j] = r_color
			elif curr_pxl in overlap_pxl_hmap and curr_pxl in t_partition:
				ar_output_ov[idx_i][idx_j] = g_color
	im_overlap = createImageFromArr(ar_output_ov)
	im_overlap.save(overlap_img_name)

# Return True if all adjacent pixels belong to overlap region Else false and if it belongs to Patch-B

def checkforAdjacentPixels(curr_pxl,patch_b_hmap,overlap_pxl_hmap,original_patch_height,original_patch_width):
	pxl_x = curr_pxl[0]
	pxl_y = curr_pxl[1]
	edge_hmap = {}
	edge_incident_hmap = {}
	edge_rcv_hmap = {}
	if not ((pxl_x-1)>=0 and (pxl_y-1)>=0 and (pxl_x-1,pxl_y-1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x-1,pxl_y-1)) 
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x-1,pxl_y-1) in edge_rcv_hmap)
		or ((pxl_x-1,pxl_y-1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x-1,pxl_y-1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x-1,pxl_y-1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
		#edge_hmap['(pxl_x,pxl_y)'+'(pxl_x-1,pxl_y-1)'] = True 
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x-1,pxl_y-1)] = True
	if not ((pxl_x-1)>=0 and (pxl_x-1,pxl_y) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x-1,pxl_y))  
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x-1,pxl_y) in edge_rcv_hmap)
		or ((pxl_x-1,pxl_y) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x-1,pxl_y),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x-1,pxl_y),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
		#edge_hmap['(pxl_x,pxl_y)'+'(pxl_x-1,pxl_y)'] = True 
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x-1,pxl_y)] = True
	if not((pxl_y-1)>=0 and (pxl_x,pxl_y-1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x,pxl_y-1))  
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x,pxl_y-1) in edge_rcv_hmap)
		or ((pxl_x,pxl_y-1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x,pxl_y-1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x,pxl_y-1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
		#edge_hmap['(pxl_x,pxl_y)'+'(pxl_x,pxl_y-1)'] = True 
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x,pxl_y-1)] = True
	if not((pxl_x+1<original_patch_height) and (pxl_y-1)>=0 and (pxl_x+1,pxl_y-1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x+1,pxl_y-1)) 
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x+1,pxl_y-1) in edge_rcv_hmap)
		or ((pxl_x+1,pxl_y-1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x+1,pxl_y-1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x+1,pxl_y-1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
		#edge_hmap['(pxl_x,pxl_y)'+'(pxl_x+1,pxl_y-1)'] = True  
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x+1,pxl_y-1)] = True
	if not((pxl_x+1<original_patch_height) and (pxl_x+1,pxl_y) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x+1,pxl_y))  
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x+1,pxl_y) in edge_rcv_hmap)
		or ((pxl_x+1,pxl_y) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x+1,pxl_y),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x+1,pxl_y),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
		#edge_hmap['(pxl_x,pxl_y)'+'(pxl_x+1,pxl_y)'] = True 
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x+1,pxl_y)] = True
	if not((pxl_x-1>=0) and (pxl_y+1<original_patch_width) and (pxl_x-1,pxl_y+1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x-1,pxl_y+1))  
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x-1,pxl_y+1) in edge_rcv_hmap)
		or ((pxl_x-1,pxl_y+1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x-1,pxl_y+1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x-1,pxl_y+1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
		#edge_hmap['(pxl_x,pxl_y)'+'(pxl_x-1,pxl_y+1)'] = True 
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x-1,pxl_y+1)] = True
	if not((pxl_y+1<original_patch_width) and (pxl_x,pxl_y+1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x,pxl_y+1)) 
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x,pxl_y+1) in edge_rcv_hmap)or ((pxl_x,pxl_y+1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)):
			G.add_edge((pxl_x,pxl_y),(pxl_x,pxl_y+1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x,pxl_y+1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
		#edge_hmap['(pxl_x,pxl_y)'+'(pxl_x,pxl_y+1)'] = True  
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x,pxl_y+1)] = True
	if not((pxl_x+1<original_patch_height) and (pxl_y+1<original_patch_width) and (pxl_x+1,pxl_y+1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x+1,pxl_y+1)) 
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x+1,pxl_y+1) in edge_rcv_hmap)or ((pxl_x+1,pxl_y+1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)):
			G.add_edge((pxl_x,pxl_y),(pxl_x+1,pxl_y+1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x+1,pxl_y+1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
		#edge_hmap['(pxl_x,pxl_y)'+'(pxl_x+1,pxl_y+1)'] = True  
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x+1,pxl_y+1)] = True
	return True,None


def calculateCut(overlap_pxls_ls,patch_b_hmap,overlap_pxl_hmap,tgt_patch_pixel):
	interior_pxl = None
	for curr_pxl in overlap_pxls_ls:
		pxl_x = curr_pxl[0]
		pxl_y = curr_pxl[1]
		original_patch_height = tgt_patch_pixel[0] + patch_height # Highest point of patch 
		original_patch_width = tgt_patch_pixel[1] + patch_width # Furthest point of patch
		overlap_covered,b_patch = checkforAdjacentPixels(curr_pxl,patch_b_hmap,overlap_pxl_hmap,original_patch_height,original_patch_width)
		if overlap_covered:
			# It means that the edges capacities were computed
			interior_pxl = curr_pxl
		else:
			if b_patch:
				G.add_edge(curr_pxl,'t',capacity=float('inf'),flow=0)
			else:
				G.add_edge('s',curr_pxl,capacity=float('inf'),flow=0)
	return interior_pxl
	#print(len(G.nodes))

	#print(missing_nodes,loop_cnt)
	#print('S---'+str(len(flow_dict[0]))+'---T---'+str(len(flow_dict[1])))

		
#print(len(G.nodes))
#print(G.graph)

#flow_val,(ptchA_dict,ptchB_dict)=(nx.minimum_cut(G,'s','t'),flow_func=shortest_augmenting_path)
#flow_val,(ptchA_dict,ptchB_dict) = nx.minimum_cut(G, "s", "t", flow_func=shortest_augmenting_path)
#print(cut_value)
#flow_val,(ptchA_dict,ptchB_dict)=(nx.minimum_cut(G,(1,2),(10,3)))

# print(ptchB_dict)
# print('===')
# print(ptchA_dict)

trial_run_steps = 20
flow_val,(ptchA_dict,ptchB_dict) = 0,({},{})
# Patches are 50*50
s_parition,t_partition = [],[]
ovlp_image_idx = 1
while  (len(t_partition) >2 or len(t_partition)==0) and trial_run_steps>0:
	src_patch_pixel = fecthRandomPatch(height,width,patch_height)
	tgt_patch_pixel = fecthRandomPatch(output_height,output_width,patch_height)
	#print(src_patch_pixel)
	#print(tgt_patch_pixel)
	overlap_pxl_hmap = {}
	overlap_pxls_ls = []
	patch_b_hmap = {}
	overlap_pxls_ls,overlap_pxl_hmap,patch_b_hmap = fetchOverlapRegion(tgt_patch_pixel[0],tgt_patch_pixel[1],ar_output,src_patch_pixel)
	
	if len(overlap_pxls_ls) > 0:
		#print(overlap_region_height,overlap_region_width,overlap_region_init_px)
		#computeGraph(overlap_region_height,overlap_region_width,overlap_region_init_px)
		#print(len(overlap_pxls_ls))
		G = nx.DiGraph()
		#print(len(G.nodes))
		interior_pxl = calculateCut(overlap_pxls_ls,patch_b_hmap,overlap_pxl_hmap,tgt_patch_pixel)
		if not G.has_node('t'):
			# Note: When the overlap region is fully covered.
			#print('Overlap region is fully covered')
			#print(len(overlap_pxls_ls))
			# curr_idx=0
			# while G.has_edge('s',(overlap_pxls_ls[curr_idx][0],overlap_pxls_ls[curr_idx][1])):
			#     curr_idx+=1
			#G.add_edge((overlap_pxls_ls[curr_idx][0],overlap_pxls_ls[curr_idx][1]),'t',capacity=float('inf'))
			G.add_edge(interior_pxl,'t',capacity=float('inf'))
		#flow_val,(ptchA_dict,ptchB_dict)=nx.minimum_cut(G,'s','t')
		#print('Pre Calculating Partition')
		#s_parition,t_partition = findMinCut(G,'s','t')
		flow_val,(s_parition,t_partition)=nx.minimum_cut(G,'s','t')
		print('Modifying the output image'+str(len(s_parition))+'---'+str(len(t_partition))+'----'+str(len(overlap_pxl_hmap)))
		
		#Intermediate Output Overlap plus seam image
		if abs(len(s_parition) - len(t_partition)) < ((len(s_parition) + len(t_partition))//2) or True:
			createOverlapImage(ar_output.copy(),'Overlap/OverlapImage'+str(ovlp_image_idx)+'.jpeg',overlap_pxl_hmap,s_parition,t_partition)
			
			#print(nx.adjacency_matrix((Gt)))
			printAdjMatrix(G,'adjMatrix/adjMatrix_'+str(ovlp_image_idx)+'.txt',4000)
#			arr_matrix = (csr_matrix(nx.adjacency_matrix(G)).toarray())
			
			ovlp_image_idx+=1
		for pixels in t_partition:
			
			if not pixels == 't':

				ar_output[pixels[0]][pixels[1]] = ar_src[overlap_pxl_hmap[pixels][0]][overlap_pxl_hmap[pixels][1]]
		
		

		im_output = createImageFromArr(ar_output)
		im_output.save('Otpt_2.jpg')
		overlap_pxl_hmap = {}
	else:
		# No overlap
		im_output = createImageFromArr(ar_output)
		im_output.save('Otpt_2.jpg')
		overlap_pxl_hmap = {}

	#trial_run_steps-=1





