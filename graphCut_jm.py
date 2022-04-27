import math
from random import random, randrange
from PIL import Image
from numpy import array
import networkx as nx 
from utils import findMinCut
from scipy.sparse import csr_matrix
import os
import sys

# Deleting files in a folder

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
	#print((csr_matrix(nx.adjacency_matrix(G)).toarray()) )
	#print("Generating the Adjacency Matrix File")
	if len(G.nodes) <=limit:
		print("Generating the Adjacency Matrix File")
		arr_matrix = (csr_matrix(nx.adjacency_matrix(G)).toarray()) 
		row_len = len(arr_matrix)
		col_len = len(arr_matrix[0])
		file_obj = open(file_name,"w")
		curr_idx = 0 
		#file_obj.write(str(csr_matrix(nx.adjacency_matrix(G)).toarray()))
		
		file_obj.write(" ")
		for idx in range(col_len):
			file_obj.write(str(idx))
			file_obj.write(" ")
		file_obj.write("\n")
		for idx_i in range(row_len):
			file_obj.write(str(curr_idx)+" ")
			for idx_j in range(col_len):
				matrix_val = arr_matrix[idx_i][idx_j]
				file_obj.write(str(matrix_val))
				file_obj.write(" ")
			file_obj.write("\n")
			curr_idx+=1
		file_obj.close()

def printCuts(G,s_partition,t_partition,file_name):
	
	print("Generating the cuts(partition) files"+str(len(s_partition))+"--"+str(len(t_partition)))
	file_obj = open(file_name,"w")
	file_obj.write('------_S_Partition-------')
	file_obj.write("\n")
		#file_obj.write('------_S_Partition-------')
	for pixel in s_partition:
		file_obj.write(str(pixel))
		file_obj.write(" ")
	file_obj.write("\n")
	file_obj.write('------_T_Partition-------')
	file_obj.write("\n")
	for pixel in t_partition:
		file_obj.write(str(pixel))
		file_obj.write(" ")
	file_obj.close()


def createImageFromArr(arr):

	im_output = Image.fromarray(arr)
	return im_output



def createImage(height,width):
	im= Image.new('RGB', (height, width))
	new_pxls_arr=[]
	for _ in range(height*width):
		#new_pxls_arr.append((255,255,255)) 
		new_pxls_arr.append((0,0,0))
	im.putdata(new_pxls_arr)
	im.save('outputTexture.jpg')
	return im




def fecthRandomPatch(src_img_height,src_img_width,limit):
	patch_start_px_x = randrange(1,src_img_height-limit)
	patch_start_px_y = randrange(1,src_img_width-limit)
	return (patch_start_px_x,patch_start_px_y)


def constructFinalImage(final_image_name):
	pass	





output_txture_map = {}
patch_texture_map = {}



deleteFiles('Overlap')
deleteFiles('adjMatrix')
deleteFiles('Cuts')
	
output_width,output_height = 300,300 # The Output File dimensions are pre-determined.
patch_height,patch_width = 150,150 # The Patch File dimensions are pre-determined.
#im_src = Image.open('Images/berry_jpg.jpeg')
image_name = sys.argv[1]
im_src = Image.open(os.getcwd()+'/Images/'+image_name)
ar_src = array(im_src)
height,width = (ar_src.shape[0],ar_src.shape[1])
print(height,width)

G = nx.Graph()


im_output = createImage(output_height,output_width)
ar_output = array(im_output)
im_output = Image.fromarray(ar_output)




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
	


def fetchOverlapRegion(patch_start_index_x,patch_start_index_y,img_arr,src_patch_pixel):
	# Compare output Texture with patch 
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



def belongstoNewPatch(patch_b_hmap,curr_pxl):
	if curr_pxl in patch_b_hmap:
		return True 
	return False

# Minimum Cut = {S,T} Red --> S, Green --> T
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

