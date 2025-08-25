from manim import *
import cv2
import numpy
from PIL import Image
import operator


class MaxPoolingLayer(Scene):
    def construct(self):

        # Tỷ lệ xấp xỉ giữa pixel và toạ độ trong manim
        ratio = 0.0043888888888888888

        # Tạo text giới thiệu về bộ lọc trung bình và hiển thị
        max_pooling_layer_text = Text("Max Pooling Layer", font="SF Pro Display").scale(0.7)
        glow_max_pooling_layer_text = self.create_glow(max_pooling_layer_text)

        self.play(glow_max_pooling_layer_text.animate.shift(UP * 3))

        # Đọc ảnh và chuyển sang gam màu xám
        img = cv2.imread("D:/Downloads/Lenna_(test_image).png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Logo PTIT góc trên bên trái
        logo = cv2.imread("D:/Downloads/ptit-logo-circle.png")
        cv2.imwrite("ptit_logo.png", logo)
        ptit_logo_mobject = ImageMobject("ptit_logo.png").scale(0.4).move_to([-6.7, 3.6, 0])

        # Text giới thiệu góc dưới bên phải
        copyright_text = Text("STDR2024 @EIC&DSP LAB", font="SF Pro").set_color_by_gradient(RED, PINK).scale(0.2).move_to([6.2, -3.6, 0])
        creator_text = Text("Designed by Trung Kiên", font="SF Pro").set_color_by_gradient(RED, PINK).scale(0.2).move_to([6.335, -3.75, 0])

        # Lưu ảnh đã xử lý và chuyển thành mobject
        cv2.imwrite("processed_image.jpg", img)
        original_image = ImageMobject("processed_image.jpg")

        convolution_text = Text("Calculate the convolution of the input matrix and the operator", font="SF Pro").scale(0.45).move_to(ORIGIN + [0, -2.75, 0])

        # Hiển thị ảnh gốc, logo và text
        self.play(FadeIn(original_image), FadeIn(ptit_logo_mobject), FadeIn(creator_text), FadeIn(copyright_text))
        self.play(
            original_image.animate.shift(LEFT * 5),
            FadeIn(convolution_text)
        )

        # Cắt hình ảnh có kích thước 6x6 từ vị trí (50, 50) pixel
        cropped_img = img[50:56, 50:56]

        # Chuyển các pixel sang ma trận
        matrix = numpy.array(cropped_img)

        # Kích thước mỗi ô vuông của lưới ma trận 5x5 vừa cắt
        square_size = 0.5

        # Tính toán chiều rộng và chiều cao của lớp phủ đánh dấu vùng ảnh cần cắt
        overlay_width = 6 * ratio  # 5 pixel chiều rộng
        overlay_height = 6 * ratio  # 5 pixel chiều cao

        # Điểm bắt đầu cho hiệu ứng GrowFromPoint
        grow_point = original_image.get_corner(UL) + [50 * ratio, -50 * ratio, 0]

        # Tạo lớp phủ (overlay) màu đỏ và hiển thị
        red_overlay = self.create_overlay(overlay_width, overlay_height, RED, original_image, 50 * ratio, 50 * ratio)
        self.play(FadeIn(red_overlay))

        # Tạo ma trận cho vùng ảnh cắt ra
        grid_vgroup = self.create_empty_grid(6, 6, square_size)
        grid_vgroup.next_to(original_image, RIGHT * 2)

        # Tạo đường viền đỏ phía trên làm hiệu ứng phóng to
        line1 = Line(
            start=red_overlay.get_corner(UR),
            end=grid_vgroup[0][0].get_corner(UL),
            color=RED, stroke_width=1
        )

        # Tạo đường viền đỏ phía dưới làm hiệu ứng phóng to
        line2 = Line(
            start=red_overlay.get_corner(DR),
            end=grid_vgroup[-1][0].get_corner(DL),
            color=RED, stroke_width=1
        )

        # Tạo vùng fill màu xanh dương giũa Line1 và Line2 bằng Polygon
        filled_region = Polygon(
            red_overlay.get_corner(DR),
            red_overlay.get_corner(UR),
            grid_vgroup[0].get_corner(UL),
            grid_vgroup[-1][0].get_corner(DL),
            color=BLUE, fill_opacity=0.4, stroke_opacity=0
        )

        # Hiển thị vùng fill
        self.play(
            GrowFromPoint(filled_region, point=grow_point),
            GrowFromPoint(line1, point=grow_point),
            GrowFromPoint(line2, point=grow_point),
            GrowFromPoint(grid_vgroup, point=grow_point)
        )

        grid_with_values = self.create_grid(matrix, square_size)
        grid_with_values.move_to(grow_point).scale(0.1)
        for i in range(6):
            for j in range(6):
                self.play(grid_with_values[i][j].animate.scale(10).move_to(grid_vgroup[i][j].get_center()), run_time=0.1)
                grid_vgroup[i][j] = grid_with_values[i][j]

        # Tạo lưới ma trận kernel 3x3 và fill màu xanh dương
        sobel_operator = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
        sobel_matrix = self.create_grid(sobel_operator, square_size)
        for row in sobel_matrix:
            for cell in row:
                cell[0].set_fill(BLUE, opacity=0.4)

        # Di chuyển lưới kernel 3x3 đến vị trí phù hợp và hiển thị
        sobel_matrix.move_to(grid_vgroup.get_center() + [6, 0, 0])
        self.play(GrowFromEdge(sobel_matrix, UP))

        # Tạo text đánh dấu ma trận input và kernel
        input_matrix_text = Text("Input Matrix", font="SF Pro").scale(0.45).move_to(grid_vgroup.get_center() + [0, 1.8, 0])
        sobel_text = Text("Sobel Operator", font="SF Pro").scale(0.45).move_to(sobel_matrix.get_center() + [0, 1.1, 0])

        # Cửa sổ trượt đánh dấu vùng ma trận con cần xét
        squared_window = Square(side_length=square_size * 3 + 0.25).set_stroke(BLUE, 2.5)
        squared_window.set_z_index(10)

        # Vị trí trung tâm của sobel_matrix và grid_vgroup
        sobel_matrix_position = sobel_matrix.get_center()
        grid_vgroup_position = grid_vgroup.get_center()

        # Tạo ma trận output và text
        feature_matrix = self.create_empty_grid(6, 6, square_size).move_to(grid_vgroup_position + [14, 0, 0] + ORIGIN)
        feature_matrix_text = Text(f"Feature Matrix", font="SF Pro").scale(0.45).move_to(feature_matrix.get_center() + [0, 1.8, 0])

        colors = [GREEN, BLUE, PINK, YELLOW, ORANGE]
        for i in range(1, 4, 2):
            for j in range(1, 4, 2):
                sub_feature_matrix = VGroup(*(feature_matrix[i + u][j + v] for u in range(2) for v in range(2)))
                color = colors[(i // 2) * 2 + (j // 2) % len(colors)]
                for cell in sub_feature_matrix:
                    cell[0].set_fill(color, opacity=0.4),
                    cell[0].set_stroke(color)
                sub_feature_matrix.set_z_index(10 - (i + j))


        convolved_text = Text("convolved with", font="SF Pro").scale(0.45).move_to(grid_vgroup_position + [3.5, 0, 0]).set_color_by_gradient(BLUE, PINK, RED)

        # Hiển thị text đánh dấu ma trận input và kernel
        self.play(
            GrowFromPoint(input_matrix_text, point=grid_vgroup.get_center()),
            GrowFromPoint(sobel_text, point=sobel_matrix.get_center()),
            GrowFromPoint(convolved_text, point=convolved_text.get_center()),
            GrowFromPoint(feature_matrix, point=feature_matrix.get_center()),
            GrowFromPoint(feature_matrix_text, point=feature_matrix.get_center())
        )

        self.play(ApplyWave(convolved_text, direction=RIGHT))

        # Hiển thị cửa sổ trượt và ma trận output, đồng thời scale sobel_text về 0
        self.play(
            DrawBorderThenFill(squared_window.move_to(grid_vgroup[1][1].get_center())),
            sobel_text.animate.scale(0),
            sobel_matrix.animate.move_to(grid_vgroup.get_center() + [2.75, -1, 0]),
            convolved_text.animate.scale(0),
            feature_matrix.animate.move_to(grid_vgroup_position + [5.5, 0, 0] + ORIGIN),
            feature_matrix_text.animate.move_to(grid_vgroup_position + [5.5, 0, 0] + ORIGIN + [0, 1.8, 0]),
        )

        for i in range(4):
            for j in range(4):

                # Tạo ma trận con 3x3 từ ma trận 5x5
                sub_matrix = VGroup(*[grid_vgroup[i + u][j + v] for u in range(3) for v in range(3)])

                # Lưu vị trí ban đầu của ma trận con vừa tạo
                original_position = sub_matrix.get_center()

                # Biến toàn cục đánh dấu vị trí ma trận con sau khi di chuyển
                global after_moving_sub_matrix_position

                if i == 0 and j == 0:

                    # Di chuyển ma trận con và đánh dấu vị trí sau khi di chuyển
                    self.play(sub_matrix.animate.move_to(sobel_matrix.get_center()).shift(UP * 2.5 + DOWN * 0.5))
                    after_moving_sub_matrix_position = sub_matrix.get_center()

                # Kết quả tích chập
                sum = 0

                for u in range(3):
                    for v in range(3):

                        # Phép nhân giữa ma trận con và kernel tương ứng vị trí
                        multiply = matrix[i + u][j + v] * sobel_operator[u][v]
                        # Cộng dần kết quả
                        sum += multiply

                # Kết quả sau khi chia trung bình và làm tròn

                # Tạo các text cho kết quả đầu tiên
                sum_text = Text(
                    f"Convolution = 164 x 1 + 161 x 0 + 161 x (-1) + 165 x 2 + 164 x 0 + 162 x (-2) + 161 x 1 + 162 x 0 + 164 x (-1)",
                    color=WHITE, font="SF Pro",
                ).scale(0.4).move_to(ORIGIN + [0, -2.25, 0])

                # Tạo các text cho các kết quả sau
                sum_result_text = Text(f"Convolution = {sum}", color=WHITE, font="SF Pro").scale(0.4).move_to(ORIGIN + [0, -2.25, 0])

                # Tạo text giá trị để cho vào ma trận output
                new_text = Text(f"{sum}", font="SF Pro").scale(0.4)
                new_text.move_to(feature_matrix[i + 1][j + 1][0].get_center())

                # Hiển thị các kết quả sau
                if i != 0 or j != 0:
                    if j <= 3 and i == 0:
                        # Di chuyển cửa sổ trượt và ma trận kernel đè lên đè lên các ma trận con
                        self.play(
                            squared_window.animate.move_to(grid_vgroup[i + 1][j + 1].get_center()),
                            sobel_matrix.animate.move_to(sub_matrix.get_center())
                        )

                        # Hiển thị kết quả sum và quotient
                        self.play(
                            GrowFromPoint(sum_result_text, point=sum_text.get_center()),
                        )

                        self.wait(0.5)

                        # Hiển thị kểt quả vào ma trận output và làm biến mất kết quả sum và quotient cũ
                        self.play(
                            sum_result_text.animate.scale(0),
                            GrowFromPoint(new_text, point=feature_matrix[i + 1][j + 1][0].get_center())
                        )

                    else:
                        # Di chuyển cửa sổ trượt và ma trận kernel đè lên đè lên các ma trận con
                        self.play(
                            squared_window.animate.move_to(grid_vgroup[i + 1][j + 1].get_center()),
                            sobel_matrix.animate.move_to(sub_matrix.get_center()),
                            run_time=0.1
                        )


                        # Hiển thị kểt quả vào ma trận output và làm biến mất kết quả sum và quotient cũ
                        self.play(
                            GrowFromPoint(new_text, point=feature_matrix[i + 1][j + 1][0].get_center()),
                            run_time=0.1
                        )
                # Hiển thị kết quả trường hợp đầu tiên
                else:
                    self.play(
                        sobel_matrix.animate.move_to(sub_matrix.get_center()),
                        GrowFromPoint(sum_text, point=sum_text.get_center())
                    )

                    self.wait(0.5)

                    self.play(
                        sobel_matrix.animate.shift(DOWN * 1),
                        sub_matrix.animate.shift(DOWN * 1),
                        Transform(sum_text, sum_result_text)
                    )

                    self.wait(0.75)

                    self.play(
                        sum_text.animate.scale(0),
                        GrowFromPoint(new_text, point=feature_matrix[i + 1][j + 1][0].get_center())
                    )

                if j == 3 and i != 3:
                    self.play(
                        squared_window.animate.move_to(grid_vgroup[i + 1][j - 2].get_center()),
                        sobel_matrix.animate.move_to(grid_vgroup[i + 1][j - 2].get_center()),
                        run_time=0.1
                    )

                if i == 0 and j == 0:
                    self.play((sub_matrix.animate.shift(original_position - sub_matrix.get_center())))

                # Thay thế giá trị cũ bằng giá trị mới trong feature_matrix
                feature_matrix[i + 1][j + 1][1] = new_text

        self.play(
            Unwrite(line1),
            Unwrite(line2),
            FadeOut(filled_region),
            FadeOut(red_overlay),
            Uncreate(squared_window),
            sobel_matrix.animate.scale(0),
            FadeOut(convolution_text)
        )

        explanation_text = Text("Find the maximum value in each 2 x 2 sub-matrix with strides = 2", font="SF Pro").scale(0.45).move_to(ORIGIN + [0, -2.75, 0])

        self.play(
            original_image.animate.shift(LEFT * 8),
            grid_vgroup.animate.shift(LEFT * 8),
            input_matrix_text.animate.shift(LEFT * 8),
            feature_matrix.animate.shift(LEFT * 6.5),
            feature_matrix_text.animate.shift(LEFT * 6.5),
            FadeIn(explanation_text)
        )

        output_matrix = self.create_empty_grid(2, 2, square_size).move_to(feature_matrix.get_center() + [4.5, 0, 0])
        output_matrix_text = Text("Output Matrix", font="SF Pro").scale(0.45).next_to(output_matrix, UP * 0.9)

        self.play(
            GrowFromPoint(output_matrix, point=output_matrix.get_center()),
            GrowFromPoint(output_matrix_text, point=output_matrix.get_center())
        )

        sliding_window = Square(side_length=square_size * 2 + 0.25).set_stroke(YELLOW_B, 2.5)
        sliding_window.set_z_index(10)
        starting_sub_matrix = VGroup(*(feature_matrix[1 + u][1 + v] for u in range(2) for v in range(2)))
        starting_point = starting_sub_matrix.get_center()
        self.play(DrawBorderThenFill(sliding_window.move_to(starting_sub_matrix.get_center())))

        max_text = Text("Max value: ", font="SF Pro").scale(0.4).move_to(ORIGIN + [0, -2.25, 0])
        self.play(GrowFromPoint(max_text, point=max_text.get_center()))

        for i in range(1, 4, 2):
            for j in range(1, 4, 2):
                sub_feature_matrix = VGroup(*(feature_matrix[i + u][j + v] for u in range(2) for v in range(2)))

                if i != 0 or j != 0:
                    self.play(sliding_window.animate.move_to(sub_feature_matrix.get_center()))
                max = -3
                element = None
                for u in range(2):
                    for v in range(2):
                        value = int(feature_matrix[i + u][j + v][1].text)
                        if value > max:
                            max = value
                            element = feature_matrix[i + u][j + v]
                            
                self.play(Wiggle(element, scale_value=1.4, n_wiggles=8))
                copy_element = element.copy()
                self.play(copy_element.animate.move_to(max_text.get_center() + RIGHT), run_time=0.2)
                self.wait(1)
                self.play(copy_element.animate.move_to(output_matrix[i // 2][j // 2][0].get_center()), run_time=0.2)
                output_matrix[i // 2][j // 2][1] = copy_element

            if j == 3 and i != 3:
                self.play(sliding_window.animate.move_to(starting_point))

        self.play(
            Uncreate(sliding_window),
            max_text.animate.scale(0)
        )

        self.play(
            grid_vgroup.animate.shift(RIGHT * 5.5),
            input_matrix_text.animate.shift(RIGHT * 5.5),
            feature_matrix.animate.shift(RIGHT * 2.75),
            feature_matrix_text.animate.shift(RIGHT * 2.75),
            output_matrix.animate.shift(RIGHT * 2),
            output_matrix_text.animate.shift(RIGHT * 2),
            FadeOut(explanation_text)
        )

        self.wait(2)

    # Tạo lớp phủ đánh dấu vùng ảnh cần cắt
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
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
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
