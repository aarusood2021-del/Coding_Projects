import matplotlib.pyplot as plt
import numpy as np

def main():
    im = loadImage('300_26a_big-vlt-s.jpg')
    (im,Dphi,mask) = opticalSystem(im,300)
    Image,errors = gerchbergSaxton(im,10,Dphi,mask)
    saveFrames(Image,errors)

# loadImage() only takes in one argument, name, and loads the jpg image with that name
# and then returns it in the form of an array of floats.

def loadImage(name):
    im = plt.imread(name)/255
    if len(im.shape) > 2:
        im = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3
    im[im < 0] = 0
    im[im > 1] = 1
    return im

# opticalSystem() takes in the arguments im and width and is then used to compute
# and return Dphi, which is the True phase aberration in the pupil plane of the -
# coronagraph. The program was modified to accept a third argument, mask, which it-
# obtains by calling the occultCircle function. It returns three arguments in total
# the im, dphi and the mask.

def opticalSystem(im,width):
    im,mask = occultCircle(im,width)
    (IMa,IMp) = dft2(im)
    rng = np.random.default_rng(12345)
    imR = rng.random(im.shape)
    (_,Dphi) = dft2(imR)
    im = idft2(IMa,IMp-Dphi)
    return (im,Dphi,mask)

# gerchbergSaxton() is a function that is used to correct the aberration of the phase.
# First the df2 function is called with im(grayscale image) being called as the argument and 
# the df2 function returns the value of the Amplitude and the phase(in radians) which is
# then stored in IMa and IMp respectively. The error is the sum total of the 
# squared values of im entries.

def gerchbergSaxton(im,maxIters,dphi,mask):
    (IMa,IMp) = dft2(im)
    Image = []
    errors=[]
    for k in range(maxIters+1):
        im = idft2(IMa,IMp + (k/maxIters)*dphi)
        error1=occultError(im,mask)
        Image.append(im)
        errors.append(error1)
    return Image,errors

# (IMa,IMp) = dft2(im) returns the amplitude, IMa, and phase, IMp, of the
# 2D discrete Fourier transform of a grayscale image, im. The image, a 2D
# array, must have entries between 0 and 1. The phase is in radians.
def dft2(im):
    IM = np.fft.rfft2(im)
    IMa = np.abs(IM)
    IMp = np.angle(IM)
    return (IMa,IMp)

# im = idft2(IMa,IMp) returns a grayscale image, im, with entries between
# 0 and 1 that is the inverse 2D discrete Fourier transform (DFT) of a 2D
# DFT specified by its amplitude, IMa, and phase, IMp, in radians.
def idft2(IMa,IMp):
    IM = IMa*(np.cos(IMp)+1j*np.sin(IMp))
    im = np.fft.irfft2(IM)
    im[im < 0] = 0
    im[im > 1] = 1
    return im

# The occultCircle() function takes in the argument, im and width, in which the width enables a darkening
# circle to form in the middle. We also modified this function to return mask, a second argument,
# that is a 2D Numpy array of boolean entries.

def occultCircle(im,width):
    [length1,width1]=np.shape(im)
    middle_x=int(length1/2)
    middle_y=int(width1/2)
    mask=np.full(np.shape(im), False)      
    for x_coordinate in range(im.shape[0]):
        for y_coordinate in range(im.shape[1]):
            if pow(abs(x_coordinate-middle_x),2)+pow(abs(y_coordinate-middle_y),2) < pow(width/2,2):
                im[x_coordinate][y_coordinate]=0
                mask[x_coordinate][y_coordinate]=True
    return im,mask

# The occultError() function takes in the arguments, im and mask and is used to compute
# and return the sum total of the squared value of im entries 

def occultError(im,mask):
    error1=np.sum(pow(im[mask],2))
    return error1

# The saveFrames function takes in the input arguments, Image and errors, and then,
# we first add equal parts of colours of green, blue and red and then using the
# errors argument we received,we obtain the maximum error. The graph is corrected to an appropriate size
# and labels and titles are included to replicate the graph as shown in Version 2.

def saveFrames(Image,errors):
    shape = (Image[0].shape[0],Image[0].shape[1],3)
    image = np.zeros(shape,Image[0].dtype)
    maxIters = len(Image)-1
    maximum_error=np.max(errors)
    for k in range(maxIters+1):
        for i in range(3):
            image[:,:,i]= Image[k]
        plt.plot(np.arange(0,k+1),errors[:k+1],'-r')
        plt.imshow(image,extent=[0,10,0,maximum_error])
        plt.gca().set_aspect(maxIters/maximum_error)
        plt.title("Coronagraph Simulation")
        plt.xlabel("Iteration")
        plt.ylabel("Sum Square Error")
        plt.savefig('coronagraph'+str(k)+'.png')
        plt.show()

main()
