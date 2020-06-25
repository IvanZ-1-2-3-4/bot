import matplotlib.pyplot as plt

def max_acc(m):
    return acc(knife_matrix(m))

def knife_matrix(m):
    import numpy as np
    out = []
    for i in range(m):
        row = np.array([])
        if i % 2 == 0: row = [0 for j in range(m)]
        else: row = [1 for j in range(m)]
        out.append(row)
    return np.array(out)

def acc(im):
    acutance = 0
    # print(im.shape)
    w = im.shape[0]
    l = im.shape[1]
    for row in range(len(im)):
        for col in range(len(im[row])): # For each pixel
            local_acutance = 0
            ref = im[row][col] # Magnitude of value current pixel, reference value

            for i in [row-1, row, row+1]:
                for j in [col-1, col, col+1]:
                    if not ( (i < 0) or (i > w - 1) or (j < 0) or (j > l - 1) or (i == row and j == col) ):
                        # These for loops and if statement go through all the row, col coordinates of the neighboring pixels
                        local_acutance += abs(ref - im[i][j])
            acutance += local_acutance
    return acutance
data = []
accut = lambda m: 6*(m**2)-(10*m)+4



import numpy as np
from skimage import io
from skimage.color import rgb2gray


image = io.imread('images/net_images_whole/355.png')
rgb2gray_image = rgb2gray(image)
countc = 0
countr = 0

w = image.shape[0] # Width
l = image.shape[1] # Length
#print(count)

r = int(0.05 * (w + l) / 2) # Radius is proportional to average of height and width.
for row in range(len(image)):
    if countr % int(r/3) == 0:
        for col in range(len(image[row])):
            if countc % int(r/3) == 0:
                region = image[
                    max(0, row - r) : min(w - 1, row + r), # Ensures that indices are within range.
                    max(0, col - r) : min(l - 1, col + r)
                ]
                avg_gradient = np.mean(
                    np.gradient(
                        np.sort(
                            rgb2gray_image.flatten()
                        )
                    )
                )
                plt.imshow(region)
                plt.show()
                plt.clf()
                plt.plot(np.sort(
                            rgb2gray_image.flatten()
                        )
                    )
                plt.show()
                region = region * (1 + avg_gradient*100)
                image[
                    max(0, row - r) : min(w - 1, row + r), # Ensures that indices are within range.
                    max(0, col - r) : min(l - 1, col + r)
                ] = region
            countc+=1
            print(f'countc{countc}')
    countr+=1 
    print(f'countr{countc}')
plt.imshow(image)
plt.show()