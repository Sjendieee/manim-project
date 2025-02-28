from scipy import np_maxversion
import manim as mn
from manim import *
config.media_width = "75%"
config.verbosity = "WARNING"

print(mn.__version__)

class ExperimentalDataAnimation(Scene):
    def construct(self):
        # Adjust camera view to ensure everything is visible
        self.camera.frame_height = 14  # Adjust height of frame to fit both graphs      12
        self.camera.frame_width = 15

        #Import experimental data
        fname = 'F:\\2023_11_13_PLMA_Dodecane_Basler5x_Xp_1_24S11los_misschien_WEDGE_v2\\Swellingimages\\data8min_anchor30_PureIntensity.csv'
        # df = pd.read_csv(fname)
        # x_data = df['xrange (pixels)']
        # y_data = df['Intensity converted (-)']
        # y_data_transformed = df['height (nm)']

        file = open(fname)
        csvreader = csv.reader(file)
        x_data = []
        y_data = []
        y_data_transformed = []
        for row in csvreader:
            try:
                x_data.append(float(row[0]))                   #distance [pixels]
                y_data.append(float(row[1]))                   #intensity [-]
                y_data_transformed.append(float(row[3]))       #height
            except:
                print("!Some value could not be casted to a float. Whether that is an issue or not is up to the user.!")
        file.close()

        # Create Axes for both graphs
        axes_a = Axes(
            x_range=[0, 700, 20], y_range=[0, 230, 1],
            axis_config={"color": BLUE}
        ).to_edge(DOWN)
        axes_b = Axes(
            x_range=[0, 700, 20], y_range=[0, np.max(y_data_transformed), np.max(y_data_transformed) // 5],
            axis_config={"color": GREEN}
        ).to_edge(UP)

        # Plot experimental data on Graph A
        graph_a = axes_a.plot_line_graph(x_data, y_data, add_vertex_dots=False, line_color=BLUE)

        # Placeholder for Graph B (initially empty)
        graph_b = VGroup()  # Will be populated in animation

        self.play(Create(axes_a), Create(axes_b))
        self.play(Create(graph_a))

        # Animate transferring segments from (a) to (b)
        seg_length = len(x_data)//5
        for i in range(0, len(x_data)-seg_length, seg_length):  # Take segments of 10 points
            segment_a = axes_a.plot_line_graph(
                x_data[i:i+seg_length], y_data[i:i+seg_length], add_vertex_dots=False, line_color=RED
            )
            segment_b = axes_b.plot_line_graph(
                x_data[i:i+seg_length], y_data_transformed[i:i+seg_length], add_vertex_dots=False, line_color=YELLOW
            )
            self.play(Transform(segment_a, segment_b), run_time=0.8)
            graph_b.add(segment_b)

        self.wait()

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