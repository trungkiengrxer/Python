import cv2
import numpy as np

# # Đọc ảnh
# img = cv2.imread("D:/Downloads/Lenna_(test_image).png")

# # Xác định tọa độ và kích thước của hình chữ nhật
# x_start, y_start = 50, 50  # Tọa độ góc trên bên trái
# width, height = 100, 100  # Kích thước hình chữ nhật

# # Chèn vùng màu đỏ
# # Tạo một hình chữ nhật màu đỏ
# red_rectangle = np.full((height, width, 3), (0, 0, 255), dtype=np.uint8)  # (B, G, R) cho OpenCV

# # Chèn hình chữ nhật vào ảnh gốc
# img[y_start:y_start + height, x_start:x_start + width] = red_rectangle

# # Lưu ảnh đã chỉnh sửa
# cv2.imwrite("image_with_red_rectangle.jpg", img)

# # Hiển thị ảnh
# cv2.imshow("Image with Red Rectangle", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
       # maxtrix_of_cropImg = []
        # for row in matrix:
        #     # Tạo các ô vuông cho từng hàng của ma trận
        #     squares = VGroup(*[Square(side_length=1).set_stroke(WHITE, 1, opacity=1) for _ in row]).arrange(RIGHT, buff=0.0)

        #     # Tạo số pixel cho từng ô vuông và di chuyển vào giữa các ô vuông
        #     numbers_in_squares = VGroup(*[Text(str(int(pixel)), color=WHITE, font="SF Pro", font_size=26).move_to(square.get_center())
        #                                 for pixel, square in zip(row, squares)])

        #     # Thêm hàng mới vào ma trận
        #     maxtrix_of_cropImg.append(VGroup(squares, numbers_in_squares))

        # # Sắp xếp toàn bộ các hàng trong ma trận
        # maxtrix_of_cropImg = VGroup(*maxtrix_of_cropImg).arrange(DOWN, buff=0.0)

        # # Hiển thị ma trận lên màn hình
        # self.play(FadeIn(maxtrix_of_cropImg))
        # self.wait(2)


# from manim import *
# import numpy as np
# import cv2

# class ImageOverlayExample(Scene):
#     def construct(self):
#         # Tạo ảnh gốc từ tệp
#         img = cv2.imread("D:/Downloads/Lenna_(test_image).png")
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         cv2.imwrite("processed_image.jpg", img)
        
#         # Tạo đối tượng ảnh trong Manim
#         original_image = ImageMobject("processed_image.jpg")
        
#         # Hiển thị ảnh gốc
#         self.play(FadeIn(original_image))

#         # Đặt ảnh ở giữa màn hình
#         self.play(original_image.animate.shift(LEFT * 2 + UP * 2))
#         self.wait(1)

#         # Tạo lớp phủ màu đỏ kích thước 5x5 pixel
#         overlay_width = 5 * 0.1  # Tương ứng với 5 pixel chiều rộng
#         overlay_height = 5 * 0.1  # Tương ứng với 5 pixel chiều cao
#         red_overlay = Rectangle(width=overlay_width, height=overlay_height, color=RED, fill_opacity=0.5)

#         # Di chuyển overlay sao cho góc trên bên trái của nó trùng với góc trên bên trái của ảnh
#         # Tính toán để đảm bảo rằng tâm của overlay nằm đúng vị trí góc trên trái của ảnh
#         overlay_shift = np.array([overlay_width / 2, -overlay_height / 2, 0])
#         red_overlay.move_to(original_image.get_corner(UL) + overlay_shift)

#         # Hiển thị lớp phủ màu đỏ trên ảnh gốc
#         self.play(FadeIn(red_overlay))
#         self.wait(2)



from manim import *
import numpy as np
import cv2

class ImageMappingExample(Scene):
    def construct(self):
        # Tạo ảnh gốc từ tệp
        img = cv2.imread("D:/Downloads/Lenna_(test_image).png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite("processed_image.jpg", img)
        
        # Tạo đối tượng ảnh trong Manim
        original_image = ImageMobject("processed_image.jpg")
        
        # Hiển thị ảnh gốc
        self.play(FadeIn(original_image))

        # Đặt ảnh ở giữa màn hình
        self.play(original_image.animate.shift(LEFT * 2 + UP * 2))
        self.wait(1)

        # Tạo lớp phủ màu đỏ kích thước 5x5 pixel
        overlay_width = 5 * 0.1  # Tương ứng với 5 pixel chiều rộng
        overlay_height = 5 * 0.1  # Tương ứng với 5 pixel chiều cao
        red_overlay = Rectangle(width=overlay_width, height=overlay_height, color=RED, fill_opacity=0.5)

        # Căn chỉnh overlay tới góc trên bên trái của ảnh
        overlay_shift = np.array([overlay_width / 2, -overlay_height / 2, 0])
        red_overlay.move_to(original_image.get_corner(UL) + overlay_shift)
        self.play(FadeIn(red_overlay))

        # Tạo ma trận 5x5
        cropped_img = img[0:5, 0:5]  # Vùng cắt ảnh
        matrix = np.array(cropped_img)

        # Tạo ma trận số trong Manim
        test = VGroup()
        square_size = 0.5
        number_of_rows, number_of_cols = matrix.shape[:2]

        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                test.add(VGroup(square, number))

        test.next_to(original_image, RIGHT * 2)  # Đặt ma trận bên phải ảnh
        self.play(FadeIn(test))

        # Tạo hai đường kẻ ánh xạ
        # Đường 1: Từ góc trên bên trái của overlay tới góc trên bên trái của ma trận
        line1 = Line(
            start=red_overlay.get_corner(UL), 
            end=test[0].get_corner(UL), 
            color=YELLOW
        )

        # Đường 2: Từ góc dưới bên phải của overlay tới góc dưới bên phải của ma trận
        line2 = Line(
            start=red_overlay.get_corner(DR), 
            end=test[-1].get_corner(DR), 
            color=YELLOW
        )

        # Hiển thị hai đường kẻ ánh xạ
        self.play(Create(line1), Create(line2))
        self.wait(2)

        # Hiển thị lớp phủ màu đỏ trên ảnh gốc
        # self.play(FadeIn(red_overlay))

        # # Tạo ma trận cho vùng ảnh cắt ra
        # grid = VGroup()
        # number_of_cols = len(matrix[0])
        # number_of_rows = len(matrix)

        # for i in range(number_of_rows):
        #     for j in range(number_of_cols):

        #         square = Square(side_length=square_size).set_stroke(WHITE, 1)
        #         square.move_to((j * square_size, -i * square_size, 0))

        #         number = Text(str(matrix[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
        #         grid.add(VGroup(square, number))

        # grid.next_to(original_image, RIGHT * 2)
        # self.play(FadeIn(grid))

        # line1 = Line(start=red_overlay.get_corner(UR), end=grid[0].get_corner(UL), color=RED)
        # line2 = Line(start=red_overlay.get_corner(DR), end=grid[20][0].get_corner(DL), color=RED)
        # self.play(Create(line1), Create(line2))
        # self.wait(2)