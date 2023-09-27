from manimlib import *
import functools

# Colors in hex
PURE_RED: str = "#FF0000"
PURE_GREEN: str = "#00FF00"
PURE_BLUE: str = "#0000FF"
DARK_BLUE: str = "#236B8E"
MAROON_A: str = "#ECABC1"

color_array = [PURE_RED, PURE_GREEN, PURE_BLUE, MAROON_A]

A = np.array((-2., -8., 0.))
B = np.array((1., 2., 0.))
C = np.array((5., -5., 0.))
D = np.array((10, 2., 0.))
E = np.array((18, -8., 0.))

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

        lines = make_lines()
        fixed_dots_ = [Dot(radius=0.175, point=points[_]).set_color(ORANGE) for _ in range(len(points))]
        points_label_txt = [Text(labels[i]) for i in range(len(labels))]
        num_of_moving_dots = sum(len(lines) - i for i in range(len(lines)))
        moving_dots = [Dot(radius=0.15) for i in range(num_of_moving_dots)]
        dots = fixed_dots_ + moving_dots
        fixed_plus_moving_dots = []
        for dot in dots:
            fixed_plus_moving_dots.append(dot)

        self.play(
            *[Write(fixed_plus_moving_dots[i]) for i in range(len(fixed_plus_moving_dots))]
        )

        self.play(
            *[Write(lines[i].set_stroke(WHITE, 8)) for i in range(len(lines))]
        )

        # # TODO: Comments
        n = 0
        for i in range(len(lines)):
            lerps = lerps_at_step(len(lines), i)
            # print(lerps)
            for j in range(lerps):
                moving_dots[n + j].set_color(color_array[i])
            n = n + lerps


        # loop start = 5 loop_end=14
        fixed_dots_ = fixed_plus_moving_dots[:5]
        moving_dots_ = fixed_plus_moving_dots[5:]

        k = 0
        for i in range(len(lines)):
            lerps = lerps_at_step(len(lines), i)
            # print(lerps)
            for j in range(lerps):
                if i == 0:
                    print(k, j, j + 1)
                    moving_dots_[j].add_updater(
                        lambda obj, j=j: self.updater_wrapper(obj, fixed_dots_[j].get_center(),
                                                              fixed_dots_[j + 1].get_center()))
                # print(k - lerps - j - 1, k - lerps - j)
                else:
                    print(k, k - lerps - j - 1 + j, k - lerps)
                    moving_dots_[k].add_updater(
                        lambda obj, k=k, j=j, lerps=lerps: self.updater_wrapper(obj, moving_dots_[
                            k - lerps - 1].get_center(),
                            moving_dots_[k - lerps].get_center()))
                k = k + 1


        #  0 - 0 + i
        # moving_dots_[0].add_updater(
        #     lambda obj: self.updater_wrapper(obj, fixed_dots_[0].get_center(),
        #                                      fixed_dots_[1].get_center()))
        # moving_dots_[1].add_updater(
        #     lambda obj: self.updater_wrapper(obj, fixed_dots_[1].get_center(),
        #                                      fixed_dots_[2].get_center()))
        # moving_dots_[2].add_updater(
        #     lambda obj: self.updater_wrapper(obj, fixed_dots_[2].get_center(),
        #                                      fixed_dots_[3].get_center()))
        # moving_dots_[3].add_updater(
        #     lambda obj: self.updater_wrapper(obj, fixed_dots_[3].get_center(),
        #                                      fixed_dots_[4].get_center()))
        #
        #
        # 3 - 3 + i    (i - leprs - j )
        # moving_dots_[4].add_updater(
        #     lambda obj: self.updater_wrapper(obj, moving_dots_[0].get_center(),
        #                                      moving_dots_[1].get_center()))
        # moving_dots_[5].add_updater(
        #     lambda obj: self.updater_wrapper(obj, moving_dots_[1].get_center(),
        #                                      moving_dots_[2].get_center()))
        # moving_dots_[6].add_updater(
        #     lambda obj: self.updater_wrapper(obj, moving_dots_[2].get_center(),
        #                                      moving_dots_[3].get_center()))
        # 6 - 2 + i
        # moving_dots_[7].add_updater(
        #     lambda obj: self.updater_wrapper(obj, moving_dots_[4].get_center(),
        #                                      moving_dots_[5].get_center()))
        # moving_dots_[8].add_updater(
        #     lambda obj: self.updater_wrapper(obj, moving_dots_[5].get_center(),
        #                                      moving_dots_[6].get_center()))
        # 8 - 1 + i
        # moving_dots_[9].add_updater(
        #     lambda obj: self.updater_wrapper(obj, moving_dots_[7].get_center(),
        #                                      moving_dots_[8].get_center()))

        # Draw path
        dark_path1 = TracedPath(fixed_plus_moving_dots[-1].get_center).set_stroke(color=RED, width=13)
        self.add(dark_path1)

        self.play(self.t.animate.set_value(1), rate_func=there_and_back, run_time=5)
        # self.wait()
