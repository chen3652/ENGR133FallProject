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
	[x] understand the assignment expectations without
		telling me how they will approach it.
	[x] understand different ways to think about a solution
		without helping me plan my solution.
	[x] think through the meaning of a specific error or
		bug present in my code without looking at my code.
	Note that if you helped somebody else with their code, you
	have to list that person as a contributor here as well.
===============================================================================
'''
# First, import all of the required packages/modules from numpy and matplot
import numpy as np # needed for dot product image padding
import matplotlib as lib # needed for importing the image and converting it into a matrix
import matplotlib.pyplot as plt # needed for displaying and saving the generated image
import sys
#Get the name of the file to run the image processing on.
file_name = input("filename: ") #takes in a picture from the user who inputs the name of a file
# Try to open the file and read it into a matrix
try:
    variable = lib.image.imread(file_name) #matplot will read the image into an array
# If the file can't be found
except FileNotFoundError:
    # Print a nice error message and end the program
    print("Sorry, I couldn't find that file in this directory!")
    #End the program:
    sys.exit()  
# Get a threshold value from the user and convert to float
try:
    threshold = float(input("Please input the threshold for determining edges on a scale of 0-1: ")) #matplot will read the image into an array
# If the value isn't a float or another error occurscoins.png

except:
    # Print a nice error message and end the program
    print("Sorry, I couldn't find a number in that!")
    #End the program:
    sys.exit()  
# Check to see if threshold is in an appropriate range
if (threshold > 1 or threshold < 0):
    print("Sorry, please input a number between 0 and 1.")
    #End the program:
    sys.exit()  
#Define a function that will convert the image to greyscale
def greyscaleConverter(colorMatrix): #dotproduct will convert image into greyscale
    dot = np.dot(colorMatrix[...,:3], [0.2126, 0.7152, 0.0722]) #Formula for converting into greyscale, takes each term and calculates dotproduct
    return dot #returns dot product
#define a function to generally convolutean image and a matrix, and then normalize it with a "divisible" factor
def convolution(imageMatrix, convoluteMatrix, divisible):
    # First, determine how much to pad the original image by. If the convolution matrix is 3x3, pad by 1 pixel so that no error is thrown
    pad_length = (len(convoluteMatrix[0])-1)/2
    # Actually pad the image with the appropriate amounts of black pixels
    paddedImage = np.pad(imageMatrix, int(pad_length), mode="constant")
    # initialize for loop variables: finalImage is the modified edge-detected image    
    finalImage = imageMatrix
    #set the initial counter position to the position of the actual image within the padded image
    tx = int(pad_length)
    ty = int(pad_length)
    # begin for loop for each pixel in Image
    for row in imageMatrix:
        for pixel in row:
            # initialize kernel to the size of the convulte Matrix
            kernel = convoluteMatrix
            # initialize internal kernel counter to size of kernel (the number that was padded up above)
            x=-int(pad_length)
            y=-int(pad_length)
            # put in a try-catch block to go to the next row of the image's kernel after the row is fully calculated
            try:
                # Generate a kernel: For each pixel in the kernel's image
                for krow in range(0,len(convoluteMatrix)):
                    for kpixel in range(0,len(convoluteMatrix)):
                        # make a kernel out of the appropriate pixels from the padded image
                        kernel[x][y] = paddedImage[tx+x][ty+y]
                        # Increment the kernel pixel counter
                        x = x + 1
                    # increment the kernel's row counter
                    y = y + 1
                    # At the end of each row, re-initialize the position of the pixel (column) to the start of the kernel
                    x=-int(pad_length) 
                # Set the sum of all of the dot products equal to zero (initialize)    
                totalDot = 0
                # For each row in the convolute matrix
                for i in range(0, len(convoluteMatrix)):
                    # Take the dot prduct of the kernel's row and the convolute matrix's row
                    dotInitial = np.dot(kernel[i], convoluteMatrix[i])
                    # Add that dot product divided by a normalization vector to the total dot product initialized above
                    totalDot += dotInitial/divisible
                # Because this is a long function, after every row, print a completion percentage    
                print(f"{round(100*tx/imageMatrix.shape[0],2)}% Complete")
                #set the final image's corresponding pixel to the sum of the normalized dot products of the kernel and convolute matrix
                finalImage[tx][ty] = totalDot
            except IndexError:
                #At the end of a row, break from the pixel loop and restart the row loop
                break
            # increment the pixel counter
            ty = ty + 1 
        # increment the row counter
        tx = tx + 1  
        # at the end of each row, reset the column counter to the start of the image
        ty = int(pad_length)
    # return the final image that has now had each pixel/kernel convoluted with a convolute Matrix
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
    # First, determine how much to pad the original image by. If the convolution matrix is 3x3, pad by 1 pixel so that no error is thrown
    pad_length = (len(convoluteMatrix[0])-1)/2
    # Actually pad the image with the appropriate amounts of black pixels
    paddedImage = np.pad(imageMatrix, int(pad_length), mode="constant")
    # initialize for loop variables: finalImage is the modified edge-detected image
    finalImage = imageMatrix
    #set the initial counter position to the position of the actual image within the padded image
    tx = int(pad_length)
    ty = int(pad_length)
    # begin for loop for each pixel in Image
    for row in imageMatrix:
        for pixel in row:
            # initialize internal kernel counter to size of kernel (the number that was padded up above)
            x=-int(pad_length)
            y=-int(pad_length)
            #initialize the counter that counts how many 1s and 0s are in each kernel of the image
            oneValue = 0
            zeroValue = 0
            # put in a try-catch block to go to the next row of the image's kernel after the row is fully calculated
            try:
                # For each pixel in the kernel's image
                for krow in range(0,len(convoluteMatrix)):
                    for kpixel in range(0,len(convoluteMatrix)):
                        #If the kernel's pixel == 1, increment the counter for 1
                        if(paddedImage[tx+x][ty+y] == 1):
                            oneValue += 1
                        #If the kernel's pixel == 0, increment the counter for 0
                        elif(paddedImage[tx+x][ty+y] == 0):
                            zeroValue += 1
                        # Increment the kernel pixel counter
                        x = x + 1
                    # increment the kernel's row counter
                    y = y + 1
                    # At the end of each row, re-initialize the position of the pixel (column) to the start of the kernel
                    x=-int(pad_length)   
                # if the majority of the kernel's pixels are "1", set the pixel in the main image to white "1"
                if(5 <= oneValue <= 7):
                    finalImage[tx][ty] = 1
                # otherwise, set the rest of the image's pixels to black "0"
                else:
                    finalImage[tx][ty] = 0
                # Because this is a long function, after every row, print a completion percentage
                print(f"Edge Detection: {round(100*tx/imageMatrix.shape[0],2)}% Complete")
            except IndexError:
                #At the end of a row, break from the pixel loop and restart the row loop
                break
            # increment the pixel counter
            ty = ty + 1 
        # increment the row counter
        tx = tx + 1  
        # at the end of each row, reset the column counter to the start of the image
        ty = int(pad_length)
    # return the final image that now has edge detection applied to it
    return finalImage
# Gaussian blur matrix for convolution
gaussianBlur = [[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]]
# A blank 3x3 matrix. Values will never be used, only size during edge detection
sk = [[1,1,1],[1,1,1],[1,1,1]]
#Convert provided image to greyscale
greyscalematrix = greyscaleConverter(variable)
# take the greyscale image and blur it using gaussian blur function and then normalize it
blurred = convolution(greyscalematrix,gaussianBlur,9)
# run the threshold function on the blurred image with a provided threshold
th = thresh(blurred, threshold)
# Run edge detection on threshold image
finalFinalImage = edgeDetect(th,sk)  
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