from traffic import *

import itertools

images, labels = load_data("gtsrb")

for image, label in itertools.islice(zip(images, labels), 4):
    print(label, image)