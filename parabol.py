from manim import *

class ExtendedParabolaGraph(Scene):
    def construct(self):
        # Tạo trục tọa độ với phạm vi lớn hơn
        axes = Axes(
            x_range=[-10, 10, 1],  # Mở rộng trục x từ -10 đến 10
            y_range=[-5, 100, 10],  # Mở rộng trục y từ -5 đến 100
            axis_config={"color": BLUE},  # Màu sắc của trục tọa độ
        )

        # Tạo nhãn cho trục x và y bằng Text
        x_label = Text("x").next_to(axes.x_axis, RIGHT)  # Nhãn cho trục x
        y_label = Text("y").next_to(axes.y_axis, UP)  # Nhãn cho trục y

        # Định nghĩa đồ thị y = x^2 với phạm vi lớn hơn
        parabola_graph = axes.plot(lambda x: x**2, x_range=[-10, 10], color=YELLOW)

        # Nhãn đồ thị y = x^2 sử dụng Text
        graph_label = Text("y = x^2").next_to(axes.c2p(3, 9), UR)

        # Tạo một điểm di chuyển trên đồ thị
        moving_dot = Dot(color=RED).move_to(axes.i2gp(0, parabola_graph))

        # Tạo dấu vết của điểm di chuyển
        dot_trace = TracedPath(moving_dot.get_center, stroke_color=RED, stroke_width=4)

        # Hoạt ảnh
        self.play(Create(axes))  # Tạo trục tọa độ
        self.play(Write(x_label), Write(y_label))  # Viết nhãn cho trục x và y
        self.play(Create(parabola_graph))  # Tạo đồ thị parabol
        self.play(Write(graph_label))  # Viết nhãn cho đồ thị

        # Di chuyển điểm dọc theo parabol, mô phỏng việc di chuyển tới vô cực
        self.add(dot_trace)
        self.play(MoveAlongPath(moving_dot, parabola_graph), run_time=8, rate_func=linear)

        # Chờ và hoàn tất cảnh
        self.wait(2)
