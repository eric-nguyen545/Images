import copy

#If you're not sure how to start, look at the swap_red_blue and blur
#examples below.

#Problem A: Invert Colors
def invert(img_matrix):
    '''
    Purpose:
      Inverts the colors in an image by setting each color component to
      255 minus its original value.
    Input Parameter(s):
      A 3D matrix (list of lists of lists) representing an .bmp image
      Each element of the matrix represents one row of pixels in the image
      Each element of a row represents a single pixel in the image
      Each pixel is represented by a list of three numbers between 0 and 255
      in the order [red, green, blue]
    Return Value:
      A 3D matrix of the same dimensions, with the colors of each pixel inverted
    '''
    height = len(img_matrix)
    width = len(img_matrix[0])
    for y in range(height):
        for x in range(width):
          img_matrix[y][x][0] = 255 - img_matrix[y][x][0]
          img_matrix[y][x][1] = 255 - img_matrix[y][x][1]
          img_matrix[y][x][2] = 255 - img_matrix[y][x][2]
    return img_matrix



#Problem B: Sepia Filter
def sepia(img_matrix):
    '''
    Purpose:
      Applies a sepia filter to each pixel using the formulas:
      newred = red * .39 + green * .75 + blue * .19
      newgreen = red * .35 + green * .69 + blue * .17
      newblue  = red * .27 + green * .51 + blue * .13
    Input Parameter(s):
      (see invert)
    Return Value:
      A 3D matrix of the same dimensions, with the pixels converted to sepia.
    '''
    height = len(img_matrix)
    width = len(img_matrix[0])
    for y in range(height):
        for x in range(width):
            old_red = img_matrix[y][x][0]
            old_green = img_matrix[y][x][1]
            old_blue = img_matrix[y][x][2]

            newred = old_red * .39 + old_green * .75 + old_blue * .19
            newgreen = old_red * .35 + old_green * .69 + old_blue * .17
            newblue  = old_red * .27 + old_green * .51 + old_blue * .13

            if newred > 255:
                newred = 255
                if newgreen > 255:
                    newgreen = 255
                    if newblue > 255:
                      newblue = 255

            img_matrix[y][x][0] = int(newred)
            img_matrix[y][x][1] = int(newgreen)
            img_matrix[y][x][2] = int(newblue)
    return img_matrix


