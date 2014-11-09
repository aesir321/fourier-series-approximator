import numpy as np
from math import fabs, floor, ceil

class FourierSeries:
    def __init__(self):
        pass


    def frac(self, x):
        # TODO: Assert x is a real number.

        """
        Returns the fractional part of a real number x.

        x -: The real number to take the fractional part of.


        """

        temp = 0
        if x >= 0:
            temp = x - floor(x)
        else:
            temp = x - ceil(x)
        return temp

    def calc_triangle(self):
        """
        TODO: Documentation
        """

        x = np.arange(0, 2, 0.01)
        y = np.zeros_like(x)
        period = len(x)

        for i in range(0, period):
            y[i] = 1 - fabs(4 * (0.5 - self.frac((0.5 * x[i]) + 0.25)))
        return x, y

    def fs_calc_triangle(self, n):
        x = np.arange(0.0, 2, 0.01)
        y = np.zeros_like(x)

        for i in range(1, n+2, 2):
            y += ((-1.)**((i-1.) / 2.) / (i**2)) * np.sin(i * np.pi * x / 1.)

        y *= 8.0/(np.pi**2)
        return x, y

    def calc_square(self):
        """
        TODO: Documentation
        """
        x = np.arange(0,2 * np.pi,0.01)
        y = np.zeros_like(x)

        for i in range(0, len(x)):
            if x[i] <= np.pi:
                y[i] = 1
            else:
                y[i] = -1

        return x, y

    def fs_calc_square(self, n):
        """
        This function approximates a square wave using a fourier series.

        n -: This is the amount of terms you wish to sum to.

        """
        x = np.arange(0.0,2*np.pi,0.01)
        y = np.zeros_like(x)

        for i in range(1,n+2,2):
            y += (((np.sin(i*x))/i))

        y *= 4.0/np.pi
        return x, y

    def calc_saw(self):
        x = np.arange(0,2 * np.pi,0.01)
        y = np.zeros_like(x)

        for i in range(0, len(x)):
            if x[i] <= np.pi:
                y[i] = x[i]
            elif x[i] > np.pi and x[i] % np.pi != 0:
                y[i] = x[i] - np.pi
            else:
                y[i] = 0
        return x, y

    def fs_calc_saw(self, n):
        """
        This function approximates a saw tooth wave using a fourier seriers.

        self -: This is the amount of terms you wish to use to approximate it with.

        """

        x = np.arange(0.0, 2*np.pi, 0.01)
        y = np.zeros_like(x)
        y += np.pi/2.0

        for i in range(1,n+2,1):
            y += -np.sin(2.0*i*x)/i
        return x, y
