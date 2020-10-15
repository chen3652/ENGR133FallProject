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
# First, import all of the required packages/modules from numpy, python, and matplot
import numpy as np
import matplotlib as lib
import matplotlib.pyplot as plt
import math
#Get the name of the file to run the image processing on.
file_name = input("filename: ") #takes in a picture from the user who inputs the name of a file
# Open the file and read it into a matrix
variable = lib.image.imread(file_name) #matplot will read the image into an array

#Define a function that will convert the image to greyscale
def greyscaleConverter(colorMatrix): #dotproduct will convert image into greyscale
    dot = np.dot(colorMatrix[...,:3], [0.2126, 0.7152, 0.0722]) #Formula for converting into greyscale, takes each term and calculates dotproduct
    return dot #returns dot product
#define a function to generally convolutean image and a matrix, and then normalize it with a "divisible" factor
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
        # plt.imshow(finalImage, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
        # plt.show()
    return finalImage
                
# Define a function to convert the image to black and white based on a provided threshold
def thresh(greyscaleImage, threshNum):
    #set up basic image size matrix
    imageToReturn = greyscaleImage
    #set up initial counting variable
    initXVal = 0
    for xVal in range(0,greyscaleImage.shape[0]):
        initYVal = 0
        for yVal in range(0,greyscaleImage.shape[1]):
            #get the current pixel's black/white shade and store in a variable
            currentPixelColor = greyscaleImage[initXVal][initYVal]
            # If the shade is greater than the threshold, set it to 1
            if(currentPixelColor >= threshNum):
                #set the final picture's black/white shade to 1
                imageToReturn[initXVal][initYVal] = 1
            # If the shade is less than the threshold, set it to 0
            else:
                #set the final picture's black/white shade to 0
                imageToReturn[initXVal][initYVal] = 0
            initYVal += 1 # increment the y counter
        initXVal += 1 # increment the x counter
        # print the % complete
        print(f"Threshold: {round(100*initXVal/greyscaleImage.shape[0],2)}% Complete")
    # after running through each pixel, return the image that now consists of only black and white pixels (1 and 0)
    return imageToReturn

def edgeDetect(imageMatrix, convoluteMatrix):
    pad_length = (len(convoluteMatrix[0])-1)/2
    paddedImage = np.pad(imageMatrix, int(pad_length), mode="constant")
    finalImage = imageMatrix
    tx = int(pad_length)
    ty = int(pad_length)
    for row in imageMatrix:
        for pixel in row:
            # kernel = convoluteMatrix
            x=-int(pad_length)
            y=-int(pad_length)
            oneValue = 0
            zeroValue = 0
            try:
                for krow in range(0,len(convoluteMatrix)):
                    for kpixel in range(0,len(convoluteMatrix)):
                        if(paddedImage[tx+x][ty+y] == 1):
                            oneValue += 1
                        elif(paddedImage[tx+x][ty+y] == 0):
                            zeroValue += 1
                        else:
                            print(paddedImage[tx+x][ty+y])
                        x = x + 1
                    y = y + 1
                    x=-int(pad_length)   
                if(5 <= oneValue <= 7):
                    finalImage[tx][ty] = 1
                else:
                    finalImage[tx][ty] = 0
                # totalDot = 0
                # for i in range(0, len(convoluteMatrix)):
                #     dotInitial = np.dot(kernel[i], convoluteMatrix[i])
                #     totalDot += dotInitial/divisible
                print(f"Edge Detection: {round(100*tx/imageMatrix.shape[0],2)}% Complete")
                # finalImage[tx][ty] = totalDot
            except IndexError:
                break
            
            ty = ty + 1 
        tx = tx + 1  
        ty = int(pad_length)
        # plt.imshow(finalImage, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
        # plt.show()
    return finalImage


def sobel(imageMatrix):
    finalFinalImage = imageMatrix
    gxOperator = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    gyOperator = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    gx = convolution(imageMatrix, gxOperator,9)
    gy = convolution(imageMatrix, gyOperator,9)
    initXVal = 0
    for xVal in range(0,gx.shape[0]):
        initYVal = 0
        for yVal in range(0,gx.shape[1]):
            finalFinalImage[initXVal][initYVal] = math.sqrt((gx[initXVal][initYVal]**2) + (gy[initXVal][initYVal]**2))
            initYVal += 1
        initXVal += 1
        print(f"Sobel: {round(100*initXVal/gx.shape[0],2)}% Complete")       
    return finalFinalImage
           
        
gaussianBlur = [[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]]
sk = [[1,1,1],[1,1,1],[1,1,1]]
#Convert provided image to greyscale
greyscalematrix = greyscaleConverter(variable)
# take the greyscale image and blur it using gaussian blur function and then normalize it
blurred = convolution(greyscalematrix,gaussianBlur,9)
# run the threshold function on the blurred image with a provided threshold
th = thresh(blurred, 0.9)
finalFinalImage = edgeDetect(th,sk)
#run the sobel operator on the blurred image
# finalFinalImage = sobel(th)      
#show the final image. Make sure matplot interprets the image in greyscale (0-1) format, instead of RGB (0-255,0-255,0-255)  
plt.imshow(finalFinalImage, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
# Show the plot
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