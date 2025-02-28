from matplotlib import pyplot as plt

import manim as mn
import numpy as np
import csv
import os
#import pandas as pd
from manim import *
from manim.utils.color.XKCD import ORANGERED


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
class SinToLinear_Function_model(Scene):
    #manim -pql .\main.py SinToLinearSeparateAxes2
    def construct(self):

        #Import experimental data
        df = pd.read_csv('F:\\2023_11_13_PLMA_Dodecane_Basler5x_Xp_1_24S11los_misschien_WEDGE_v2\\Swellingimages\\data8min_anchor30_PureIntensity.csv')
        x_distance = df['xrange (pixels)']
        y_intensity = df['Intensity converted (-)']
        y_height = df['height (nm)']

        thickness_offset = 120 #TODO implement thickness offset
        final_thickness = 700

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
            y_range=[thickness_offset - 10, final_thickness + 10, 100],
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


class ExperimentalDataAnimation(Scene):
    #manim -pql .\main.py SinToLinearSeparateAxes2
    def construct(self):
        # Import experimental data
        basepath = 'F:\\2025-01-30 PLMA-dodecane-Zeiss-Basler15uc-Xp1_32_BiBB4_tiltedplate-5deg-covered\\Swellingimages'
        fname = os.path.join(basepath, 'data28min 1s_anchor30_PureIntensity.csv')
        f_name_minmax = os.path.join(basepath, 'MinAndMaximaHandpicked264_1735_590.0211860602973_50.txt')
        file = open(fname)
        csvreader = csv.reader(file)
        x_distance = []
        y_intensity = []
        y_height = []
        for row in csvreader:
            try:
                x_distance.append(float(row[0]))  # distance [pixels]
                y_intensity.append(float(row[1]))  # intensity [-]
                y_height.append(float(row[3]))  # height
            except:
                print("!Some value could not be casted to a float. Whether that is an issue or not is up to the user.!")
        file.close()
        #Import extrema indexes
        minmax_ordered = [0]
        f = open(f_name_minmax, 'r')
        lines = f.readlines()
        for line in lines:
            data = line.split(',')
            minmax_ordered.append(int(data[0]))  # add already analyzed img nr's into a list, so later we can check if this analysis already exists
        minmax_ordered.append(len(y_intensity))

        # Adjust camera view to ensure everything is visible
        self.camera.frame_height = 14  # Adjust height of frame to fit both graphs      12
        self.camera.frame_width = 15

        # Define Axes for the Sine-like Graph (Bottom Graph)
        # Intensity vs distance
        axes_a = Axes(
            x_range=[0, max(x_distance), 100],
            y_range=[0, max(y_intensity)+10, 50],
            axis_config={"color": WHITE},
            x_length=10,
            y_length=3,
            x_axis_config={"numbers_to_include": np.arange(0, max(x_distance), 100)},
            y_axis_config={"numbers_to_include": np.arange(0, max(y_intensity)+10, 50)},
            tips=False
        ).shift(DOWN * 3)  # Move the cosine graph downwards

        # Define Axes for the Linear Graph (Top Graph)
        axes_b = Axes(
            x_range=[0, max(x_distance), 100],
            y_range=[150, max(y_height) + 10, 200],
            axis_config={"color": WHITE},
            x_length=10,
            y_length=7,
            #x_axis_config={"numbers_to_include": np.arange(0, 3.14 * 6, 3.14)},
            y_axis_config={"numbers_to_include": np.arange(150, max(y_height) + 10, 200)},
            tips=False
        ).shift(UP * 3)  # Move the linear graph upwards

        # Labels
        x_label_a = axes_a.get_x_axis_label(Text(r"Distance [pixels]", font_size=30)).shift(DOWN*2, LEFT*0.5)
        y_label_a = axes_a.get_y_axis_label(Text(r"Intensity [-]", font_size=30)).shift(LEFT * 5.15, DOWN*1.8).rotate(0.5*PI)  # Move the label left & rotate 90 deg
        x_label_b = axes_b.get_x_axis_label("")  # Move
        y_label_b = axes_b.get_y_axis_label(Text(r"Height [nm]", font_size=30)).shift(LEFT * 5.15, DOWN*1).rotate(0.5*PI)  # Move the top graph left & rotate 90 deg

        graph_a = axes_a.plot_line_graph(x_distance, y_intensity, add_vertex_dots=False, line_color=BLUE)
        # Placeholder for Graph B (initially empty)
        graph_b = VGroup()  # Will be populated in animation

        #graph_a_label = axes_a.get_graph_label(graph_a, label="Intensity profile", x_val=5).shift(RIGHT*3.8, UP*1.25)#TODO fix labels
        graph_a_label = Text(r"Experimental Intensity Profile", font_size=35).next_to(axes_a, UP, buff=0.1)
        graph_b_label = Text(r"Brush Height Profile", font_size=35).next_to(axes_b, UP, buff=-0.5)
        #graph_b_label = axes_b.get_graph_label(graph_b, label=Tex(r"$\lambda N / 2n$"), x_val=5)#TODO fix labels

        # Add axes and labels
        self.play(Create(axes_a), Write(x_label_a), Write(y_label_a), Write(graph_a_label))
        self.play(Create(axes_b), Write(x_label_b), Write(y_label_b), Write(graph_b_label))

        # Show Graph A
        self.play(Create(graph_a))
        self.wait(1)

        # Create dots for extrema (but don't show them yet)
        extrema_dots = [
            Dot(axes_a.coords_to_point(x_distance[i], y_intensity[i]), color=ORANGE).scale(1.1)
            for i in minmax_ordered[1:-1]
        ]
        # Animate extrema appearing one after another
        for dot in extrema_dots:
            self.play(FadeIn(dot), run_time=0.08)
        self.wait(1)

        # Animate transferring segments from (a) to (b)
        for i in range(0, len(minmax_ordered)-1):  # Take segments of 10 points
            r1 = minmax_ordered[i]
            r2 = minmax_ordered[i+1]+1
            segment_a = axes_a.plot_line_graph(
                x_distance[r1:r2], y_intensity[r1:r2], add_vertex_dots=False, line_color=BLUE
            )
            segment_b = axes_b.plot_line_graph(
                x_distance[r1:r2], y_height[r1:r2], add_vertex_dots=False, line_color=RED
            )
            self.play(Transform(segment_a, segment_b), run_time=0.8)
            graph_b.add(segment_b)

        self.wait(2)

