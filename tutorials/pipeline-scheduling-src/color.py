from enum import Enum, unique
import numpy as np

@unique
class Color(Enum) : 
    Red = 0 
    Orange = 1 
    Yellow = 2
    Green = 3
    Blue = 4
    Indigo = 5
    Violet = 6

    @classmethod
    def randn_color(cls) : 
        v = np.random.randn()
        c = next((c for c in Color if v < (0.65 * (float(c.value) - 2.5))), Color.Violet)
        return c