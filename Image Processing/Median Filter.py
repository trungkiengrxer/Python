from manim import *
import cv2
import numpy
from PIL import Image
import operator


class MedianFilter(Scene):
    def construct(self):

        # Tỷ lệ xấp xỉ giữa pixel và toạ độ trong manim
        ratio = 0.0043888888888888888

        # Tạo text giới thiệu về bộ lọc trung vị và hiển thị
        median_filter_text = Text("Median Filter", font="SF Pro Display").scale(0.7)
        glow_median_filter_text = self.create_glow_text(median_filter_text)
        self.play(glow_median_filter_text.animate.shift(UP * 3))

        # Đọc ảnh và chuyển sang gam màu xám
        img = cv2.imread("D:/Downloads/Lenna_(test_image).png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Logo PTIT góc trên bên trái
        logo = cv2.imread("D:/Downloads/ptit-logo-circle.png")
        cv2.imwrite("ptit_logo.png", logo)
        ptit_logo_mobject = ImageMobject("ptit_logo.png").scale(0.4).move_to([-6.7, 3.6, 0])

        # Text giới thiệu góc dưới bên phải
        copyright_text = Text("STDR2024 @EIC&DSP LAB", font="SF Pro").scale(0.2).move_to([6.2, -3.6, 0])
        creator_text = Text("Designed by Trung Kiên", font="SF Pro").scale(0.2).move_to([6.335, -3.75, 0])

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

        # Tạo vùng fill màu xanh dương giữa Line1 và Line2 bằng Polygon
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


        # Di chuyển lưới kernel 3x3 đến vị trí phù hợp và hiển thị

        # Tạo text đánh dấu ma trận input và kernel
        matrix_text = Text("Input Matrix", font="SF Pro").scale(0.45).move_to(grid_vgroup.get_center() + [0, 1.6, 0])

        # Tạo ảnh mờ bằng cv2 và lưu
        blurred_image = cv2.medianBlur(img, 3)
        cv2.imwrite("blurred_image.jpg", blurred_image)

        # Cửa sổ trượt đánh dấu vùng ma trận con cần xét
        squared_window = Square(side_length=square_size * 3 + 0.25).set_stroke(color = [BLUE, PINK, RED, YELLOW]).set_z_index(10)
        glowing_squared_window = self.create_glow_mobject(squared_window)

        # Vị trí trung tâm của grid_kernel và grid_vgroup
        grid_vgroup_position = grid_vgroup.get_center()

        # Tạo ma trận output và text
        output_matrix = self.create_empty_grid(5, 5, square_size).move_to(grid_vgroup_position + [5, 0, 0] + ORIGIN)
        output_matrix_text = Text(f"Output Matrix", font="SF Pro").scale(0.45).move_to(output_matrix.get_center() + [0, 1.6, 0])

        # Hiển thị text đánh dấu ma trận input
        self.play(GrowFromPoint(matrix_text, point=grid_vgroup.get_center()))

        # Hiển thị cửa sổ trượt và ma trận output, đồng thời scale kernel_text về 0
        self.play(
            DrawBorderThenFill(glowing_squared_window.move_to(grid_vgroup[1][1].get_center())),
            GrowFromPoint(output_matrix, point=output_matrix.get_center()),
            GrowFromPoint(output_matrix_text, point=output_matrix.get_center())
        )

        for i in range(3):
            for j in range(3):

                # Tạo ma trận con 3x3 từ ma trận 5x5
                sub_matrix = VGroup(*[grid_vgroup[i + u][j + v] for u in range(3) for v in range(3)])

                # Lưu vị trí ban đầu của ma trận con vừa tạo
                original_position = sub_matrix.get_center()

                grid =[]
                if i == 0 and j == 0:
                    copy_sub_matrix = sub_matrix.copy()
                    original_position_of_sorted_sub_matrix_elements = {}
                    
                    sorted_indices = sorted(range(9), key=lambda k: int(sub_matrix[k][1].text))

                    sorted_elements = []
                    for k, u in enumerate(sorted_indices):
                        position = sub_matrix[u].copy().get_center()
                        sorted_elements.append(sub_matrix[u].copy())
                        original_position_of_sorted_sub_matrix_elements[sorted_elements[k]] = position

                    target_position = grid_vgroup_position + [-0.5, -2.25, 0] 
                    for k, element in enumerate(sub_matrix):
                        self.play(element.animate.move_to(target_position + RIGHT * k * square_size), run_time=0.2)

                    
                    for k, element in enumerate(sorted_elements):
                        element.move_to(target_position + RIGHT * k * square_size)

                    self.play(
                        *[ReplacementTransform(sub_matrix[u], sorted_elements[k]) for k, u in enumerate(sorted_indices)],
                        run_time=1
                    )

                    square_highlight = Square(side_length=square_size + 0.15, fill_opacity=0, color=GOLD).move_to(sorted_elements[4].get_center())
                    glowing_square_highlight = self.create_glow_mobject(square_highlight)

                    median_text = Text(f"Median = {int(sorted_elements[4][1].text)}", font="SF Pro").scale(0.4).move_to(ORIGIN + [0, -2.80, 0])

                    new_text = Text(str(int(sorted_elements[4][1].text)), font="SF Pro").scale(0.4)
                    new_text.move_to(output_matrix[i + 1][j + 1][0].get_center())

  
                    self.play(
                        DrawBorderThenFill(glowing_square_highlight),
                        GrowFromPoint(median_text, point=median_text.get_center())
                    )

                    self.wait(0.5)

                    self.play(
                        median_text.animate.scale(0), 
                        GrowFromPoint(new_text, point=new_text.get_center()),
                        glowing_square_highlight.animate.scale(0)
                    )

                    output_matrix[i + 1][j + 1][1] = new_text 

                    for u in range(9):
                        self.play(
                            sorted_elements[u].animate.move_to(original_position_of_sorted_sub_matrix_elements[sorted_elements[u]]), 
                            run_time = 0.2
                        )

                    sub_matrix = copy_sub_matrix

                    self.play(
                        glowing_squared_window.animate.move_to(grid_vgroup[i + 1][j + 1].get_center()),
                    )
                

                else:
                    self.play(
                        glowing_squared_window.animate.move_to(grid_vgroup[i + 1][j + 1].get_center()),
                    )
                    array = []
                    for u in range(3):
                        for v in range(3):
                            array.append(matrix[i + u][j + v])

                    array.sort()
                    median_value = array[4]
                    median_text = Text(f"Median = {median_value}", font="SF Pro").scale(0.4).move_to(ORIGIN + [0, -2.80, 0])

                    new_text = Text(str(median_value), font="SF Pro").scale(0.4)
                    new_text.move_to(output_matrix[i + 1][j + 1][0].get_center())

                    self.play(GrowFromPoint(median_text, point=median_text.get_center()))
                    self.wait(0.5)
                    self.play(
                        median_text.animate.scale(0), 
                        GrowFromPoint(new_text, point=new_text.get_center())
                    )

                    output_matrix[i + 1][j + 1][1] = new_text


                if j == 2 and i != 2:
                    self.play(
                        glowing_squared_window.animate.move_to(grid_vgroup[i + 1][j - 1].get_center()),
                    )

        self.play(
            glowing_squared_window.animate.scale(0),
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

    gradient_colors = [BLUE, PINK, RED, YELLOW]

    def create_glow_text(self, vmobject, rad=1):
        glow_group = VGroup()
        for idx in range(60):
            glowing_text = vmobject.copy()
            stroke_width = rad * (1.002**((idx/1)**2)) / 18.345
            opacity_of_glow = 0.2 - idx / 305

            glowing_text.set_stroke(width=stroke_width, opacity=opacity_of_glow)
            glowing_text.set_color_by_gradient(*self.gradient_colors)
            glow_group.add(glowing_text)

        glow_group.add(vmobject)
        return glow_group

    def create_glow_mobject(self, vmobject, rad=1):
        glow_group = VGroup()
        for idx in range(80):
            glowing_mobject = vmobject.copy()
            stroke_width = rad * (1.002**((idx/1)**2)) / 18.345
            opacity_of_glow = 0.2 - idx / 305

            glowing_mobject.set_stroke(width=stroke_width, color = self.gradient_colors, opacity=opacity_of_glow)
            glow_group.add(glowing_mobject)
            
        glow_group.add(vmobject)
        return glow_group