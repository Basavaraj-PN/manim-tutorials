from manimlib import *

# Colors in hex
PURE_RED: str = "#FF0000"
PURE_GREEN: str = "#00FF00"


def inv_lerp(start:float, end: float, value: float) -> float:
    """
    Performs inverse linear interpolation to calculate the fraction t.
    :param start: Start value.
    :param end: End value.
    :param value: Float from lerp function
    :return: Float (value - start) / (end - start)
    """
    return (value - start) / (end - start)


def clamp(min_val: float, max_val: float, value:float) ->float:
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

        # Create Dot.
        d = Dot()

        # Write objects
        self.play(Write(d))

        # Value updater function.
        def value_updater(obj):
            v_ = v.get_value()

        d.add_updater(value_updater)

        self.play(
            v.animate.set_value(20),
            run_time=4,
            rate_func=there_and_back
        )
