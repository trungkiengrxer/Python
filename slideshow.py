from manim import *


class Slide(Scene):
    def construct(self):
        # Title with Gradient
        title = Text("My SlideShow", font_size=70, font="SF Pro")
        title.set_color_by_gradient(BLUE, PURPLE)

        background = ImageMobject(r"D:\OneDrive\Pictures\img20.jpg")
        background.scale_to_fit_height(config.frame_height)
        background.scale_to_fit_width(config.frame_width)

        self.add(background)
        title.to_edge(UP)  # Move the title to the top

        # Main content
        main_points = BulletedList(
            Text("Tran Dao Trung Kien", font="Arial"),
            Text("MSV: B23DCKH068", font="Arial"),
            Text("B23CQKH02-B", font="Arial"),
            Text("PTIT", font="Arial"),
            font_size=35,

        )

        main_points.set_color_by_gradient(BLUE, PURPLE)
        main_points.arrange(DOWN, aligned_edge=LEFT).next_to(
            title, DOWN, buff=0.5)

        # Applying gradient color to main points text
        main_points.set_color_by_gradient(YELLOW, ORANGE)

        # Display title with effect
        self.play(FadeIn(title, shift=UP), run_time=1.5)
        self.wait(1)

        # Display main content with effect
        for it in main_points:
            self.play(FadeIn(it, shift=UP), run_time=1)
            self.wait(0.5)

        # Create surrounding rectangle for main content
        frame = SurroundingRectangle(main_points, color=GREEN, buff=0.5)
        self.play(Create(frame), run_time=1)
        self.wait(1)

        # Add decorative shapes
        circle = Circle(radius=0.5, color=BLUE).next_to(frame, LEFT, buff=1)
        square = Square(side_length=0.7, color=YELLOW).next_to(
            frame, RIGHT, buff=1)
        triangle = Triangle().scale(0.7).next_to(frame, DOWN, buff=1)

        self.play(Create(circle), Create(square),
                  Create(triangle), run_time=1.5)
        self.wait(1)

        # Transition to the next slide
        next_slide = Text("Next Slide...", font_size=50,
                          color=PINK, font="SF Pro")
        self.play(Transform(main_points, next_slide), run_time=1)
        self.wait(1)

        # Fade out everything
        self.play(FadeOut(main_points), FadeOut(frame), FadeOut(title), FadeOut(
            circle), FadeOut(square), FadeOut(triangle), run_time=1)