#WOKRING: USE THIS ONE for animating experimental Intensity & height data!
class ExperimentalDataAnimationWhite(Scene):
    """
    Animate 2 graphs top,a = brush/drop height vs distance; bot,b Intensity vs distance.
    Import experimental data from csv. file. Import Extrema index locations from seperate (but corresponding!) .txt file.
    Set transition indices of dry brush - swollen brush - droplet yourself!


    Some text-locations in the graphs are hardcoded! Adjust as desired in code.
    """
    #uv run manim -pql .\main.py ExperimentalDataAnimationWhite
    config.background_color = WHITE
    def construct(self):
        # Import experimental data
        basepath = 'F:\\2025-01-30 PLMA-dodecane-Zeiss-Basler15uc-Xp1_32_BiBB4_tiltedplate-5deg-covered\\Swellingimages'
        fname = os.path.join(basepath, 'data28min 1s_anchor30_PureIntensity.csv')
        f_name_minmax = os.path.join(basepath, 'MinAndMaximaHandpicked264_1735_590.0211860602973_50.txt')

        # Define i1 and i2 as the index where the transitions happen
        i1 = 280  # Dry-swollen brush
        i2 = 590  # Swollen brush - droplet

        file = open(fname)
        csvreader = csv.reader(file)
        x_distance = []
        y_intensity = []
        y_height = []
        for row in csvreader:
            try:
                x_distance.append(float(row[0]))  # distance [pixels]
                y_intensity.append(float(row[1]))  # intensity [-]
                y_height.append(float(row[3]))  # height
            except:
                print("!Some value could not be casted to a float. Whether that is an issue or not is up to the user.!")
        file.close()
        #Import extrema indexes
        minmax_ordered = [0]
        f = open(f_name_minmax, 'r')
        lines = f.readlines()
        for line in lines:
            data = line.split(',')
            minmax_ordered.append(int(data[0]))  # add already analyzed img nr's into a list, so later we can check if this analysis already exists
        minmax_ordered.append(len(y_intensity))

        # Adjust camera view to ensure everything is visible
        self.camera.frame_height = 15  # Adjust height of frame to fit both graphs      12
        self.camera.frame_width = 13

        # Define Axes for the Sine-like Graph (Bottom Graph)
        # Intensity vs distance
        axes_a = Axes(
            x_range=[0, max(x_distance), 100],
            y_range=[0, max(y_intensity)+10, 50],
            axis_config={"color": BLACK},
            x_length=10,
            y_length=3,
            x_axis_config={"numbers_to_include": np.arange(0, max(x_distance), 100), "color": BLACK},
            y_axis_config={"numbers_to_include": np.arange(0, max(y_intensity)+10, 50), "color": BLACK},
            tips=False
        ).shift(DOWN * 3)  # Move the cosine graph downwards

        # Define Axes for the Linear Graph (Top Graph)
        axes_b = Axes(
            x_range=[0, max(x_distance), 100],
            y_range=[0, max(y_height) + 10, 200],
            axis_config={"color": BLACK},
            x_length=10,
            y_length=7,
            #x_axis_config={"numbers_to_include": np.arange(0, 3.14 * 6, 3.14)},
            y_axis_config={"numbers_to_include": np.arange(0, max(y_height) + 10, 200), "color": BLACK},
            tips=False
        ).shift(UP * 3)  # Move the linear graph upwards
        for tick in axes_a.x_axis.numbers + axes_a.y_axis.numbers:
            tick.set_color(BLACK)
        for tick in axes_b.y_axis.numbers:
            tick.set_color(BLACK)

        # Labels
        x_label_a = axes_a.get_x_axis_label(Text(r"Distance [pixels]", font_size=30, color=BLACK)).shift(DOWN*2, LEFT*0.5)
        y_label_a = axes_a.get_y_axis_label(Text(r"Intensity [-]", font_size=30, color=BLACK)).shift(LEFT * 5.15, DOWN*1.8).rotate(0.5*PI)  # Move the label left & rotate 90 deg
        x_label_b = axes_b.get_x_axis_label("")  # Move
        y_label_b = axes_b.get_y_axis_label(Text(r"Height [nm]", font_size=30, color=BLACK)).shift(LEFT * 5.15, DOWN*1).rotate(0.5*PI)  # Move the top graph left & rotate 90 deg

        graph_a = axes_a.plot_line_graph(x_distance, y_intensity, add_vertex_dots=False, line_color=BLUE)
        # Placeholder for Graph B (initially empty)
        graph_b = VGroup()  # Will be populated in animation

        graph_a_label = Text(r"Experimental Intensity Profile", font_size=35, color=BLACK).next_to(axes_a, UP, buff=0.1)
        graph_b_label = Text(r"Brush Height Profile", font_size=35, color=BLACK).next_to(axes_b, UP, buff=0.05)

        # Add axes and labels
        self.play(Create(axes_a), Write(x_label_a), Write(y_label_a), Write(graph_a_label))
        self.play(Create(axes_b), Write(x_label_b), Write(y_label_b), Write(graph_b_label))

        # Show Graph A
        self.play(Create(graph_a))
        self.wait(1)

        ################ Animate extrema appearing one after another ###############
        # Create dots for extrema (but don't show them yet)
        extrema_dots = [
            Dot(axes_a.coords_to_point(x_distance[i], y_intensity[i]), color=ORANGE).scale(1.1)
            for i in minmax_ordered[1:-1]
        ]
        # Animate extrema appearing one after another
        for dot in extrema_dots:
            self.play(FadeIn(dot), run_time=0.08)
        self.wait(1)

        ################ Animate transferring segments from (a) to (b) ###############
        for i in range(0, len(minmax_ordered)-1):  # Take segments of 10 points
            r1 = minmax_ordered[i]
            r2 = minmax_ordered[i+1]+1
            segment_a = axes_a.plot_line_graph(
                x_distance[r1:r2], y_intensity[r1:r2], add_vertex_dots=False, line_color=BLUE
            )
            segment_b = axes_b.plot_line_graph(
                x_distance[r1:r2], y_height[r1:r2], add_vertex_dots=False, line_color=RED
            )
            self.play(Transform(segment_a, segment_b), run_time=0.8)
            graph_b.add(segment_b)

        self.wait(2)

        ############## Animate linear fit on Droplet part
        # Get the two points (x1, y1) and (x2, y2)
        x1, y1 = x_distance[i2], y_height[i2]
        x2, y2 = x_distance[-1], y_height[-1]

        # Compute slope (m) and intercept (b) for y = mx + b
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        # Extend the x-range slightly beyond x1 & x2
        x_extra = (x2 - x1) * 0.1  # Extend by 10% of the segment length
        x_start = (y1/2 - b)/m  #x at half-height 0-y(swollenbrush-drop)
        x_end = x2 + x_extra

        # Compute corresponding y-values using y = mx + b
        y_start = m * x_start + b
        y_end = m * x_end + b

        fitted_line = axes_b.plot_line_graph(
            [x_end, x_start], [y_end, y_start], add_vertex_dots=False, line_color=ORANGERED, stroke_width=6
        )

        # Animate the line appearing from right to left
        self.play(Create(fitted_line), run_time=1.5, rate_func=linear)

        ############## Animate color backgrounds for Dry, Swollen & Droplet part ###############

        #####Dry - swollen brush
        x_values_brush = x_distance[:i1+1]  # Get corresponding x position
        y_values_brush = y_height[:i1+1]  # Corresponding Y values
        # Convert to scene coordinates
        brush_points = [axes_b.c2p(x, y) for x, y in zip(x_values_brush, y_values_brush)]
        # Add bottom boundary (close the polygon)
        bottom_left = axes_b.c2p(x_values_brush[0], 0)  # Lowest y in range
        bottom_right = axes_b.c2p(x_values_brush[-1], 0)
        # Create a filled shape for the brush region
        brush_fill_dry = Polygon(
            bottom_left, *brush_points, bottom_right, color=DARK_BLUE, fill_opacity=0.3, stroke_opacity=0
        )
        #####Dry - swollen brush
        x_values_brush = x_distance[i1:i2+1]  # Get corresponding x position
        y_values_brush = y_height[i1:i2+1]  # Corresponding Y values
        # Convert to scene coordinates
        brush_points = [axes_b.c2p(x, y) for x, y in zip(x_values_brush, y_values_brush)]
        # Add bottom boundary (close the polygon)
        bottom_left = axes_b.c2p(x_values_brush[0], 0)  # Lowest y in range
        bottom_right = axes_b.c2p(x_values_brush[-1], 0)
        # Create a filled shape for the brush region
        brush_fill_swollen = Polygon(
            bottom_left, *brush_points, bottom_right, color=BLUE, fill_opacity=0.3, stroke_opacity=0
        )
        #####Dry - swollen brush
        x_values_brush = x_distance[i2:]  # Get corresponding x position
        y_values_brush = y_height[i2:]  # Corresponding Y values
        # Convert to scene coordinates
        brush_points = [axes_b.c2p(x, y) for x, y in zip(x_values_brush, y_values_brush)]
        # Add bottom boundary (close the polygon)
        bottom_left = axes_b.c2p(x_values_brush[0], 0)  # Lowest y in range
        bottom_right = axes_b.c2p(x_values_brush[-1], 0)
        # Create a filled shape for the brush region
        brush_fill_droplet = Polygon(
            bottom_left, *brush_points, bottom_right, color=ORANGE, fill_opacity=0.3, stroke_opacity=0
        )

        # --- Position Text Labels Above Regions ---
        # Find the middle x-position of the Dry Brush region
        brush_x_center = (x_distance[0] + x_distance[i1]) / 2
        brush_y_top = max(y_height[:i1]) + 130  # Move text 30 units above max height
        dryBrush_text = Tex(r"\textbf{Dry brush}", font_size=35, color=DARK_BLUE).move_to(
            axes_b.c2p(brush_x_center, brush_y_top)
        )

        # Find the middle x-position of the Swollen Brush region
        droplet_x_center = (x_distance[i1] + x_distance[i2]) / 2
        droplet_y_top = max(y_height[i1:i2]) - 60
        swollenBrush_text = Tex(r"\textbf{Swollen Brush}", font_size=35, color=BLUE).move_to(
            axes_b.c2p(droplet_x_center, droplet_y_top)
        )
        # Find the middle x-position of the Droplet region
        droplet_x_center = (x_distance[i2]) - 40
        droplet_y_top = (max(y_height[i2:]) + min(y_height[i2:])) / 2
        droplet_text = Tex(r"\textbf{Droplet}", font_size=35, color=ORANGE).move_to(
            axes_b.c2p(droplet_x_center, droplet_y_top)
        )


        # Animate the shaded region appearing
        self.play(FadeIn(brush_fill_dry), FadeIn(dryBrush_text))
        self.play(FadeIn(brush_fill_swollen), FadeIn(swollenBrush_text))
        self.play(FadeIn(brush_fill_droplet), FadeIn(droplet_text))
        # # Get the x-coordinates for positioning the colored backgrounds
        # left_x = axes_b.c2p(0, 0)[0]  # Start of graph
        # split_x = axes_b.c2p(x_split, 0)[0]  # x position at i1
        # right_x = axes_b.c2p(max(x_distance), 0)[0]  # End of graph
        #
        # # Define Y positioning using axes_b bounds
        # y_center = axes_b.get_center()[1]  # Middle of the graph
        # y_top = axes_b.get_top()[1]  # Highest point
        # y_bottom = axes_b.get_bottom()[1]  # Lowest point
        #
        # # Create background rectangles
        # left_bg = Rectangle(
        #     width=split_x - left_x, height=axes_b.y_length, color=DARK_BLUE, fill_opacity=0.2
        # ).move_to([(left_x + split_x) / 2, y_center, 0])
        #
        # right_bg = Rectangle(
        #     width=right_x - split_x, height=axes_b.y_length, color=ORANGE, fill_opacity=0.2
        # ).move_to([(split_x + right_x) / 2, y_center, 0])
        #
        # # Adjust text positioning
        # brush_text = Text("(Swollen) Polymer Brush", font_size=25, color=BLACK).move_to(
        #     [(left_x + split_x) / 2, y_top - 0.5, 0]  # Shift text upward slightly
        # )
        #
        # droplet_text = Text("Droplet", font_size=25, color=BLACK).move_to(
        #     [(split_x + right_x) / 2, y_top - 0.5, 0]  # Shift text upward slightly
        # )
        #
        # # Animate the background and text appearing
        # self.play(FadeIn(left_bg), FadeIn(right_bg), Write(brush_text), Write(droplet_text))

        self.wait(2)