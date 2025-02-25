import manim as mn
import numpy as np

from manim import *
#config.media_width = "75%"
#config.verbosity = "WARNING"

class SquareToCircle(Scene):
    def construct(self):
        self.camera.frame_height = 8
        self.camera.frame_width = 14

        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))

class PlotExample(Scene):
    def construct(self):
        plot_axes = Axes(
            x_range=[0, 1, 0.05],
            y_range=[0, 1, 0.05],
            # x_length=4,       #9
            # y_length=2,     #5.5
            axis_config={
                "numbers_to_include": np.arange(0, 1 + 0.1, 0.1),
                "font_size": 24,
            },
            tips=False,
        )

        y_label = plot_axes.get_y_axis_label("y", edge=LEFT, direction=LEFT, buff=0.4)
        x_label = plot_axes.get_x_axis_label("x")
        plot_labels = VGroup(x_label, y_label)

        plots = VGroup()
        for n in np.arange(1, 20 + 0.5, 0.5):
            plots += plot_axes.plot(lambda x: x ** n, color=WHITE)
            plots += plot_axes.plot(
                lambda x: x ** (1 / n), color=WHITE, use_smoothing=False
            )

        extras = VGroup()
        extras += plot_axes.get_horizontal_line(plot_axes.c2p(1, 1, 0), color=BLUE)
        extras += plot_axes.get_vertical_line(plot_axes.c2p(1, 1, 0), color=BLUE)
        extras += Dot(point=plot_axes.c2p(1, 1, 0), color=YELLOW)
        title = Title(
            r"Graphs of $y=x^{\frac{1}{n}}$ and $y=x^n (n=1, 1.5, 2, 2.5, 3, \dots, 20)$",
            include_underline=False,
            font_size=40,
        )

        self.play(Write(title))
        self.play(Create(plot_axes), Create(plot_labels), Create(extras))
        self.play(AnimationGroup(*[Create(plot) for plot in plots], lag_ratio=0.05))


class IntensityToHeight(Scene):
    def construct(self):
        self.camera.frame_height = 8
        self.camera.frame_width = 14

        plot_axes = Axes(
            x_range=[0, np.pi*6, 0.5*np.pi],
            y_range=[0, 1, 0.05],
            x_length=9,
            y_length=6,
            x_axis_config={"numbers_to_include": np.arange(0, 3.14*6, 3.14)},
            y_axis_config={"numbers_to_include": np.arange(0, 1, 0.2)},
            tips=False,
        )
        y_label = plot_axes.get_y_axis_label("intensity", edge=LEFT, direction=LEFT, buff=0.4)
        x_label = plot_axes.get_x_axis_label("radians")
        plot_labels = VGroup(x_label, y_label)

        plots = VGroup()
        #I profile = a*cos(2pi*N) + b
        #For ease, let's plot N=[0,3] ->  I = 0.4 cos([0,6pi]) + 0.5
        plots += plot_axes.plot(lambda x: 0.4 * np.cos(x) + 0.5, color=WHITE)

        #Convert every dx=pi to a part in the height profile
        #with h=lambda*N/2n
        l = 520 #wavelengt [nm]
        n = 1.434  #refractive index [-]
        for N in np.arange(0, 4, 0.5):

            #y = lambda x: np.mod(l * x / (2 * n), np.pi) + l * N / (2 * n)
            y = lambda x: l * x / (2 * n * 10000)
            plots += plot_axes.plot(y, color=WHITE, use_smoothing=False
            )

        extras = VGroup()
        extras += plot_axes.get_horizontal_line(plot_axes.c2p(1, 1, 0), color=BLUE)
        extras += plot_axes.get_vertical_line(plot_axes.c2p(1, 1, 0), color=BLUE)
        #extras += Dot(point=plot_axes.c2p(1, 1, 0), color=YELLOW)
        title = Title(
            r"Plotting Intensity profiles and corresponding height profile",
            include_underline=False,
            font_size=40,
        )

        self.play(Write(title))
        self.play(Create(plot_axes), Create(plot_labels), Create(extras))
        self.play(AnimationGroup(*[Create(plot) for plot in plots], lag_ratio=0.05))


