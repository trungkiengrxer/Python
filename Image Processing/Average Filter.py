from manim import *
import cv2
import numpy
from PIL import Image
import operator


class AverageFilter(Scene):
    def construct(self):

        # Tỷ lệ xấp xỉ giữa pixel và toạ độ trong manim
        ratio = 0.0043888888888888888

        # Tạo text giới thiệu về bộ lọc trung bình và hiển thị
        median_filter_text = Text("Average Filter", font="SF Pro").scale(0.7).set_color_by_gradient(RED, LIGHT_PINK)
        self.play(median_filter_text.animate.shift(UP * 3))

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

        # Hiển thị ảnh gốc, logo và text
        self.play(FadeIn(original_image), FadeIn(ptit_logo_mobject), FadeIn(creator_text), FadeIn(copyright_text))
        self.play(original_image.animate.shift(LEFT * 5))

        # Cắt hình ảnh có kích thước 5x5 từ vị trí (50, 50) pixel
        cropped_img = img[50:55, 50:55]

        # Chuyển các pixel sang ma trận
        matrix = numpy.array(cropped_img)

        # Kích thước mỗi ô vuông của lưới ma trận 5x5 vừa cắt
        square_size = 0.5

        # Tính toán chiều rộng và chiều cao của lớp phủ đánh dấu vùng ảnh cần cắt
        overlay_width = 5 * ratio  # 5 pixel chiều rộng
        overlay_height = 5 * ratio  # 5 pixel chiều cao

        # Điểm bắt đầu cho hiệu ứng GrowFromPoint
        grow_point = original_image.get_corner(UL) + [50 * ratio, -50 * ratio, 0]

        # Tạo lớp phủ (overlay) màu đỏ và hiển thị
        red_overlay = self.create_overlay(overlay_width, overlay_height, RED, original_image, 50 * ratio, 50 * ratio)
        self.play(FadeIn(red_overlay))

        # Tạo ma trận cho vùng ảnh cắt ra
        grid_vgroup = self.create_grid(matrix, square_size)
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

        # Tạo lưới ma trận kernel 3x3 và fill màu xanh dương
        grid_kernel = self.create_grid([[1, 1, 1], [1, 1, 1], [1, 1, 1]], square_size)
        for row in grid_kernel:
            for cell in row:
                cell[0].set_fill(BLUE, opacity=0.4)

        # Di chuyển lưới kernel 3x3 đến vị trí phù hợp và hiển thị
        grid_kernel.move_to(grid_vgroup.get_center() + [2.5, -1, 0])
        self.play(GrowFromEdge(grid_kernel, UP))

        # Tạo text đánh dấu ma trận input và kernel
        matrix_text = Text("Input Matrix", font="SF Pro").scale(0.45).move_to(grid_vgroup.get_center() + [0, 1.6, 0])
        kernel_text = Text("Kernel Matrix", font="SF Pro").scale(0.45).move_to(grid_kernel.get_center() + [0, -1.1, 0])

        # Tạo ảnh mờ bằng cv2 và lưu
        blurred_image = cv2.blur(img, (3, 3))
        cv2.imwrite("blurred_image.jpg", blurred_image)

        # Cửa sổ trượt đánh dấu vùng ma trận con cần xét
        squared_window = Square(side_length=square_size * 3 + 0.25).set_stroke(BLUE, 2.5)
        squared_window.set_z_index(10)

        # Vị trí trung tâm của grid_kernel và grid_vgroup
        grid_kernel_position = grid_kernel.get_center()
        grid_vgroup_position = grid_vgroup.get_center()

        # Tạo ma trận output và text
        output_matrix = self.create_empty_grid(5, 5, square_size).move_to(grid_vgroup_position + [5, 0, 0] + ORIGIN)
        output_matrix_text = Text(f"Output Matrix", font="SF Pro").scale(0.45).move_to(output_matrix.get_center() + [0, 1.6, 0])

        # Hiển thị text đánh dấu ma trận input và kernel
        self.play(
            GrowFromPoint(matrix_text, point=grid_vgroup.get_center()),
            GrowFromPoint(kernel_text, point=grid_kernel.get_center())
        )

        # Hiển thị cửa sổ trượt và ma trận output, đồng thời scale kernel_text về 0
        self.play(
            DrawBorderThenFill(squared_window.move_to(grid_vgroup[1][1].get_center())),
            kernel_text.animate.scale(0),
            GrowFromPoint(output_matrix, point=output_matrix.get_center()),
            GrowFromPoint(output_matrix_text, point=output_matrix.get_center())
        )

        for i in range(3):
            for j in range(3):

                # Tạo ma trận con 3x3 từ ma trận 5x5
                sub_matrix = VGroup(*[grid_vgroup[i + u][j + v] for u in range(3) for v in range(3)])

                # Lưu vị trí ban đầu của ma trận con vừa tạo
                original_position = sub_matrix.get_center()

                # Biến toàn cục đánh dấu vị trí ma trận con sau khi di chuyển
                global after_moving_sub_matrix_position

                if i == 0 and j == 0:

                    # Di chuyển ma trận con và đánh dấu vị trí sau khi di chuyển
                    self.play(sub_matrix.animate.move_to(grid_kernel.get_center()).shift(UP * 2))
                    after_moving_sub_matrix_position = sub_matrix.get_center()

                # Kết quả tổng tích chập
                sum = 0

                for u in range(3):
                    for v in range(3):

                        # Phép nhân giữa ma trận con và kernel tương ứng vị trí
                        multiply = matrix[i + u][j + v] * 1
                        # Cộng dần kết quả
                        sum += multiply

                # Kết quả sau khi chia trung bình và làm tròn
                average_result = round(sum / 9.0)

                # Tạo các text cho kết quả đầu tiên
                sum_text = Text(
                    f"Sum = 164 x 1 + 161 x 1 + 161 x 1 + 165 x 1 + 164 x 1 + 162 x 1 + 161 x 1 + 162 x 1 + 164 x 1",
                    color=WHITE, font="SF Pro",
                ).scale(0.4).move_to(ORIGIN + [0, -2.25, 0])

                quotient_text_result = Text(
                    f"Average = {sum} / 9 = [162.666...] = {average_result}",
                    color=WHITE,
                    font="SF Pro"
                ).scale(0.4).move_to(ORIGIN + [0, -2.65, 0])

                # Tạo các text cho các kết quả sau
                sum_result_text = Text(f"Sum = {sum}", color=WHITE, font="SF Pro").scale(0.4).move_to(ORIGIN + [0, -2.25, 0])

                quotient_text = Text(f"Average = [{sum} / 9] = {average_result}",
                                     color=WHITE,
                                     font="SF Pro"
                                     ).scale(0.4).move_to(ORIGIN + [0, -2.65, 0])

                # Tạo text giá trị để cho vào ma trận output
                new_text = Text(str(average_result), font="SF Pro").scale(0.4)
                new_text.move_to(output_matrix[i + 1][j + 1][0].get_center())

                # Hiển thị các kết quả sau
                if i != 0 or j != 0:

                    # Di chuyển cửa sổ trượt và ma trận kernel đè lên đè lên các ma trận con
                    self.play(
                        squared_window.animate.move_to(grid_vgroup[i + 1][j + 1].get_center()),
                        grid_kernel.animate.move_to(sub_matrix.get_center())
                    )

                    # Hiển thị kết quả sum và quotient
                    self.play(
                        GrowFromPoint(sum_result_text, point=sum_text.get_center()),
                        GrowFromPoint(quotient_text, point=quotient_text.get_center())
                    )

                    self.wait(0.5)

                    # Hiển thị kểt quả vào ma trận output và làm biến mất kết quả sum và quotient cũ
                    self.play(
                        sum_result_text.animate.scale(0),
                        quotient_text.animate.scale(0),
                        GrowFromPoint(new_text, point=output_matrix[i + 1][j + 1][0].get_center())
                    )

                # Hiển thị kết quả trường hợp đầu tiên
                else:
                    self.play(
                        grid_kernel.animate.move_to(sub_matrix.get_center()),
                        GrowFromPoint(sum_text, point=sum_text.get_center())
                    )

                    self.wait(0.5)

                    self.play(
                        grid_kernel.animate.shift(DOWN * 1),
                        sub_matrix.animate.shift(DOWN * 1),
                        Transform(sum_text, sum_result_text)
                    )

                    self.wait(0.25)

                    self.play(GrowFromPoint(quotient_text_result, point=quotient_text_result.get_center()))

                    self.wait(0.5)

                    self.play(
                        quotient_text_result.animate.scale(0),
                        sum_text.animate.scale(0),
                        GrowFromPoint(new_text, point=output_matrix[i + 1][j + 1][0].get_center())
                    )

                if j == 2 and i != 2:
                    self.play(
                        squared_window.animate.move_to(grid_vgroup[i + 1][j - 1].get_center()),
                        grid_kernel.animate.move_to(grid_vgroup[i + 1][j - 1].get_center())
                    )

                if i == 0 and j == 0:
                    self.play((sub_matrix.animate.shift(original_position - sub_matrix.get_center())))

                # Thay thế giá trị cũ bằng giá trị mới trong output_matrix
                output_matrix[i + 1][j + 1][1] = new_text

        self.play(
            Uncreate(squared_window),
            grid_kernel.animate.scale(0),
            output_matrix.animate.shift(LEFT * 2.25),
            output_matrix_text.animate.shift(LEFT * 2.25)
        )

        blurred_image_mobject = ImageMobject("blurred_image.jpg").next_to(output_matrix, RIGHT * 2)

        input_image_text = Text(f"Before", font="SF Pro").scale(0.45).next_to(original_image, UP)
        output_image_text = Text(f"After", font="SF Pro").scale(0.45).next_to(blurred_image_mobject, UP)

        self.play(
            GrowFromPoint(blurred_image_mobject, point=output_matrix.get_center()),
            GrowFromPoint(input_image_text, point=original_image.get_center()),
            GrowFromPoint(output_image_text, point=output_matrix.get_center()),
            Unwrite(line1),
            Unwrite(line2),
            FadeOut(filled_region),
            FadeOut(red_overlay)
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
