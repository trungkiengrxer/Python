from manim import *
import cv2
import numpy
from PIL import Image
import operator


class SobelEdgeDetection(Scene):
    def construct(self):

        # Tỷ lệ xấp xỉ giữa pixel và toạ độ trong manim
        ratio = 0.0043888888888888888

        # Tạo text giới thiệu về bộ lọc trung bình và hiển thị
        sobel_detection_text = Text("Sobel Edge Detection", font="SF Pro Display").scale(0.7)
        glow_sobel_detection_text = self.create_glow(sobel_detection_text)

        self.play(glow_sobel_detection_text.animate.shift(UP * 3.5))

        # Đọc ảnh và chuyển sang gam màu xám
        img = cv2.imread("D:/Downloads/Sobel Img.png")
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
        self.play(
            original_image.animate.shift(LEFT * 4.5),
        )

        # Cắt hình ảnh có kích thước 6x6 từ vị trí (50, 50) pixel
        cropped_img = img[50:55, 50:55]

        # Chuyển các pixel sang ma trận
        matrix = numpy.array(cropped_img)

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
        sobel_operator_x = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
        sobel_matrix_x = self.create_grid(sobel_operator_x, square_size)
        for row in sobel_matrix_x:
            for cell in row:
                cell[0].set_fill(BLUE, opacity=0.4)

        sobel_operator_y = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
        sobel_matrix_y = self.create_grid(sobel_operator_y, square_size)
        for row in sobel_matrix_y:
            for cell in row:
                cell[0].set_fill(GREEN, opacity=0.4)

        self.play(
            Uncreate(filled_region),
            Uncreate(line1),
            Uncreate(line2),
            Uncreate(red_overlay),
        )

        self.play(
            original_image.animate.shift(LEFT * 5),
            grid_vgroup.animate.shift(LEFT * 4.5),
        )

        # Di chuyển lưới kernel 3x3 đến vị trí phù hợp và hiển thị
        sobel_matrix_x.move_to(grid_vgroup.get_center() + [6, 1, 0])
        sobel_matrix_y.move_to(grid_vgroup.get_center() + [6, -1, 0])

        # Tạo text đánh dấu ma trận input và kernel
        input_matrix_text = Text("Input Matrix", font="SF Pro").scale(0.45).move_to(grid_vgroup.get_center() + [0, 1.6, 0])
        sobel_x_text = Text("Sobel X Operator", font="SF Pro").scale(0.45).move_to(sobel_matrix_x.get_center() + [0, 1.1, 0])
        sobel_y_text = Text("Sobel Y Operator", font="SF Pro").scale(0.45).move_to(sobel_matrix_y.get_center() + [0, -1.1, 0])

        # Cửa sổ trượt đánh dấu vùng ma trận con cần xét
        squared_window = Square(side_length=square_size * 3 + 0.25).set_stroke(BLUE, 2.5)
        squared_window.set_z_index(10)

        # Vị trí trung tâm của sobel_matrix_x và grid_vgroup
        sobel_matrix_position = sobel_matrix_x.get_center()
        grid_vgroup_position = grid_vgroup.get_center()

        # Tạo ma trận output và text
        gx_matrix = self.create_empty_grid(5, 5, square_size).move_to(grid_vgroup_position + [9, 1.5, 0])
        gx_matrix_text = MathTex("G_x Matrix").scale(0.6).move_to(gx_matrix.get_center() + [0, 1.6, 0])

        gy_matrix = self.create_empty_grid(5, 5, square_size).move_to(grid_vgroup_position + [9, -1.5, 0])
        gy_matrix_text = MathTex("G_y Matrix").scale(0.6).move_to(gy_matrix.get_center() + [0, -1.6, 0])

        self.play(
            GrowFromEdge(sobel_matrix_x, DOWN),
            GrowFromEdge(sobel_matrix_y, UP),
            GrowFromPoint(gx_matrix, point=sobel_matrix_position),
            GrowFromPoint(gy_matrix, point=sobel_matrix_position),
            Write(sobel_x_text),
            Write(sobel_y_text),
            GrowFromPoint(input_matrix_text, point=grid_vgroup_position),
            Write(gx_matrix_text),
            Write(gy_matrix_text)
        )

        # Hiển thị cửa sổ trượt và ma trận output, đồng thời scale sobel_x_text về 0
        self.play(
            DrawBorderThenFill(squared_window.move_to(grid_vgroup[1][1].get_center())),
            sobel_x_text.animate.scale(0),
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
                    self.play(sub_matrix.animate.move_to(grid_vgroup.get_center() + [3.5, 0, 0]))
                    self.play(sobel_matrix_x.animate.move_to(sub_matrix.get_center()))
                    after_moving_sub_matrix_position = sub_matrix.get_center()

                # Kết quả tích chập
                sum = 0

                for u in range(3):
                    for v in range(3):

                        # Phép nhân giữa ma trận con và kernel tương ứng vị trí
                        multiply = matrix[i + u][j + v] * sobel_operator_x[u][v]
                        # Cộng dần kết quả
                        sum += multiply

                # Kết quả sau khi chia trung bình và làm tròn

                # Tạo các text cho kết quả đầu tiên
                sum_text = Text(
                    f"Convolution = {sum}",
                    color=WHITE,
                    font="SF Pro"
                ).scale(0.4).move_to(ORIGIN + [0, 2.25, 0])

                # Tạo các text cho các kết quả sau
                sum_result_text = Text(f"Convolution = {sum}", color=WHITE, font="SF Pro").scale(0.4).move_to(ORIGIN + [0, 2.25, 0])

                # Tạo text giá trị để cho vào ma trận output
                new_text = Text(f"{sum}", font="SF Pro").scale(0.4)
                new_text.move_to(gx_matrix[i + 1][j + 1][0].get_center())

                # Hiển thị các kết quả sau
                if i != 0 or j != 0:
                    if j <= 2 and i == 0:
                        # Di chuyển cửa sổ trượt và ma trận kernel đè lên đè lên các ma trận con
                        self.play(
                            squared_window.animate.move_to(grid_vgroup[i + 1][j + 1].get_center()),
                            sobel_matrix_x.animate.move_to(sub_matrix.get_center())
                        )

                        # Hiển thị kết quả sum và quotient
                        self.play(
                            GrowFromPoint(sum_result_text, point=sum_text.get_center()),
                        )

                        self.wait(0.5)

                        # Hiển thị kểt quả vào ma trận output và làm biến mất kết quả sum và quotient cũ
                        self.play(
                            sum_result_text.animate.scale(0),
                            GrowFromPoint(new_text, point=gx_matrix[i + 1][j + 1][0].get_center())
                        )

                    else:
                        # Di chuyển cửa sổ trượt và ma trận kernel đè lên đè lên các ma trận con
                        self.play(
                            squared_window.animate.move_to(grid_vgroup[i + 1][j + 1].get_center()),
                            sobel_matrix_x.animate.move_to(sub_matrix.get_center()),
                            run_time=0.1
                        )

                        # Hiển thị kểt quả vào ma trận output và làm biến mất kết quả sum và quotient cũ
                        self.play(
                            GrowFromPoint(new_text, point=gx_matrix[i + 1][j + 1][0].get_center()),
                            run_time=0.1
                        )
                # Hiển thị kết quả trường hợp đầu tiên
                else:
                    self.play(
                        GrowFromPoint(sum_result_text, point=sum_result_text.get_center())
                    )

                    self.wait(1)

                    self.play(
                        sum_result_text.animate.scale(0),
                        GrowFromPoint(new_text, point=gx_matrix[i + 1][j + 1][0].get_center())
                    )

                if j == 2 and i != 2:
                    self.play(
                        squared_window.animate.move_to(grid_vgroup[i + 1][j - 1].get_center()),
                        sobel_matrix_x.animate.move_to(grid_vgroup[i + 1][j - 1].get_center()),
                        run_time=0.1
                    )

                if i == 0 and j == 0:
                    self.play((sub_matrix.animate.shift(original_position - sub_matrix.get_center())))

                # Thay thế giá trị cũ bằng giá trị mới trong gx_matrix
                gx_matrix[i + 1][j + 1][1] = new_text

                if i == 2 and j == 2:
                    self.wait(0.5)
                    self.play(sobel_matrix_x.animate.scale(0)),
                    self.play(squared_window.animate.move_to(grid_vgroup[1][3].get_center()))
                    self.play(squared_window.animate.move_to(grid_vgroup[1][1].get_center()))
                    self.play(sobel_y_text.animate.scale(0))
                    self.wait(0.5)
                    self.play(sobel_matrix_y.animate.move_to(squared_window.get_center()))
                    self.wait(1)

        for i in range(3):
            for j in range(3):

                # Tạo ma trận con 3x3 từ ma trận 5x5
                sub_matrix = VGroup(*[grid_vgroup[i + u][j + v] for u in range(3) for v in range(3)])

                # Lưu vị trí ban đầu của ma trận con vừa tạo
                original_position = sub_matrix.get_center()

                # Kết quả tích chập
                sum = 0

                for u in range(3):
                    for v in range(3):

                        # Phép nhân giữa ma trận con và kernel tương ứng vị trí
                        multiply = matrix[i + u][j + v] * sobel_operator_y[u][v]
                        # Cộng dần kết quả
                        sum += multiply

                # Hiển thị các kết quả sau
                new_text = Text(f"{sum}", font="SF Pro").scale(0.4)
                new_text.move_to(gy_matrix[i + 1][j + 1][0].get_center())
                if i != 0 or j != 0:
                    self.play(
                        squared_window.animate.move_to(grid_vgroup[i + 1][j + 1].get_center()),
                        sobel_matrix_y.animate.move_to(sub_matrix.get_center()),
                        run_time=0.1
                    )

                    self.play(
                        GrowFromPoint(new_text, point=gy_matrix[i + 1][j + 1][0].get_center()),
                        run_time=0.1
                    )

                if j == 2 and i != 2:
                    self.play(
                        squared_window.animate.move_to(grid_vgroup[i + 1][j - 1].get_center()),
                        sobel_matrix_y.animate.move_to(grid_vgroup[i + 1][j - 1].get_center()),
                        run_time=0.1
                    )

                # Thay thế giá trị cũ bằng giá trị mới trong gx_matrix
                gy_matrix[i + 1][j + 1][1] = new_text

        self.wait(1)

        self.play(
            sobel_matrix_y.animate.scale(0),
            Unwrite(squared_window)
        )

        self.play(
            grid_vgroup.animate.shift(LEFT * 4.5),
            input_matrix_text.animate.shift(LEFT * 4.5),
            gx_matrix.animate.move_to([-5, 1.5, 0]),
            gx_matrix_text.animate.move_to([-5, 3.1, 0]),

            gy_matrix.animate.move_to([-5, -1.5, 0]),
            gy_matrix_text.animate.move_to([-5, -3.1, 0]),
        )

        combined_matrix = self.create_empty_grid(5, 5, square_size).move_to([5, 0, 0])
        combined_matrix_text = Text("Magnitude", font="SF Pro").scale(0.45).move_to([5, 1.6, 0])

        self.play(
            GrowFromPoint(combined_matrix, point=[5, 0, 0]),
            Write(combined_matrix_text)
        )

        equation = MathTex(f"G = \\sqrt{{G_x^2 + G_y^2}}").scale(0.6).move_to(ORIGIN + [0, -2, 0])

        hidden_combined_matrix = self.create_empty_grid(5, 5, square_size)
        threshold_value = 0
        array = []

        for i in range(3):
            for j in range(3):
                gx = int(gx_matrix[i + 1][j + 1][1].get_text())
                gy = int(gy_matrix[i + 1][j + 1][1].get_text())
                x_backup_element = gx_matrix[i + 1][j + 1].copy()
                y_backup_element = gy_matrix[i + 1][j + 1].copy()

                magnitude = int(numpy.sqrt(gx**2 + gy**2))

                threshold_value += magnitude
                array.append(magnitude)

                g_x_text = MathTex(f"G_x = {gx}").scale(0.6).move_to([-1, 1, 0]).set_color(YELLOW)
                g_y_text = MathTex(f"G_y = {gy}").scale(0.6).move_to([1, 1, 0]).set_color(PINK)

                self.play(
                    gx_matrix[i + 1][j + 1][0].animate.set_fill(YELLOW, opacity=0.4).set_stroke(YELLOW),
                    gy_matrix[i + 1][j + 1][0].animate.set_fill(PINK, opacity=0.4).set_stroke(PINK),
                    run_time=0.1
                )

                new_text = Text(f"{magnitude}", font="SF Pro").scale(0.4)
                new_text.move_to(combined_matrix[i + 1][j + 1][0].get_center())
                if i == 0 and j <= 2:
                    x_copy_element = gx_matrix[i + 1][j + 1].copy()
                    y_copy_element = gy_matrix[i + 1][j + 1].copy()
                    self.wait(0.5)
                    self.play(
                        ReplacementTransform(x_copy_element, g_x_text),
                        ReplacementTransform(y_copy_element, g_y_text)
                    )

                    self.wait(1)

                    group_text = VGroup(g_x_text, g_y_text)

                    result = MathTex(
                        r"G = \sqrt{(", str(gx), ")^2 + (", str(gy), ")^2} = ", str(magnitude)
                    ).scale(0.6).move_to([0, 0, 0])

                    result[1].set_color(YELLOW)
                    result[3].set_color(PINK)

                    self.play(ReplacementTransform(group_text, result))
                    self.wait(0.5)
                    self.play(ReplacementTransform(result, new_text))

                else:
                    self.play(
                        GrowFromPoint(new_text, point=combined_matrix[i + 1][j + 1][0].get_center()), run_time=0.1
                    )

                combined_matrix[i + 1][j + 1][1] = new_text

                self.play(
                    gx_matrix[i + 1][j + 1][0].animate.set_fill(opacity=0).set_stroke(WHITE),
                    gy_matrix[i + 1][j + 1][0].animate.set_fill(opacity=0).set_stroke(WHITE),
                    run_time=0.1
                )

        self.wait(0.5)
        output_edge_matrix = self.create_empty_grid(5, 5, square_size).move_to([5, 0, 0])
        output_edge_matrix_text = Text("Edge", font="SF Pro").scale(0.45).move_to([5, 1.6, 0])

        self.play(
            gx_matrix.animate.move_to([-5, 11, 0]),
            gx_matrix_text.animate.move_to([-5, 12.6, 0]),

            gy_matrix.animate.move_to([-5, -11, 0]),
            gy_matrix_text.animate.move_to([-5, -12.6, 0]),

            combined_matrix.animate.move_to([-5, 0, 0]),
            combined_matrix_text.animate.move_to([-5, 1.6, 0]),

            GrowFromPoint(output_edge_matrix, point=[5, 0, 0]),
            Write(output_edge_matrix_text)
        )

        self.wait(0.5)

        a1, a2, a3, a4, a5, a6, a7, a8, a9 = array

        threshold_value = int(threshold_value / 9)
        threshold_text = MathTex(
            r"\theta = \frac{" + str(a1) + "+" + str(a2) + "+" + str(a3) + "+" + str(a4) + "+" + str(a5) + "+" + str(a6) + "+" + str(a7) + "+" + str(a8) + "+" + str(a9) + "}{9} = " + str(threshold_value)
        ).scale(0.6).move_to([0, 0, 0])
        combined_matrix_copy = combined_matrix.copy()

        self.play(
            ReplacementTransform(combined_matrix_copy, threshold_text),
        )

        self.wait(1)

        threshold_text_final = Text(f"θ = {threshold_value}", font="SF Pro").scale(0.45).move_to([1, 0, 0])
        self.play(
            ReplacementTransform(threshold_text, threshold_text_final)
        )

        greater_than_symbol = MathTex(">").set_stroke(width=2).scale(0.6).move_to([0, 0, 0])
        less_than_symbol = MathTex("<").set_stroke(width=2).scale(0.6).move_to([0, 0, 0])
        equal_symbol = MathTex("=").set_stroke(width=2).scale(0.6).move_to([0, 0, 0])

        for i in range(3):
            for j in range(3):
                magnitude = int(combined_matrix[i + 1][j + 1][1].get_text())
                self.play(combined_matrix[i + 1][j + 1][0].animate.set_fill(YELLOW, opacity=0.4).set_stroke(YELLOW), run_time=0.1)
                if i == 1 and j == 0:
                    self.play(threshold_text_final.animate.scale(0), run_time=0.1)
                if i == 0 and j <= 2:
                    self.wait(0.5)
                    element = combined_matrix[i + 1][j + 1].copy()
                    self.play(element.animate.move_to([-1, 0, 0]))

                    if magnitude > threshold_value:
                        text = Text("1", font="SF Pro").scale(0.4).move_to(output_edge_matrix[i + 1][j + 1][0].get_center())
                        self.play(GrowFromPoint(greater_than_symbol, point=[0, 0, 0]))
                        self.play(Indicate(greater_than_symbol, color=WHITE))
                        self.play(
                            FadeOut(greater_than_symbol),
                            element.animate.scale(0),
                            GrowFromPoint(text, point=output_edge_matrix[i + 1][j + 1][0].get_center())
                        )
                        output_edge_matrix[i + 1][j + 1][1] = text

                    elif magnitude < threshold_value:
                        text = Text("0", font="SF Pro").scale(0.4).move_to(output_edge_matrix[i + 1][j + 1][0].get_center())
                        self.play(GrowFromPoint(less_than_symbol, point=[0, 0, 0]))
                        self.play(Indicate(less_than_symbol, color=WHITE))
                        self.play(
                            FadeOut(less_than_symbol),
                            element.animate.scale(0),
                            GrowFromPoint(text, point=output_edge_matrix[i + 1][j + 1][0].get_center())
                        )
                        output_edge_matrix[i + 1][j + 1][1] = text

                    else:
                        text = Text("0", font="SF Pro").scale(0.4).move_to(output_edge_matrix[i + 1][j + 1][0].get_center())
                        self.play(GrowFromPoint(equal_symbol, point=[0, 0, 0]))
                        self.play(Indicate(equal_symbol, color=WHITE))
                        self.play(
                            FadeOut(equal_symbol),
                            element.animate.scale(0),
                            GrowFromPoint(text, point=output_edge_matrix[i + 1][j + 1][0].get_center())
                        )
                        output_edge_matrix[i + 1][j + 1][1] = text

                else:
                    if magnitude > threshold_value:
                        text = Text("1", font="SF Pro").scale(0.4).move_to(output_edge_matrix[i + 1][j + 1][0].get_center())
                        self.play(GrowFromPoint(text, point=output_edge_matrix[i + 1][j + 1][0].get_center()), run_time=0.1)
                        output_edge_matrix[i + 1][j + 1][1] = text

                    elif magnitude < threshold_value:
                        text = Text("0", font="SF Pro").scale(0.4).move_to(output_edge_matrix[i + 1][j + 1][0].get_center())
                        self.play(GrowFromPoint(text, point=output_edge_matrix[i + 1][j + 1][0].get_center()), run_time=0.1)
                        output_edge_matrix[i + 1][j + 1][1] = text

                    else:
                        text = Text("0", font="SF Pro").scale(0.4).move_to(output_edge_matrix[i + 1][j + 1][0].get_center())
                        self.play(GrowFromPoint(text, point=output_edge_matrix[i + 1][j + 1][0].get_center()), run_time=0.1)
                        output_edge_matrix[i + 1][j + 1][1] = text

                self.play(combined_matrix[i + 1][j + 1][0].animate.set_fill(opacity=0).set_stroke(WHITE), run_time=0.1)

        self.wait(0.5)
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

        sobel_magnitude = cv2.magnitude(sobel_x, sobel_y)
        threshold = numpy.mean(sobel_magnitude)

        _, sobel_thresh = cv2.threshold(sobel_magnitude, threshold, 255, cv2.THRESH_BINARY)

        cv2.imwrite("sobel_thresh.jpg", sobel_thresh)
        processed_image = ImageMobject("sobel_thresh.jpg").set_z_index(10)
        processed_text = Text("Processed Image", font="SF Pro").scale(0.45).move_to([4, 2.2, 0])

        origin_text = Text("Original Image", font="SF Pro").scale(0.45).move_to([-4, 2.2, 0])

        self.play(
            combined_matrix.animate.move_to([0, 0, 0]),
            combined_matrix_text.animate.move_to([0, 1.6, 0]),

            grid_vgroup.animate.move_to([-5, 0, 0]),
            input_matrix_text.animate.move_to([-5, 1.6, 0]),
        )

        self.wait(2)

        self.play(
            original_image.animate.move_to([0, 0, 0]),
            combined_matrix.animate.move_to([0, 11, 0]),
            combined_matrix_text.animate.move_to([0, 12.6, 0]),

            grid_vgroup.animate.move_to([-5, -11, 0]),
            input_matrix_text.animate.move_to([-5, -12.6, 0]),

            output_edge_matrix.animate.move_to([5, -11, 0]),
            output_edge_matrix_text.animate.move_to([5, -12.6, 0]),
        )

        self.play(
            FadeIn(processed_image),
        )
        self.play(
            original_image.animate.move_to([-4, 0, 0]),
            Write(origin_text),

            processed_image.animate.move_to([4, 0, 0]),
            Write(processed_text)
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