class SineCurveUnitCircle(Scene):
    # contributed by heejin_park, https://infograph.tistory.com/230
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6,0,0])
        x_end = np.array([6,0,0])

        y_start = np.array([-4,-2,0])
        y_end = np.array([-4,2,0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4,0,0])
        self.curve_start = np.array([-3,0,0])

    def add_x_labels(self):
        x_labels = [
            MathTex(r"\pi"), MathTex(r"2 \pi"),
            MathTex(r"3 \pi"), MathTex(r"4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x,y,0]), color=YELLOW_A, stroke_width=2 )


        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)


class SinToLinear(Scene):
    def construct(self):
        self.camera.frame_height = 8
        self.camera.frame_width = 14

        # Define Axes
        axes = Axes(
            x_range=[0, 6 * PI, PI],  # X-axis goes from 0 to 6π
            y_range=[-1.5, 20, 2],  # Y-axis range to accommodate both graphs
            axis_config={"color": WHITE}
        )

        # Labels for Axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # Graph A: Sine-like Curve (Cosine function)
        graph_a = axes.plot(lambda x: np.cos(x), color=BLUE)
        graph_a_label = axes.get_graph_label(graph_a, label="\\cos(x)", x_val=5)

        # Graph B: Linear Function y = 3x
        graph_b = axes.plot(lambda x: 3 * x, color=RED)
        graph_b_label = axes.get_graph_label(graph_b, label="3x", x_val=5)

        # Create segments for transformation
        num_segments = 6
        segment_length = PI
        segments = []
        transformed_segments = []

        for i in range(num_segments):
            x_start = i * segment_length
            x_end = (i + 1) * segment_length

            # Create a segment of the sine curve
            segment = axes.plot(lambda x: np.cos(x),
                                x_range=[x_start, x_end],
                                color=BLUE, stroke_width=4)
            segments.append(segment)

            # Corresponding segment on the linear graph
            transformed_segment = axes.plot(lambda x: 3 * x,
                                            x_range=[x_start, x_end],
                                            color=RED, stroke_width=4)
            transformed_segments.append(transformed_segment)

        # Add everything to the scene
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph_a), Write(graph_a_label))
        self.wait(1)

        # Animate each segment transforming
        for i in range(num_segments):
            self.play(Transform(segments[i], transformed_segments[i]), run_time=1.5)

        self.play(Write(graph_b_label))
        self.wait(2)

class SinToLinearSeparateAxes(Scene):
    def construct(self):
        self.camera.frame_height = 8
        self.camera.frame_width = 14

        # Define Axes for the Sine-like Graph (Top Graph)
        axes_a = Axes(
            x_range=[0, 6 * PI, PI],
            y_range=[-1.5, 1.5, 1],
            axis_config={"color": WHITE}
        ).shift(UP * 2)  # Move the sine graph upwards

        # Define Axes for the Linear Graph (Bottom Graph)
        axes_b = Axes(
            x_range=[0, 6 * PI, PI],
            y_range=[0, 20, 5],
            axis_config={"color": WHITE}
        ).shift(DOWN * 2)  # Move the linear graph downwards

        # Labels
        x_label_a = axes_a.get_x_axis_label("x")
        y_label_a = axes_a.get_y_axis_label("y")
        x_label_b = axes_b.get_x_axis_label("x")
        y_label_b = axes_b.get_y_axis_label("y")

        # Graph A: Sine-like Curve
        graph_a = axes_a.plot(lambda x: np.cos(x), color=BLUE)
        graph_a_label = axes_a.get_graph_label(graph_a, label="\\cos(x)", x_val=5)

        # Graph B: Linear Function y = 3x
        graph_b = axes_b.plot(lambda x: 3 * x, color=RED)
        graph_b_label = axes_b.get_graph_label(graph_b, label="3x", x_val=5)

        # Create segments for transformation
        num_segments = 6
        segment_length = PI
        segments = []
        transformed_segments = []

        for i in range(num_segments):
            x_start = i * segment_length
            x_end = (i + 1) * segment_length

            # Create a segment of the sine curve
            segment = axes_a.plot(lambda x: np.cos(x),
                                  x_range=[x_start, x_end],
                                  color=BLUE, stroke_width=4)
            segments.append(segment)

            # Corresponding segment on the linear graph
            transformed_segment = axes_b.plot(lambda x: 3 * x,
                                              x_range=[x_start, x_end],
                                              color=RED, stroke_width=4)
            transformed_segments.append(transformed_segment)

        # Add axes and labels
        self.play(Create(axes_a), Write(x_label_a), Write(y_label_a))
        self.play(Create(axes_b), Write(x_label_b), Write(y_label_b))

        # Show Graph A
        self.play(Create(graph_a), Write(graph_a_label))
        self.wait(1)

        # Animate each segment moving and transforming
        for i in range(num_segments):
            self.play(segments[i].animate.move_to(axes_b.c2p((i + 0.5) * segment_length, 3 * ((i + 0.5) * segment_length))),
                      Transform(segments[i], transformed_segments[i]), run_time=1.5)

        self.play(Write(graph_b_label))
        self.wait(2)


