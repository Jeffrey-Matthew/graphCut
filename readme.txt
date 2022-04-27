Description: A Project based on the Paper - Graphcut Textures: Image and Video Synthesis Using Graph Cuts
Dependencies:
-- Python 3.9.10 
-- Python Packages: math,random,PIL,numpy,networkx,scipy,os 

To install the packages, python -m pip install Pillow numpy networkx scipy

Statement of Help: 

---------       Folder Structure  ---------
1. Cuts Folder : Provides the Text file of the cuts at each iteration (S,T) as requested 
2. Overlap Folder: Contains the Overlap Images at each stage. If (S,T) is considered as the cut, then {S} pixels are contained under RED Color ; {T} pixels are contained under GREEN color. 
3. Images Folder: Contains the input Images 
4. adjMatrix Folder: Provides a text file of the adjacency matrix but a limit is provided based on the number of nodes since text file generation takes too much time when the limit >3500.  [Line:321]

---------       Input           --------- 

1. Provide input image name as argument.

---------       Output            ---------
1. OutputImage.jpg = Final Output Image (GraphCut Algorithm is executed on the patches as long as the number of pixels coming from the new patch is minimum)

---------       Reference:         ---------       

For custom Min Cut Algorithm - https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/

---------       Notes           --------- 
1. For the custom Edmonds Karp algorithm, it is executed if the number of nodes is less than 5500 [Line:318]
   Because edmonds karp algorithm takes a lot of time to execute compared to the inbuilt library [Line:316] which I believe  uses preflow algorithms. 
   To ensure that the project doesn't run too long, the limit has been provided.

--          To run      --
python graphCut_jm.py <img_name>
E.g. python graphCut_jm.py olives.jpeg
Note: <img_name> should be present in the Images Folder
