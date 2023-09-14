from manimlib import *


def lerp_color(color1, color2, t):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    interpolated_r = float(r1 + (r2 - r1) * t)
    interpolated_g = float(g1 + (g2 - g1) * t)
    interpolated_b = float(b1 + (b2 - b1) * t)

    return interpolated_r, interpolated_g, interpolated_b


def pulse(t, a, f) -> float:
    r = a * np.sin(f * TAU * t)
    if r == 0:
        return 0.0001
    else:
        return r


def lerp(a, b, t) -> float:
    return a + (b - a) * t


def inv_lerp(a, b, v) -> float:
    return (v - a) / (b - a)


PURE_RED: str = "#FF0000"
PURE_GREEN: str = "#00FF00"


class Lerp(Scene):
    def construct(self) -> None:
        # Create a white rectangle
        color = Color()
        red = Color('red').get_rgb()
        blue = Color('green').get_rgb()
        t = ValueTracker(0)
        health_txt = Text("Health Bar", font_size=40).set_color(GREEN)
        label_txt = Text("Health bar with LERP").set_color(BLACK)
        zero = TexText(r"0\%").set_color(PURE_RED)
        hundred = TexText(r"100\%").set_color(PURE_GREEN)

        box = Rectangle(color=WHITE)
        health_txt.move_to(box)
        zero.next_to(box, LEFT)
        hundred.next_to(box, RIGHT)
        moving_box = Rectangle(
            width=0.000,
            height=0.0,
        )
        self.play(Write(label_txt))
        self.play(
            label_txt.animate.move_to(2.5 * UP).set_color(PURE_GREEN),
            rate_func=smooth,
            run_time=3
        )
        self.play(FadeIn(box), FadeIn(health_txt), FadeIn(moving_box))
        self.play(Write(zero), Write(hundred))

        def lerp_updater(obj):
            t_ = t.get_value()
            v = lerp(4, 0, t_)
            c1 = lerp_color(blue, red, t_)
            color.set_rgb(c1)
            health_txt.set_color(color)
            label_txt.set_color(color)
            obj.become(
                Rectangle(width=v, height=box.get_height(), fill_color=color, fill_opacity=1).align_to(box, LEFT),
            )

        moving_box.add_updater(lerp_updater)
        # self.play(Write(box), Write(moving_box))
        self.wait()
        # self.add(box, health_txt, moving_box)

        self.play(
            t.animate.set_value(1),
            run_time=20,
            rate_func=there_and_back,
        )
