"""
This script compares the different ways to open an image file using Python. First, the classical approach of
using the Pillow `PIL` library is demonstrated. Then, the ImageIO `imageio` library is used to read an image file.
Finally, the OpenCV `cv2` library is used to read an image file. The script will display the image using the
`cv2` library.
"""

# First, create a pathlib Path object ot deal with file path of the image, the image was manually extracted from the
# 'Cubo.zip' file, thus it is placed in the 'data/tmp' directory:
from pathlib import Path
#image_path = Path('data/tmp/Cubo05.png')
#image_path = Path('data/tmp/homer.gif')
image_path = Path('data/tmp/test.bmp')

# Use the method `open` from the `Image` class from the `PIL` library to open the image file:
from PIL import Image
image_pil = Image.open(image_path)

# Display the image using the `show` method from the `Image` class, notice this will open an external window
# with the image using the default image viewer of the OS:
image_pil.show()

# Use the method `imread` from the `imageio` library to open the image file:
import imageio as iio
image_arr = iio.v2.imread(image_path)

# Display the image using matplotlib as the image is no longer an object "Image" but a "np.array" object:
import matplotlib.pyplot as plt
plt.ion()
plt.imshow(image_arr)

# Finally, use the method `imread` from the `cv2` library to open the image file:
import cv2
image_cv2 = cv2.imread(str(image_path))

# Display the image, using the `imshow` method from the `cv2` library, notice that the image will be displayed
# in a window using the `cv2` library. This windows needs to be closed manually:
while True:
    cv2.imshow('cv2', image_arr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Furthermore, we can notice that `cv2.imread` also returns an array, thus we can use the `cv2.imshow` method
# to display the imageio array as well, and we can use the `plt.imshow` method to display the `cv2` array as well:
plt.imshow(image_cv2)

# However, notice the image will be inverted, this is because the `cv2` library reads the image in the BGR format,
# thus we need to convert it to the RGB format using the `cvtColor` method from the `cv2` library:
image_cv2_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
plt.imshow(image_cv2_rgb)