#TODO next step: incorporate actual data Intensity profile & corresponding height profile
class SinToLinearSeparateAxes2(Scene):
    def construct(self):

        thickness_offset = 120 #TODO implement thickness offset

        # Adjust camera view to ensure everything is visible
        self.camera.frame_height = 14  # Adjust height of frame to fit both graphs      12
        self.camera.frame_width = 15

        # Define Axes for the Sine-like Graph (Bottom Graph)
        axes_a = Axes(
            x_range=[0, 6 * 3.14, 3.14],
            y_range=[0, 1, 0.5],
            axis_config={"color": WHITE},
            x_length=10,
            y_length=3,
            x_axis_config={"numbers_to_include": np.arange(0, 3.14 * 6, 3.14)},
            y_axis_config={"numbers_to_include": np.arange(0, 1, 0.5)},
        ).shift(DOWN * 3)  # Move the cosine graph downwards

        # Define Axes for the Linear Graph (Top Graph)
        axes_b = Axes(
            x_range=[0, 6 * 3.14, 3.14],
            y_range=[0, 3.14 * 3 * 7, 3.14 * 3],
            axis_config={"color": WHITE},
            x_length=10,
            y_length=7,
            #x_axis_config={"numbers_to_include": np.arange(0, 3.14 * 6, 3.14)},
            y_axis_config={"numbers_to_include": np.arange(0, 3.14 * 3 * 6, 10)},
        ).shift(UP * 3)  # Move the linear graph upwards

        # Labels
        x_label_a = axes_a.get_x_axis_label("Distance [rad]").shift(DOWN*2)
        y_label_a = axes_a.get_y_axis_label("Intensity [-]").shift(LEFT * 6, DOWN*2).rotate(0.5*PI)  # Move the label left & rotate 90 deg
        x_label_b = axes_b.get_x_axis_label("")  # Move
        y_label_b = axes_b.get_y_axis_label("Height [nm]").shift(LEFT * 6, DOWN*1).rotate(0.5*PI)  # Move the top graph left & rotate 90 deg

        # Graph A: Sine-like Curve
        graph_a = axes_a.plot(lambda x: 0.4*np.cos(x) + 0.5, color=BLUE)
        graph_a_label = axes_a.get_graph_label(graph_a, label="a cos(x) + b", x_val=5).shift(RIGHT*3.8, UP*1.25)

        # Graph B: Linear Function y = 3x
        graph_b = axes_b.plot(lambda x: 3 * x, color=RED)
        graph_b_label = axes_b.get_graph_label(graph_b, label="3x", x_val=5)

        # Create segments for transformation
        num_segments = 6
        segment_length = PI
        segments = []
        transformed_segments = []

        for i in range(num_segments):
            x_start = i * segment_length
            x_end = (i + 1) * segment_length

            # Create a segment of the sine curve
            segment = axes_a.plot(lambda x: 0.4*np.cos(x) + 0.5,
                                  x_range=[x_start, x_end],
                                  color=BLUE, stroke_width=4)
            segments.append(segment)

            # Corresponding segment on the linear graph
            transformed_segment = axes_b.plot(lambda x: 3 * x,            #Was 1.5*x??
                                              x_range=[x_start, x_end],
                                              color=RED, stroke_width=4)
            transformed_segments.append(transformed_segment)

        # Add axes and labels
        self.play(Create(axes_a), Write(x_label_a), Write(y_label_a))
        self.play(Create(axes_b), Write(x_label_b), Write(y_label_b))

        # Show Graph A
        self.play(Create(graph_a), Write(graph_a_label))
        self.wait(1)

        # Animate each segment moving and transforming
        for i in range(num_segments):
            self.play(segments[i].animate.move_to(axes_b.c2p((i + 0.5) * segment_length, 3 * ((i + 0.5) * segment_length))),
                      Transform(segments[i], transformed_segments[i]), run_time=1.5)

        self.play(Write(graph_b_label))
        self.wait(2)