#Problem C: Mirror
def mirror(img_matrix):
    '''
    Purpose:
      Overwrites the right half of an image with a mirror image of the
      left half of the image.
    Input Parameter(s):
      (see invert)
    Return Value:
      A 3D matrix of the same dimensions, mirrored horizontally.
    '''
    height = len(img_matrix)
    width = len(img_matrix[0])
    new_mirror = copy.deepcopy(img_matrix)
    for y in range(height):
        for x in range(width // 2):
            new_mirror[y][-(x + 1)] = img_matrix[y][x]
    return new_mirror            

#Problem D: Your Own Filter
def custom_filter(img_matrix):
    '''
    Purpose:
      Clear the image and create a solid white rectangle
    Input Parameter(s):
      (see invert)
    Return Value:
      A 3D matrix of the same dimensions as img_matrix,
      with changes as described in the purpose section.
    '''
    height = len(img_matrix)
    width = len(img_matrix[0])
    for y in range(height):
        for x in range(width):
          img_matrix[y][x][0] = 255
          img_matrix[y][x][1] = 255
          img_matrix[y][x][2] = 255
    return img_matrix


#Example #1: Swapping red and blue components
def swap_red_blue(img_matrix):
    '''
    Purpose:
      Swaps the red and blue components in an image
    Input Parameter(s):
      (see invert)
    Return Value:
      A 3D matrix of the same dimensions, with all colors inverted
      (that is, for every pixel list, the first and last values have been
      swapped.
    '''
    height = len(img_matrix)  #Height = # of rows, i.e. length of matrix
    width = len(img_matrix[0]) #Width = # of columns, i.e. length of one row
    for y in range(height):
        for x in range(width):
            # img_matrix[y][x] is a 3-element list representing the
            # [red, green, blue] values for the pixel at coordinates (x, y)
            old_red = img_matrix[y][x][0]
            old_blue = img_matrix[y][x][2]
            img_matrix[y][x][0] = old_blue
            img_matrix[y][x][2] = old_red
    return img_matrix


#Example #2: Blur the image
#(this is a little more complex than the ones you need to do)
def blur(img_matrix):
    '''
    Purpose:
      Blurs an image by applying a 3x3 pixel filter
    Input Parameter(s):
      (see invert)
    Return Value:
      A 3D matrix of the same dimensions, with each pixel blurred:
      each color component is averaged with the surrounding 9 pixels
    '''
    height = len(img_matrix)
    width = len(img_matrix[0])
    #Make a deep copy of the matrix to use as our output matrix.
    #This is just a convenient way to get an output matrix of the same
    #dimensions as the original.
    new_matrix = copy.deepcopy(img_matrix)

    #Loops through every pixel we need to compute via (x, y) coordinates
    for y in range(height):
        for x in range(width):

            #To compute each pixel, for each of the three color components
            #take the average of that component for the surrounding 9 pixels
            new_pixel = [0, 0, 0]
            for j in range(-1,2):  #Loop through y-1, y, y+1
                for i in range(-1,2):  #Loop through x-1, x, x+1
                    for color in range(3):
                        #If x+i or y+j is out of bounds, ignore it
                        if 0 <= x+i < width and 0 <= y+j < height:
                            new_pixel[color] += img_matrix[y+j][x+i][color]/9

            #Averaging might result in a float, so truncate down to nearest int
            for color in range(3):
                new_pixel[color] = int(new_pixel[color])

            #Replace pixel in output matrix
            new_matrix[y][x] = new_pixel
    return new_matrix  



#--------------------------------------------------
# DO NOT EDIT ANYTHING BELOW THIS LINE
# .bmp file manipulation functions.  You don't have to understand these.
#--------------------------------------------------

def big_end_to_int(ls):
    '''
    Byte conversion helper 
    Purpose:
      Compute the integer represented by a sequence of bytes
    Input Parameter(s):
      A list of bytes (integers between 0 and 255), in big-endian order
    Return Value:
      Integer value that the bytes represent
    '''
    total = 0
    for ele in ls[::-1]:
        total *= 256
        total += ele
    return total

def transform_image(fname,operation):
    '''
    .bmp conversion function
    Purpose:
      Turns a .bmp file into a matrix of pixel values, performs an operation
      on it, and then converts it back into a new .bmp file
    Input Parameter(s):
      fname, a string representing a file name in the current directory
      operation, a string representing the operation to be performed on the
      image. 
    Return Value:
      None
    '''
    #Open file in read bytes mode, get bytes specifying width/height
    fp = open(fname,'rb')
    data = list(fp.read())
    old_data = list(data)
    width = big_end_to_int(data[18:22])
    height = big_end_to_int(data[22:26])

    #Data starts at byte 54.  Create matrix of pixels, where each
    #pixel is a 3 element list [red,green,blue].
    #Starts in lower left corner of image.
    i = 54
    matrix = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel = [data[i+2],data[i+1],data[i]]
            i += 3
            row.append(pixel)
        matrix.append(row)
        #Row size must be divisible by 4, otherwise padding occurs
        i += (2-i)%4
    fp.close()

    #Perform operation on the pixel matrix
    if operation == 'invert':
        new_matrix = invert(matrix[::-1])
    elif operation == 'sepia':
        new_matrix = sepia(matrix[::-1])
    elif operation == 'custom_filter':
        new_matrix = custom_filter(matrix[::-1])
    elif operation == 'mirror':
        new_matrix = mirror(matrix[::-1])
    elif operation == 'blur':
        new_matrix = blur(matrix[::-1])
    elif operation == 'swap_red_blue':
        new_matrix = swap_red_blue(matrix[::-1])
    else:
        return
    new_matrix = new_matrix[::-1]
    #Write back to new .bmp file.
    #New file name is operation+fname
    i = 54
    for y in range(height):
        for x in range(width):
            pixel = tuple(new_matrix[y][x])
            data[i+2],data[i+1],data[i] = pixel
            i += 3
        i += (2-i)%4
    fp = open(operation+"_"+fname,'wb')
    fp.write(bytearray(data))
    fp.close()


