"""
This script demonstrate examples of color filters using Python. Several filters are applied to the image using the
`numpy` libraries. The filters are the negative filter, the grayscale filter, the HSV filter, and the threshold filter.

Some exercises are proposed to the user to create their own filters and apply them to the image.
"""
# Import dependencies from third-party libraries:
import cv2
import numpy as np
from scipy.datasets import face
import matplotlib.pyplot as plt

# Set the matplotlib to interactive mode:
plt.ion()


if __name__ == '__main__':
    # Load the image using the `face` method from the `scipy.misc` library:
    im = face()

    # Display the image using the `imshow` method from the `matplotlib.pyplot` library:
    fig0, ax0 = plt.subplots()
    ax0.imshow(im)

    # 1. Negative filter
    im_max = 255
    im_neg = im_max - im

    # Display both images comparing them:
    fig1, axes1 = plt.subplots(1, 2, sharey=True, sharex=True)
    axes1[0].imshow(im)
    axes1[1].imshow(im_neg)

    # Linear transforms:
    # 2.1. Grayscale filter
    im_gray = np.mean(im, axis=2)

    # 2.2. Grayscale filter using the `cmap` parameter of the `imshow` method:
    fig2, axes2 = plt.subplots(1, 3, sharey=True, sharex=True)
    axes2[0].imshow(im)
    axes2[1].imshow(im_gray)
    axes2[2].imshow(im_gray, cmap='gray')

    # 2.2.1 Another grayscale:
    # TODO read information from GIMP about the grayscale filter:
    #  https://docs.gimp.org/2.8/en/gimp-tool-desaturate.html#:~:text=In%20the%20image%20menu%20through,tool%20has%20been%20installed%20there.
    im_gray2 = np.dot(im, [0.22, 0.72, 0.06])

    # Alternatively, one could use the `@` operator to perform the dot product:
    # im_gray2 = im @ [0.22, 0.72, 0.06]

    # Display original and grayscale images:
    fig3, axes3 = plt.subplots(1, 3, sharey=True, sharex=True)
    axes3[0].imshow(im)
    axes3[1].imshow(im_gray, cmap='gray')
    axes3[2].imshow(im_gray2, cmap='gray')

    # 2.2. Sepia filter
    # Additional filters can be applied using linear transforms of the color channels:
    sepia_matrix = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131],
                             ])

    im_sepia = im @ sepia_matrix.T

    # Display the original and the sepia image:
    fig6, axes6 = plt.subplots(1, 2, sharey=True, sharex=True)
    axes6[0].imshow(im)
    axes6[1].imshow(im_sepia / 255)

    # 2.3. White-balance:
    # TODO search internet for information on white balance correction, which is the matrix to perform a
    #  white balance correction on an image?

    # 3. Non-linear transforms:
    # 3.1. HSV filter
    # TODO read documentation about the HSV color space:
    #  https://en.wikipedia.org/wiki/HSL_and_HSV
    # We will use the `cv2` library to convert the image to the HSV color space:
    im_hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HLS)

    # Display the original and the HSV image:
    fig4, axes4 = plt.subplots(1, 3, sharey=True, sharex=True)
    axes4[0].imshow(im_hsv[..., 0], cmap='gray')
    axes4[1].imshow(im_hsv[..., 2], cmap='gray')
    axes4[2].imshow(im_hsv[..., 1], cmap='gray')

    # TODO implement your own HSL and HSV filters!

    # 4. Histogram alterations
    # 4.1. Threshold filter
    # Thresholding is a useful technique to segment an image into regions of interest. We will use the HSV image to
    # create a mask of the image:
    im_hsv_0 = im_hsv[..., 0]

    # Create a mask using the hue channel:
    im_mask = im_hsv_0 > 100

    # Important, recast the mask to the original type:
    im_mask_255 = 255 * im_mask.astype("uint8")

    # Display the original and the mask:
    fig5, axes5 = plt.subplots(1, 2, sharey=True, sharex=True)
    axes5[0].imshow(im)
    axes5[1].imshow(im_mask_255, cmap='gray')

    # 4.2. Histogram equalization
    # HE often involves a non-linear transformation following a step function like a
    # an arc tangent or a sigmoid function. We will use the `cv2` library to perform the histogram equalization:
    im_gray = np.mean(im, axis=2)
    im_eq = cv2.equalizeHist(im_gray.astype("uint8"))

    # Display the original and the equalized image:
    fig6, axes6 = plt.subplots(1, 2, sharey=True, sharex=True)
    axes6[0].imshow(im_gray, cmap='gray')
    axes6[1].imshow(im_eq, cmap='gray')

    # TODO implement your own histogram equalization filter!
