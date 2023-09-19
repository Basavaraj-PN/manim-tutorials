from manimlib import *
import functools

# Colors in hex
PURE_RED: str = "#FF0000"
PURE_GREEN: str = "#00FF00"
PURE_BLUE: str = "#0000FF"
DARK_BLUE: str = "#236B8E"
MAROON_A: str = "#ECABC1"

color_array = [PURE_RED, PURE_GREEN, PURE_BLUE, MAROON_A]

A = np.array((-2., -2., 0.))
B = np.array((1., 2., 0.))
C = np.array((5., -5., 0.))
D = np.array((10, 2., 0.))
E = np.array((18, -2., 0.))

points = [A, B, C, D, E]
labels = ["A", "B", "C", "D", "E"]


def make_lines() -> []:
    lines = []
    for i in range(len(points) - 1):
        line = Line(points[i], points[i + 1])
        lines.append(line)

    return lines


def lerps_at_step(num_of_lines, i) -> int:
    return num_of_lines - i


class Bezier(Scene):

    def updater_wrapper(self, obj, start, end):
        alpha = self.t.get_value()
        interpolated_pos = interpolate(start, end, alpha)
        obj.move_to(interpolated_pos)

    def construct(self):
        self.t = ValueTracker(0)

        self.camera.frame.move_to(6 * RIGHT + 2 * DOWN)
        self.camera.frame.set_z(8)

        self.camera.background_color = BLUE

        lines = make_lines()
        fixed_dots = [Dot(radius=0.175).set_color(WHITE) for _ in range(len(points))]
        points_label_txt = [Text(labels[i]) for i in range(len(labels))]
        num_of_moving_dots = sum(len(lines) - i for i in range(len(lines)))
        moving_dots = [Dot(radius=0.15) for i in range(num_of_moving_dots)]

        welocome_text = Text("Beauty of Bézier curve", gradient=(PURE_RED, PURE_GREEN, PURE_BLUE, MAROON_A)).scale(3)
        welocome_text.next_to(LEFT_SIDE + 4 * RIGHT)
        self.play(Write(welocome_text))
        self.wait()
        self.play(FadeOut(welocome_text))

        self.play(
            *[Write(lines[i].set_stroke(BLACK, 10)) for i in range(len(lines))]
        )
        self.play(
            *[Write(fixed_dots[i].move_to(lines[i].get_start())) for i in range(len(lines))]
        )
        self.play(
            Write(Dot(radius=0.175).set_color(WHITE).move_to(lines[-1].get_end()))
        )
        self.play(
            *[Write(points_label_txt[i].next_to(lines[i].get_start(), LEFT)) for i in range(len(lines))]
        )
        self.play(
            Write(Text(labels[-1]).next_to(lines[-1].get_end(), LEFT))
        )

        # TODO: Comments
        n = 0
        for i in range(len(lines)):
            lerps = lerps_at_step(len(lines), i)
            for j in range(lerps):
                moving_dots[n + j].set_color(color_array[i])
            n = n + lerps

        # TODO: where to start moving dots initially?
        self.play(
            *[Write(moving_dots[i].move_to(LEFT * 100)) for i in range(num_of_moving_dots)]
        )

        # Lerp
        moving_dots[0].add_updater(lambda obj: self.updater_wrapper(obj, A, B))
        moving_dots[1].add_updater(lambda obj: self.updater_wrapper(obj, B, C))
        moving_dots[2].add_updater(lambda obj: self.updater_wrapper(obj, C, D))
        moving_dots[3].add_updater(lambda obj: self.updater_wrapper(obj, D, E))

        moving_dots[4].add_updater(
            lambda obj: self.updater_wrapper(obj, moving_dots[0].get_center(), moving_dots[1].get_center()))
        moving_dots[5].add_updater(
            lambda obj: self.updater_wrapper(obj, moving_dots[1].get_center(), moving_dots[2].get_center()))
        moving_dots[6].add_updater(
            lambda obj: self.updater_wrapper(obj, moving_dots[2].get_center(), moving_dots[3].get_center()))

        moving_dots[7].add_updater(
            lambda obj: self.updater_wrapper(obj, moving_dots[4].get_center(), moving_dots[5].get_center()))
        moving_dots[8].add_updater(
            lambda obj: self.updater_wrapper(obj, moving_dots[5].get_center(), moving_dots[6].get_center()))
        moving_dots[9].add_updater(
            lambda obj: self.updater_wrapper(obj, moving_dots[7].get_center(), moving_dots[8].get_center()))

        # path = [TracedPath(moving_dots[i].get_center).set_stroke(color=PINK) for i in range(len(moving_dots))]
        # self.add(*path)

        n = 0
        for i in range(len(lines)):
            lerps = lerps_at_step(len(lines), i)
            for j in range(lerps):
                moving_dots[n + j].set_color(color_array[i])
                path = TracedPath(moving_dots[n + j].get_center).set_stroke(color=color_array[i], width=5)
                self.add(path)
            n = n + lerps

        dark_path = TracedPath(moving_dots[-1].get_center).set_stroke(color=PINK, width=13)
        self.add(dark_path)
        # self.play(FadeOut(dark_path))

        self.play(self.t.animate.set_value(1), rate_func=there_and_back, run_time=15)
        # self.wait()
