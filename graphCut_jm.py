import math
from random import random, randrange
from PIL import Image
from numpy import array
import networkx as nx 
from networkx.algorithms.flow import shortest_augmenting_path

class pixelNode:

    def __init__(self,x_index,y_index) -> None:
        self.x_index  = x_index
        self.y_index = y_index

def createImageFromArr(arr):
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
    print('Up Height'+str(index_i))
    while (index_i,index_j) in hmap and index_i>=0:
        index_i-=1
        up_height+=1
    print('Up Height'+str(index_i))    
    return up_height

def findDownHeight(index_i,index_j,hmap):
    down_height = 0
    while (index_i,index_j) in hmap and index_i <=output_height:
        index_i+=1
        down_height+=1
    return down_height

# For Overlap Region
# 
def findRightHeight(index_i,index_j,hmap):
    right_height = 0 
    print('Right-height'+str(index_j))
    while (index_i,index_j) in hmap and index_j<=output_width:
        index_j+=1
        right_height+=1
    print('Right-height'+str(index_j))    
    return right_height 

output_txture_map = {}
patch_texture_map = {}

def computeOverlapRegion(patch_start_index_x,patch_start_index_y,img_arr,src_patch_pixel):
    # Compare output Texture with patch 
    #start_pixel = [patch_start_index_x][patch_start_index_y]
    src_patch_x = src_patch_pixel[0]
    src_patch_y = src_patch_pixel[1]
    overlap_region_height,overlap_region_width,overlap_region_init_px = 0,0,[0,0]
    for index_i in range(patch_start_index_x,patch_start_index_x+patch_height):
        src_patch_y = src_patch_pixel[1]
        for index_j in range(patch_start_index_y,patch_start_index_y+patch_width):
            curr_pixel = img_arr[index_i][index_j]
            if (index_i,index_j) in output_txture_map:
                if (index_i,index_j) in patch_texture_map:
                    #overlap_pixels.append((index_i,index_j))
                    # Go left 
                    curr_index_i,curr_index_j = index_i,index_j 
                    #left_height = findleftHeight(curr_index_i,curr_index_j,patch_texture_map)
                    #print(curr_index_i,curr_index_j,left_height)
                    #up_height = findUpHeight(curr_index_i,curr_index_j,patch_texture_map)
                    #print(up_height)
                    right_height = findRightHeight(curr_index_i,curr_index_j,patch_texture_map)
                    #print(right_height)
                    bottom_height = findDownHeight(curr_index_i,curr_index_j,patch_texture_map)
                    while (curr_index_i,curr_index_j) in patch_texture_map and curr_index_j>=0:
                        curr_index_j-=1
                        
                    # Go up 
                    while (curr_index_i,curr_index_j) in patch_texture_map and curr_index_i>=0:
                        curr_index_i-=1
                        
                    # Go right 
                    overlap_region_init_px = [patch_start_index_x,patch_start_index_y]
                    overlap_region_height =  bottom_height
                    overlap_region_width =  right_height 
                    #return overlap_region_height,overlap_region_width,overlap_region_init_px
                else:
                    patch_texture_map[(index_i,index_j)] = True 
            else:
                output_txture_map[(index_i,index_j)] = True 
                patch_texture_map[(index_i,index_j)] = True
                print(src_patch_x,src_patch_y)
                ar_output[index_i-1][index_j-1] = ar_src[src_patch_x-1][src_patch_y-1]
            src_patch_y+=1
        src_patch_x+=1
    return overlap_region_height,overlap_region_width,overlap_region_init_px



    
output_width,output_height = 500,500
patch_height,patch_width = 100,100
im_src = Image.open('src.jpg')
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
# print(height_d,width_d)
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
def computeweighingCost(px1,px2,old_patch,new_patch):
    # Test it at 100,100,101,101 ||A(s) - B(s) || + ||A(t) - B(t)
    as_r,as_g,as_b = old_patch[px1[0]][px1[1]]
    at_r,at_g,at_b = old_patch[px2[0]][px2[1]]
    bs_r,bs_g,bs_b = new_patch[px1[0]][px1[1]]
    bt_r,bt_g,bt_b = new_patch[px2[0]][px2[1]]
    rs_r = abs(int(int(as_r) - int(bs_r))) + abs(int(int(at_r) - int(bt_r)))
    rs_g = abs(int(int(as_g) - int(bs_g))) + abs(int(int(at_g) - int(bt_g)))
    #print(at_b,at_g)
    rs_b = abs(int(int(as_b) - int(bs_b))) + abs(int(int(at_b) - int(bt_b)))
    return (rs_r+rs_g+rs_b)
    
#print(computeweighingCost([50,51],[51,51],ar_src,ar_output))






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
#flow_value, flow_dict = nx.maximum_flow(G, "x", "y")
#print(nx.minimum_cut(Gt,"x","y"))
#print(flow_value)
#print(flow_dict["x"]["b"])
#print([n for n in G])
#print(len(G.nodes))

#height_d=10
#width_d=10

def computeGraph(overlap_region_height,overlap_region_width):

    for index_i in range(overlap_region_height):
        for index_j in range(overlap_region_width):
            dst_pxl_val = ar_output[index_i][index_j]
            src_pxl_val = ar_src[index_i][index_j]
            if canMoveRight(index_j,overlap_region_width):
                G.add_edge((index_i,index_j),(index_i,index_j+1),capacity= (computeweighingCost([index_i,index_j],[index_i,index_j+1],ar_src,ar_output)))
            if canMoveDown(index_i,overlap_region_height):
                G.add_edge((index_i,index_j),(index_i+1,index_j),capacity= (computeweighingCost([index_i,index_j],[index_i+1,index_j],ar_src,ar_output)))
            if canMoveDiag(index_i,index_j,overlap_region_height,overlap_region_width):
                G.add_edge((index_i,index_j),(index_i+1,index_j+1),capacity= (computeweighingCost([index_i,index_j],[index_i+1,index_j+1],ar_src,ar_output)))
            if checkifinitCol(index_j):
                G.add_edge('s',(index_i,index_j),capacity=float('inf'))
            if checkiffinalCol(index_j,overlap_region_width):
                G.add_edge((index_i,index_j),'t',capacity=float('inf'))

        
#print(len(G.nodes))
#print(G.graph)

#flow_val,(ptchA_dict,ptchB_dict)=(nx.minimum_cut(G,'s','t'),flow_func=shortest_augmenting_path)
#flow_val,(ptchA_dict,ptchB_dict) = nx.minimum_cut(G, "s", "t", flow_func=shortest_augmenting_path)
#print(cut_value)
#flow_val,(ptchA_dict,ptchB_dict)=(nx.minimum_cut(G,(1,2),(10,3)))

# print(ptchB_dict)
# print('===')
# print(ptchA_dict)

trial_run_steps = 100
# Patches are 50*50
while trial_run_steps:
    src_patch_pixel = fecthRandomPatch(height,width,patch_height)
    tgt_patch_pixel = fecthRandomPatch(output_height,output_width,patch_height)
    print(src_patch_pixel)
    print(tgt_patch_pixel)
    print(computeOverlapRegion(tgt_patch_pixel[0],tgt_patch_pixel[1],ar_output,src_patch_pixel))
    im_output = createImageFromArr(ar_output)
    im_output.save('Otpt_2.jpg')
    #print(patch_texture_map)
    trial_run_steps-=1




"""
Ford Fulkerson Algorithm
Construct a Residual Graph 
If there is a path from source to sink in the residual graph, add flow through it. 

"""