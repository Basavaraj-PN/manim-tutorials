import numpy as np
from manimlib import *

# Colors in hex
PURE_RED: str = "#FF0000"
PURE_GREEN: str = "#00FF00"


def inv_lerp(start: float, end: float, value: float) -> float:
    """
    Performs inverse linear interpolation to calculate the fraction t.
    :param start: Start value.
    :param end: End value.
    :param value: Lerp value
    :return: Float (value - start) / (end - start)
    """
    return (value - start) / (end - start)


def inv_lerp_array(start_array: np.array([]), end_array: np.array([]), value):
    """
    Performs inverse lerp on array
    :param end_array: The start array.
    :param start_array: The end array.
    :param value: The value between start_array and end_array.
    :return: Inverse lerp value.
    """

    return (value - start_array) / (end_array - start_array)


def clamp(min_val: float, max_val: float, value: float) -> float:
    """
    Performs clamping within a specified range.
    :param min_val: The minimum allowed value.
    :param max_val: The maximum allowed value.
    :param value: The value to be clamped.
    :return: The clamped value.
    """
    return max(min(value, max_val), min_val)


class Sound(Scene):
    def construct(self) -> None:
        # Value tracker from x -> y.
        v = ValueTracker(10)

        # Define axis
        axes = Axes(x_range=[-5, 5], y_range=[-3, 7])
        labels = axes.get_axis_labels(x_label_tex="x", y_label_tex="y")

        self.play(Write(axes), Write(labels))

        # Create Dot.
        d = Dot()

        # Write objects
        self.play(Write(d))

        # Value updater function.
        def value_updater(obj):
            v_ = v.get_value()
            # print(inv_lerp_array(np.array([10, 10]), np.array([20, 20]), v_))
            d.move_to(LEFT * v_)

        d.add_updater(value_updater)

        self.play(
            v.animate.set_value(20),
            run_time=4,
            rate_func=there_and_back
        )
