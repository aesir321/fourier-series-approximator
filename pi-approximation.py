import matplotlib.pyplot as plt
from math import pi

class Parseval:
    
    def compute_pi(self, n):
        pi_approx = 0.0
        for i in range(1, n+1):
            pi_approx += (1.0 / (i**2))
        pi_approx *= 6
        return pi_approx**.5
    
    def plot_pi(self, n):
        x, y = [], []
        for i in range(1, n+1):
            x.append(self.compute_pi(i))
            y.append(i)
        return x, y

