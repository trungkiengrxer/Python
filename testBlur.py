from manim import *
from PIL import Image
import numpy
import cv2


def box_blur(file, r=1, steps=10):
    img = Image.open(file).convert('RGB')
    img_array = numpy.array(img)
    height, width, _ = img_array.shape
    area = (2 * r + 1) ** 2

    for step in range(steps):
        new_img_array = img_array.copy()
        for x in range(r, width - r):
            for y in range(r, height - r):
                sum_pixels = numpy.sum(img_array[y-r:y+r+1, x-r:x+r+1], axis=(0, 1))
                new_img_array[y, x] = sum_pixels // area
        img_array = new_img_array
        cv2.imwrite(f"blur_step_{step}.png", cv2.cvtColor(new_img_array, cv2.COLOR_RGB2BGR))


box_blur("D:/Downloads/Lenna_(test_image).png", 5, 10)


class BlurAnimation(Scene):
    def construct(self):
        images = [ImageMobject(f"blur_step_{i}.png") for i in range(10)]
        for img in images:
            img.scale(2.5)  # Scale the image to fit the scene

        self.play(FadeIn(images[0]))
        for i in range(1, len(images)):
            self.play(Transform(images[i-1], images[i]), run_time=0.5)
        self.wait(2)


if __name__ == "__main__":
    from manim import config
    config.media_width = "100%"
    config.verbosity = "WARNING"
    scene = BlurAnimation()
    scene.render()
