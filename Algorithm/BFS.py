from manim import *
import cv2
import numpy
from PIL import Image
import operator
import collections


class BreathFirstSearch(Scene):
    def construct(self):
        intro_text = Text("Breath First Search", font="SF Pro Display").scale(0.7)
        glowing_intro_text = self.create_glow(intro_text)
        self.play(glowing_intro_text.animate.shift(UP * 3.5))

        logo = cv2.imread("D:/Downloads/ptit-logo-circle.png")
        cv2.imwrite("ptit_logo.png", logo)
        ptit_logo_mobject = ImageMobject("ptit_logo.png").scale(0.4).move_to([-6.7, 3.6, 0])

        # Text giới thiệu góc dưới bên phải
        copyright_text = Text("STDR2024 @EIC&DSP LAB", font="SF Pro").set_color_by_gradient(RED, PINK).scale(0.2).move_to([6.2, -3.6, 0])
        creator_text = Text("Designed by Trung Kiên", font="SF Pro").set_color_by_gradient(RED, PINK).scale(0.2).move_to([6.335, -3.75, 0])


        matrix = [
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        original_map = self.create_empty_grid(10, 22, 0.5)
        original_map.move_to(ORIGIN)
        for i in range(10):
            for j in range(22):
                if matrix[i][j] == 1:
                    original_map[i][j][0].set_fill(WHITE, opacity=1)
                else:
                    original_map[i][j][0].set_fill(BLACK, opacity=0)

        start_text = Text("Start (0, 0)", font="SF Pro").scale(0.4).move_to(original_map[0][0][0].get_center() + [0, 0.7, 0])
        end_text = Text("End (0, 21)", font="SF Pro").scale(0.4).move_to(original_map[0][21][0].get_center() + [0, 0.7, 0])
        self.play(Create(original_map), FadeIn(ptit_logo_mobject), FadeIn(creator_text), FadeIn(copyright_text))
        self.play(
            Write(start_text),
            Write(end_text),
            original_map[0][0][0].animate.set_fill(YELLOW, opacity=1),
            original_map[0][21][0].animate.set_fill(YELLOW, opacity=1)
        )

        visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

        path = []
        target = (0, 21)
        self.wait(1)
        self.preprocess(matrix, original_map, visited)
        self.bfs(matrix, 0, 0, target, visited, path, original_map)

        self.wait(2)

    def preprocess(self, matrix, original_map, visited):
        self.play(original_map[0][0][0].animate.set_fill(RED, opacity=1), run_time=0.2)
        text_01 = Text("1", color=BLACK, font="SF Pro").scale(0.4).move_to(original_map[0][1][0].get_center())
        text_10 = Text("2", color=BLACK, font="SF Pro").scale(0.4).move_to(original_map[1][0][0].get_center())
        self.add(
            text_01,
            text_10
        )
        self.wait(1)
        self.wink(original_map[0][1][0], 5)
        self.play(original_map[0][1][0].animate.set_fill(RED, opacity=1), run_time=0.2)
        self.play(original_map[1][0][0].animate.set_fill(RED, opacity=1), run_time=0.2)
        self.remove(
            text_01,
            text_10
        )
        self.wait(1)

        text_02 = Text("1", color=BLACK, font="SF Pro").scale(0.4).move_to(original_map[0][2][0].get_center())
        text_11 = Text("2", color=BLACK, font="SF Pro").scale(0.4).move_to(original_map[1][1][0].get_center())

        self.add(
            text_02,
            text_11,
        )
        self.wait(1)
        self.wink(original_map[0][2][0], 5)
        self.play(original_map[0][2][0].animate.set_fill(RED, opacity=1), run_time=0.2)
        self.play(original_map[1][1][0].animate.set_fill(RED, opacity=1), run_time=0.2)
        self.remove(
            text_02,
            text_11,
        )

    def is_valid(self, x, y, visited, matrix):
        return x >= 0 and y >= 0 and x < len(matrix) and y < len(matrix[0]) and not visited[x][y] and matrix[x][y] == 1

    def bfs(self, matrix, i, j, target, visited, path, original_map):
        dx = [-1, 0, 0, 1]
        dy = [0, -1, 1, 0]

        queue = collections.deque()
        queue.append([i, j])
        visited[i][j] = True

        while queue:
            current = queue.popleft()
            i, j = current
            self.play(original_map[i][j][0].animate.set_fill(RED, opacity=1), run_time=0.2)
            if (i, j) == target:
                self.wink(original_map[i][j][0], 10)
                self.play(original_map[i][j][0].animate.set_fill(RED, opacity=1), run_time=0.2)
                break

            for k in range(4):
                x = i + dx[k]
                y = j + dy[k]

                if self.is_valid(x, y, visited, matrix):
                    queue.append([x, y])
                    visited[x][y] = True
                    path.append([x, y])
    
    
    def wink(self, mobject, times):
        for i in range(times):
            self.play(mobject.animate.set_fill(RED, opacity=1), run_time=0.2)
            self.play(mobject.animate.set_fill(WHITE, opacity=1), run_time=0.2)

    def create_overlay(self, width, height, overlay_color, original_image, start_x, start_y):

        overlay = Rectangle(
            width=width,
            height=height,
            color=overlay_color,
            fill_opacity=0.5
        ).set_stroke(RED, 2)

        # Tính toán vị trí overlay
        overlay_shift = np.array([width / 2, -height / 2, 0])
        # Di chuyển overlay
        overlay.move_to(original_image.get_corner(UL) + [start_x, -start_y, 0] + overlay_shift)
        return overlay

    # Tạo lưới ma trận cho vùng ảnh được cắt
    def create_grid(self, matrix, square_size):
        grid = []

        number_of_cols = len(matrix[0])
        number_of_rows = len(matrix)
        for i in range(number_of_rows):
            row = []
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))

                number = Text(
                    str(matrix[i][j]),
                    color=WHITE,
                    font="SF Pro"
                ).scale(0.4).move_to(square.get_center())

                row.append(VGroup(square, number))
            grid.append(row)

        # Chuyển đổi grid thành VGroup
        grid_vgroup = VGroup(*[VGroup(*row) for row in grid])
        return grid_vgroup

    def create_empty_grid(self, rows, cols, square_size):
        grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                square = Square(side_length=square_size).set_stroke(BLACK, 1)
                square.move_to((j * square_size, -i * square_size, 0))

                number = Text("", color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())

                row.append(VGroup(square, number))
            grid.append(row)

        return VGroup(*[VGroup(*row) for row in grid])

    def create_glow(self, vmobject, rad=1):
        glow_group = VGroup()
        for idx in range(60):
            glowing_text = vmobject.copy()
            stroke_width = rad * (1.002**((idx/1)**2)) / 18.345
            opacity_of_glow = 0.2 - idx / 305
            glowing_text.set_stroke(width=stroke_width, opacity=opacity_of_glow)
            glowing_text.set_color_by_gradient(BLUE, PINK, RED, YELLOW)
            glow_group.add(glowing_text)
        glow_group.add(vmobject)
        return glow_group
