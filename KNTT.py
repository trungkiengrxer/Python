from manim import *
import random

list = [random.randint(1, 100) for i in range(10)]
mainTarget = random.choice(list)


class LinearSearch(Scene):
    def construct(self):
        # Tạo một mảng số
        array = list
        target = mainTarget  # Phần tử cần tìm

        # Hiển thị mảng dưới dạng các ô vuông


        # Hiển thị thông tin ban đầu
        array_text = Text("ẢNH HƯỞNG TÍCH CỰC CỦA AI", font="SF Pro", font_size=70)
        array_text.set_color_by_gradient(RED, LIGHT_PINK)

        # Thêm tất cả các phần tử vào Scene
        self.play(array_text.animate.shift(UP * 2.2))
     