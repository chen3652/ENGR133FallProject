'''
===============================================================================
ENGR 133 Fa 2020
Assignment Information
	Assignment:     Python Project
	Author:         Tejas Chandrasekhar, tlchandr@purdue.edu
                    Zachary Chen, chen3652@purdue 
                    Rajan Phadnis, rphadnis@purdue 
                    David Hegeburg, dhegberg@purdue 
	Team ID:        LC3-05 
	
	My contributor(s) helped me:	
	[ ] understand the assignment expectations without
		telling me how they will approach it.
	[ ] understand different ways to think about a solution
		without helping me plan my solution.
	[ ] think through the meaning of a specific error or
		bug present in my code without looking at my code.
	Note that if you helped somebody else with their code, you
	have to list that person as a contributor here as well.
===============================================================================
'''
import numpy as np
import matplotlib as lib
import matplotlib.pyplot as plt
import math
file_name = input("filename: ") #takes in a picture from the user who inputs the name of a file
variable = lib.image.imread(file_name) #matplot will read the image into an array
def greyscaleConverter(colorMatrix): #dotproduct will convert image into greyscale
    dot = np.dot(colorMatrix[...,:3], [0.2126, 0.7152, 0.0722]) #Formula for converting into greyscale, takes each term and calculates dotproduct
    return dot #returns dot product
def convolution(imageMatrix, convoluteMatrix, divisible):
    pad_length = (len(convoluteMatrix[0])-1)/2
    paddedImage = np.pad(imageMatrix, int(pad_length), mode="constant")
    finalImage = imageMatrix
    tx = int(pad_length)
    ty = int(pad_length)
    for row in imageMatrix:
        for pixel in row:
            kernel = convoluteMatrix
            x=-int(pad_length)
            y=-int(pad_length)
            try:
                for krow in range(0,len(convoluteMatrix)):
                    for kpixel in range(0,len(convoluteMatrix)):
                        kernel[x][y] = paddedImage[tx+x][ty+y]
                        x = x + 1
                    y = y + 1
                    x=-int(pad_length) 
                totalDot = 0
                for i in range(0, len(convoluteMatrix)):
                    dotInitial = np.dot(kernel[i], convoluteMatrix[i])
                    totalDot += dotInitial/divisible
                print(f"{round(100*tx/imageMatrix.shape[0],2)}% Complete")
                finalImage[tx][ty] = totalDot
            except IndexError:
                break
            
            ty = ty + 1 
        tx = tx + 1  
        ty = int(pad_length)
        plt.imshow(finalImage, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
        plt.show()
    return finalImage
                
            
            
        
             
sk = [[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]]
# sk = [[1,1,1],[1,1,1],[1,1,1]]
finalFinalImage = variable
greyscalematrix = greyscaleConverter(variable)
blurred = convolution(greyscalematrix,sk,9)
gxOperator = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
gyOperator = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
gx= convolution(blurred, gxOperator,9)
gy= convolution(blurred, gyOperator,9)
initXVal = 0
for xVal in range(0,gx.shape[0]):
    initYVal = 0
    for yVal in range(0,gx.shape[1]):
        finalFinalImage[initXVal][initYVal] = math.sqrt((gx[initXVal][initYVal]**2) + (gy[initXVal][initYVal]**2))
        initYVal += 1
    initXVal += 1
    print(f"Sobel: {round(100*initXVal/gx.shape[0],2)}% Complete")
        
plt.imshow(finalFinalImage, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
plt.show()


'''
===============================================================================
ACADEMIC INTEGRITY STATEMENT
    I have not used source code obtained from any other unauthorized
    source, either modified or unmodified. Neither have I provided
    access to my code to another. The project I am submitting
    is my own original work.
===============================================================================
'''