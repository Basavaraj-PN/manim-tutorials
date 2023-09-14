from manimlib import *


# Colors in hex
PURE_RED: str = "#FF0000"
PURE_GREEN: str = "#00FF00"


def lerp_color(color1, color2, t):
    """
    Linearly interpolate (lerp) between two RGB colors.
    Parameters:
    - color1 (tuple): A tuple representing the first RGB color (r, g, b).
    - color2 (tuple): A tuple representing the second RGB color (r, g, b).
    - t (float): A value between 0 and 1 representing the interpolation factor.

    Returns:
    - tuple: An RGB color tuple representing the interpolated color.
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    interpolated_r = float(r1 + (r2 - r1) * t)
    interpolated_g = float(g1 + (g2 - g1) * t)
    interpolated_b = float(b1 + (b2 - b1) * t)

    return interpolated_r, interpolated_g, interpolated_b


def pulse(t, a, f) -> float:
    """
    Generate a pulse signal with the given parameters.

    This function generates a pulse signal using the formula:
    pulse(t, a, f) = a * sin(2 * pi * f * t)

    Parameters:
    - t (float): The time value at which to evaluate the pulse signal.
    - a (float): The amplitude of the pulse.
    - f (float): The frequency of the pulse.

    Returns:
    - float: The value of the pulse signal at time t.

    If the computed value is exactly 0, it is replaced with a very small positive value (0.0001)
    to prevent division by zero or other issues.

    """

    r = a * np.sin(f * TAU * t)
    if r == 0:
        return 0.0001
    else:
        return r


def lerp(start: float, end: float, t: float) -> float:
    """
    Linearly interpolate (lerp) function.
    Parameters:
        - start(float): Start value.
        - end(float): End value.
        - t(float): Fraction between 0.0 to 1.0.

    Returns:
        - float: interpolated value between start and end.
    """
    return start + (end - start) * t


def inv_lerp(start:float, end: float, value: float) -> float:
    """
    Performs inverse linear interpolation to calculate the fraction t.
    :param start: Start value.
    :param end: End value.
    :param value: Float from lerp function
    :return: Float (value - start) / (end - start)
    """
    return (value - start) / (end - start)


class Lerp(Scene):
    def construct(self) -> None:

        # Empty color object for color operation.
        color = Color()

        # Create a white rectangle
        red = Color('red').get_rgb()
        blue = Color('green').get_rgb()

        # value tracker from 0 -> 1.
        t = ValueTracker(0)

        # Labels.
        health_txt = Text("Health Bar", font_size=40).set_color(GREEN)
        label_txt = Text("Health bar with LERP").set_color(BLACK)
        zero = TexText(r"0\%").set_color(PURE_RED)
        hundred = TexText(r"100\%").set_color(PURE_GREEN)
        t_label_txt = Text("t = 1.0")

        # Create shapes.
        box = Rectangle(color=WHITE)
        # This is the moving box and width will change.
        moving_box = Rectangle(width=0.000, height=0.0)

        # Align the text label appropriately.
        health_txt.move_to(box)
        zero.next_to(box, LEFT)
        hundred.next_to(box, RIGHT)
        t_label_txt.next_to(box, BOTTOM)

        # Animate the label texts and shapes
        self.play(FadeIn(label_txt))
        self.play(
            label_txt.animate.move_to(2.5 * UP).set_color(PURE_GREEN),
            rate_func=smooth,
            run_time=3
        )
        self.play(FadeIn(box), FadeIn(health_txt), FadeIn(moving_box))
        self.play(Write(zero), Write(hundred), FadeIn(t_label_txt))

        # t label updater
        def t_label_updater(obj):
            t_ = t.get_value()
            obj.become(Text(f"t = {round((1 -t_), 2)}").next_to(box, BOTTOM))

        # Lerp updater
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
        t_label_txt.add_updater(t_label_updater)
        moving_box.add_updater(lerp_updater)
        self.wait()

        # Finally animate t value tracker from 0 to 1.
        self.play(
            t.animate.set_value(1),
            run_time=20,
            rate_func=there_and_back,
        )
