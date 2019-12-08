import numpy as np
import collections
import matplotlib.pyplot as plt

with open('input.txt') as f:
    input_code = [int(s) for s in f.read()[:-1]]

class Image:
    
    '''
    Image object is an image with n layers. 
    '''
    
    def __init__(self, input_values, layer_shape):
        
        self.input_values = input_values #Pixel values (list or array)
        self.layer_shape = layer_shape #2D shape tuple
        
        self.pix_per_layer = self.layer_shape[0]*self.layer_shape[1]
        
        self.n_layers = len(self.input_values)/self.pix_per_layer
        
        try:
            assert self.n_layers % 1 == 0 #Has to be a whole number
        except:
            raise Exception('Incomplete input data or incorrect pixel size, cannot create image.')
            return None
        
        self.image_shape =(int(self.n_layers), self.layer_shape[0], self.layer_shape[1])
        
    def create_image(self):
        
        '''
        Create the image by filling the layers using the input values.
        '''
        
        self.image = np.zeros(self.image_shape)
        
        pix_start = 0
        pix_end = pix_start+self.pix_per_layer

        self.layer_counts = [] #Store element counts in each layer

        for l in range(int(self.n_layers)): #Fill layer by layer
            
            self.image[l] =  np.array(self.input_values[pix_start:pix_end]).reshape((6,25))

            pix_start = pix_end
            pix_end = pix_end+self.pix_per_layer

            element_count = collections.Counter(self.image[l].flatten()) #Count elements in each layer
            self.layer_counts.append(element_count)
            
    def find_lowest(self, pix_value):
        
        '''
        Find layer with lowest number of 'pix_value'
        '''
        
        lowest_layer = 0 #Set first layer to be lowest layer for now
        lowest_amount = self.layer_counts[lowest_layer][pix_value]
        
        for i, c in enumerate(self.layer_counts): #loop through element count of each layer
            
            if c[pix_value] < lowest_amount:
                lowest_amount = c[pix_value]
                lowest_layer = i
        
        return lowest_layer, lowest_amount
    
    def color_image(self):
        
        '''
        Create the color image.
        0 = black
        1 = white
        2 = transparent
        A pixel is either black or white. Transparent pixels in layers in front of it do not count.
        Essentially dimension reduction.
        '''
        
        self.pixel_colors = np.zeros((self.image.shape[1],self.image.shape[2]))
        
        for i in range(self.image.shape[1]): #loop through 2D image 
            for j in range(self.image.shape[2]):
                #For every pixel (with all layers) take first layer that contains non-transparent pixel (so not '2')
                self.pixel_colors[i,j] = self.image[:,i,j][self.image[:,i,j] != 2][0] 


if __name__ == "__main__":

    im = Image(input_code, (6,25))
    im.create_image()

    lowest_zero_layer, lowest_zero_amount = im.find_lowest(0)

    answer = im.layer_counts[lowest_zero_layer][1] * im.layer_counts[lowest_zero_layer][2]
    print('Answer to part 1 is: {}'.format(answer))

    #Part 2
    test.color_image()
    plt.imshow(test.pixel_colors)