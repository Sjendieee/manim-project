from scipy import np_maxversion
from manim import *

class IntensityToHeight(Scene):
    def construct(self):
        plot_axes = Axes(
            x_range=[0, np.pi*6, 0.5*np.pi],
            y_range=[0, np.pi*6, 0.5*np.pi],
            x_length=9,
            y_length=5.5,
            axis_config={
                "numbers_to_include": np.arange(0, 1 + 0.1, 0.1),
                "font_size": 24,
            },
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
            y = np.arange( l * N / (2 * n), l * (N+0.5) / (2 * n), 100)
            plots += plot_axes.plot(y, color=WHITE, use_smoothing=False
            )

        extras = VGroup()
        extras += plot_axes.get_horizontal_line(plot_axes.c2p(1, 1, 0), color=BLUE)
        extras += plot_axes.get_vertical_line(plot_axes.c2p(1, 1, 0), color=BLUE)
        extras += Dot(point=plot_axes.c2p(1, 1, 0), color=YELLOW)
        title = Title(
            r"Plotting Intensity profiles & corresponding height profile",
            include_underline=False,
            font_size=40,
        )

        self.play(Write(title))
        self.play(Create(plot_axes), Create(plot_labels), Create(extras))
        self.play(AnimationGroup(*[Create(plot) for plot in plots], lag_ratio=0.05))