from manim import *

class MyFirstScene(Scene):
    def construct(self):
        text = Text("Hello, Manim!")  # Tạo văn bản
        self.play(Write(text))        # Hoạt ảnh viết văn bản lên màn hình
        self.wait(2)                  # Chờ 2 giây