# Return True if all adjacent pixels belong to overlap region Else false and if it belongs to Patch-B (New Patch)
# Checks in all 8 directions
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
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x-1,pxl_y-1)] = True
	if not ((pxl_x-1)>=0 and (pxl_x-1,pxl_y) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x-1,pxl_y))  
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x-1,pxl_y) in edge_rcv_hmap)
		or ((pxl_x-1,pxl_y) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x-1,pxl_y),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x-1,pxl_y),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x-1,pxl_y)] = True
	if not((pxl_y-1)>=0 and (pxl_x,pxl_y-1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x,pxl_y-1))  
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x,pxl_y-1) in edge_rcv_hmap)
		or ((pxl_x,pxl_y-1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x,pxl_y-1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x,pxl_y-1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x,pxl_y-1)] = True
	if not((pxl_x+1<original_patch_height) and (pxl_y-1)>=0 and (pxl_x+1,pxl_y-1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x+1,pxl_y-1)) 
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x+1,pxl_y-1) in edge_rcv_hmap)
		or ((pxl_x+1,pxl_y-1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x+1,pxl_y-1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x+1,pxl_y-1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x+1,pxl_y-1)] = True
	if not((pxl_x+1<original_patch_height) and (pxl_x+1,pxl_y) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x+1,pxl_y))  
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x+1,pxl_y) in edge_rcv_hmap)
		or ((pxl_x+1,pxl_y) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x+1,pxl_y),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x+1,pxl_y),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x+1,pxl_y)] = True
	if not((pxl_x-1>=0) and (pxl_y+1<original_patch_width) and (pxl_x-1,pxl_y+1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x-1,pxl_y+1))  
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x-1,pxl_y+1) in edge_rcv_hmap)
		or ((pxl_x-1,pxl_y+1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)
		):
			G.add_edge((pxl_x,pxl_y),(pxl_x-1,pxl_y+1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x-1,pxl_y+1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x-1,pxl_y+1)] = True
	if not((pxl_y+1<original_patch_width) and (pxl_x,pxl_y+1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x,pxl_y+1)) 
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x,pxl_y+1) in edge_rcv_hmap)or ((pxl_x,pxl_y+1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)):
			G.add_edge((pxl_x,pxl_y),(pxl_x,pxl_y+1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x,pxl_y+1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
			edge_incident_hmap[(pxl_x,pxl_y)] = True
			edge_rcv_hmap[(pxl_x,pxl_y+1)] = True
	if not((pxl_x+1<original_patch_height) and (pxl_y+1<original_patch_width) and (pxl_x+1,pxl_y+1) in overlap_pxl_hmap):
		return False,belongstoNewPatch(patch_b_hmap,(pxl_x+1,pxl_y+1)) 
	else:
		if not (((pxl_x,pxl_y) in edge_incident_hmap and (pxl_x+1,pxl_y+1) in edge_rcv_hmap)or ((pxl_x+1,pxl_y+1) in edge_incident_hmap and (pxl_x,pxl_y) in edge_rcv_hmap)):
			G.add_edge((pxl_x,pxl_y),(pxl_x+1,pxl_y+1),capacity= (computeweighingCost((pxl_x,pxl_y),(pxl_x+1,pxl_y+1),ar_src,ar_output,overlap_pxl_hmap)),flow=0)
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

#trial_run_steps = 20
flow_val,(ptchA_dict,ptchB_dict) = 0,({},{})
# Patches are 50*50
s_parition,t_partition = [],[]
ovlp_image_idx = 1
while  (len(t_partition) >2 or len(t_partition)==0):
	src_patch_pixel = fecthRandomPatch(height,width,patch_height)
	tgt_patch_pixel = fecthRandomPatch(output_height,output_width,patch_height)
	overlap_pxl_hmap = {}
	overlap_pxls_ls = []
	patch_b_hmap = {}
	overlap_pxls_ls,overlap_pxl_hmap,patch_b_hmap = fetchOverlapRegion(tgt_patch_pixel[0],tgt_patch_pixel[1],ar_output,src_patch_pixel)
	
	if len(overlap_pxls_ls) > 0:
		G = nx.DiGraph()
		interior_pxl = calculateCut(overlap_pxls_ls,patch_b_hmap,overlap_pxl_hmap,tgt_patch_pixel)
		if not G.has_node('t'):
			# Note: When the overlap region is fully covered.
			G.add_edge(interior_pxl,'t',capacity=float('inf'))
		if len(G.nodes) > 5500:
			flow_val,(s_parition,t_partition)=nx.minimum_cut(G,'s','t')
		else:
			s_parition,t_partition = findMinCut(G,'s','t')
		print('Modifying the output image'+str(len(s_parition))+'---'+str(len(t_partition))+'----'+str(len(overlap_pxl_hmap)))
		createOverlapImage(ar_output.copy(),'Overlap/OverlapImage_'+str(ovlp_image_idx)+'.jpeg',overlap_pxl_hmap,s_parition,t_partition)
		printAdjMatrix(G,'adjMatrix/adjMatrix_'+str(ovlp_image_idx)+'.txt',3500)
		printCuts(G,s_parition,t_partition,'Cuts/cutslist_'+str(ovlp_image_idx)+'.txt')
		ovlp_image_idx+=1
		for pixels in t_partition:
			if not pixels == 't':
				# Provide the output pixels with the pixels from the New Patch
				ar_output[pixels[0]][pixels[1]] = ar_src[overlap_pxl_hmap[pixels][0]][overlap_pxl_hmap[pixels][1]]
		im_output = createImageFromArr(ar_output)
		im_output.save('OutputImage.jpg')
		overlap_pxl_hmap = {}
		
	else:
		# No overlap
		im_output = createImageFromArr(ar_output)
		im_output.save('OutputImage.jpg')
		overlap_pxl_hmap = {}






