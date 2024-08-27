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

    # Create a grayscale image using a balanced average of the color channels:
    im_gray = im @ [0.22, 0.72, 0.06]

    # Add noise to the image:
    noise = np.random.random(im_gray.shape)
    noise_95 = noise > 0.95
    im_noisy = im_gray.copy()
    im_noisy[noise_95] = 255

    noise_05 = noise < 0.05
    im_noisy[noise_05] = 0

    # Display the original, grayscale, and noisy images:
    fig, axes = plt.subplots(1, 3, sharey=True, sharex=True)
    axes[0].imshow(im)
    axes[1].imshow(im_gray, cmap='gray')
    axes[2].imshow(im_noisy, cmap='gray')

    # 1. Average filters
    # TODO it is important to use the `cv2.filter2D` for the course to learn about the kernel configurations,
    #  please do avoid using other methods to apply the filter, such as `cv2.blur` or `cv2.boxFilter`. This is
    #   also true for next examples.
    # 1.1. 3x3 kernel size
    # We will use the OpenCV framework to apply a kernel to the image:
    kernel = np.ones((3, 3)) / 9
    im_avg = cv2.filter2D(im_noisy, -1, kernel)

    # Display the original and filtered images:
    fig, axes = plt.subplots(1, 2, sharey=True, sharex=True)
    axes[0].imshow(im_noisy, cmap='gray')
    axes[1].imshow(im_avg, cmap='gray')
    plt.show()

    # 1.2. 9x9 kernel size
    # Increasing the kernel size will increase the blurring effect in the image, but will reduce the noise:
    kernel = np.ones((9, 9)) / 25
    im_avg = cv2.filter2D(im_noisy, -1, kernel)

    # Display the original and filtered images:
    fig, axes = plt.subplots(1, 2, sharey=True, sharex=True)
    axes[0].imshow(im_noisy, cmap='gray')
    axes[1].imshow(im_avg, cmap='gray')
    plt.show()

    # 1.3. Gaussian filter
    # The Gaussian filter is a more sophisticated filter that applies a kernel with a
    # Gaussian distribution to the image:
    kernel = cv2.getGaussianKernel(3, 1)
    im_gaussian = cv2.filter2D(im_noisy, -1, kernel @ kernel.T)

    # Display the original and filtered images:
    fig, axes = plt.subplots(1, 2, sharey=True, sharex=True)
    axes[0].imshow(im_noisy, cmap='gray')
    axes[1].imshow(im_gaussian, cmap='gray')
    plt.show()

    # TODO create your own function to define the kernel and apply the filter to the image.

    # 2. Gradient filters
    # Kernels can be constructed to as way to implement discrete derivatives of the image, this
    # can be used to detect edges in the image:
    # 2.1. Sobel filter
    # Horizontal edge detection:
    kernel = np.array(
        [[-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]]
    )
    im_sobel_x = cv2.filter2D(im_gray, -1, kernel)

    # Edge detection using absolute and thresholding:
    im_sobel_x = np.abs(im_sobel_x) > 127

    # Vertical edge detection:
    kernel = np.array(
        [[1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]]
    )
    im_sobel_y = cv2.filter2D(im_gray, -1, kernel)

    # Edge detection using absolute and thresholding:
    im_sobel_y = np.abs(im_sobel_y) > 127

    # Display the original and filtered images:
    fig, axes = plt.subplots(1, 3, sharey=True, sharex=True)
    axes[0].imshow(im_gray, cmap='gray')
    axes[1].imshow(im_sobel_x, cmap='gray')
    axes[2].imshow(im_sobel_y, cmap='gray')

    # 2.3. Laplacian filter
    # The Laplacian filter is a second derivative filter that can be used to detect edges in the image:
    kernel = np.array(
        [[0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]]
    )
    im_laplacian = cv2.filter2D(im_gray, -1, kernel)

    # Edge detection using square and thresholding:
    im_laplacian = im_laplacian ** 2
    im_laplacian = (im_laplacian/im_laplacian.max()) > 0.01

    # Display the original and filtered images:
    fig, axes = plt.subplots(1, 2, sharey=True, sharex=True)
    axes[0].imshow(im_gray, cmap='gray')
    axes[1].imshow(im_laplacian, cmap='gray')
    plt.show()

    # TODO study morphological operations to improve the edge detection. 












