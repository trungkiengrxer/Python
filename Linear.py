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
        squares_size = 1
        squares = VGroup(*[RoundedRectangle(height=squares_size, width=squares_size, corner_radius=0.2).set_fill(BLUE, opacity=0.5).set_stroke(WHITE, 0) for _ in array]).arrange(RIGHT, buff=0.1)

        # Hiển thị giá trị bên trong các ô vuông
        numbers = VGroup(*[Text(str(num), font="SF Pro").move_to(square) for num, square in zip(array, squares)])

        # Hiển thị thông tin ban đầu
        array_text = Text("Linear Search Algorithm", font="SF Pro", font_size=36)
        array_text.set_color_by_gradient(RED, LIGHT_PINK)
        search_text = Text(f"Target: {target}", font="SF Pro", font_size=33).next_to(squares, DOWN)

        # Thêm tất cả các phần tử vào Scene
        self.play(array_text.animate.shift(UP * 2.2))
        self.play(FadeIn(squares, run_time=0.5), FadeIn(numbers, run_time=0.5), FadeIn(search_text, run_time=0.5))
        self.wait(1)
        index_text = Text(f"Current Index: 0 - Value: {array[0]} - Next Index {1}", font="SF Pro", font_size=33).next_to(search_text, DOWN)
        self.play(FadeIn(index_text, run_time=0.5))
        found = False

        # Mô phỏng quá trình tìm kiếm
        for i, (square, num, number) in enumerate(zip(squares, array, numbers)):
            # Tạo chữ
            if (i == len(array) - 1):
                next = "null"
            else:
                next = str(i + 1)
            new_index_text = Text(f"Current Index: {i} - Value: {num} - Next Index: {next}", font="SF Pro", font_size=33).next_to(search_text, DOWN)

            # Đánh dấu ô đang kiểm tra
            self.play(square.animate.set_fill(RED, opacity=0.7).shift(UP), number.animate.shift(UP), Transform(index_text, new_index_text))
            self.wait(0.5)

            # Kiểm tra nếu phần tử là phần tử cần tìm
            if num == target:
                self.play(square.animate.set_fill(GREEN, opacity=0.7))
                success_text = Text(f"Found {target} at index {i}", font="SF Pro", font_size=33).next_to(new_index_text, DOWN)
                success_text.set_color_by_gradient(RED, LIGHT_PINK)

                self.play(FadeIn(success_text, run_time=0.5))
                found = True
                break
            # else:
            #     not_equal_text = Text(f"{num} != {target}", font="SF Pro", font_size=36).next_to
            self.play(square.animate.shift(DOWN), number.animate.shift(DOWN))

        if not found:
            # Nếu không đúng, trả lại màu ban đầu
            unsuccessful_text = Text(f"Not fount {target}", font="SF Pro", font_size=33)
            unsuccessful_text.next_to(index_text, DOWN)
            self.play(FadeIn(unsuccessful_text, run_time=0.5))
            self.play(square.animate.set_fill(BLUE, opacity=0.5))
        self.wait(2)
