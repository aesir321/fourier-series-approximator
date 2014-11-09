from scipy.integrate import quad
import numpy as np

class Orthogonality:
    """
    This class is used to numerically calculate the inner product between two
    functions psi and phi.  It makes use of the quad function which uses the
    trapezoidal rule to evaluate the integrals.  It calculates the inner product
    over a fixed range of n values 0-5, enough to demonstrate orthogonality.
    """

    def __init__(self, function):
        self.function = function

    def inner_product(self, m, period):
        """
        Calculates the inner product of two functions and returns a list of
        evaluated results.
        """
        results = []
        integral = 0
        error = 0

        for i in range(0,6):
            if self.function == "psi_psi" and m == 0:
                integral, error = quad(self.multiply_half_psi, -1.0 * period, period, args=(i, m, period))
                results.append(integral*0.5)
            elif self.function == "psi_psi":
                integral, error = quad(self.multiply_psi_psi, -1.0 * period, period, args=(i, m, period))
                results.append(integral)
            elif self.function == "psi_phi":
                integral, error = quad(self.multiply_psi_phi, -1.0 * period, period, args=(i, m, period))
                results.append(integral)
            else:
                integral, error = quad(self.multiply_phi_phi, -1.0 * period, period, args=(i, m, period))
                results.append(integral)

        return results

    def psi(self, x, n, L):
        return np.cos(n * np.pi * x / L)

    def phi(self, x, n, L):
        return np.sin(n * np.pi * x / L)

    def multiply_half_psi(self, x, n, m, L):
        return 0.5 * self.psi(x, m, L)

    def multiply_psi_psi(self, x, n, m, L):
        return self.psi(x, n, L) * self.psi(x, m, L)

    def multiply_psi_phi(self, x, n, m, L):
        return self.psi(x, n, L) * self.phi(x, m, L)

    def multiply_phi_phi(self, x, n, m, L):
        return self.phi(x, n, L) * self.phi(x, m, L)
