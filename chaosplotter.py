import sys
import numpy as np
from numpy import fft
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from ui import createUI
import concurrent.futures as cf
from threading import Thread

# dft(x,=None): This function computes the discrete Fourier transform (DFT)
# of given input array x. It uses the fft function from the fft module of NumPy
# to compute the DFT, and then applies a frequency shift using fftshift. 
# The function then computes the absolute value and natural logarithm of the DFT coefficients.
# The norm argument is used to specify the normalization mode for the FFT.

def dft(x, norm=None):
    x = fft.fft(x, norm=norm)
    x = fft.fftshift(x)
    x = np.abs(x)
    x = np.log(x)
    return x

# iterate(function, R, P, iter_count, history=False): This function
# applies a given function function to a starting point P for a
# specified number of iterations iter_count. The function function 
# should take two arguments: a matrix R and a point P, and return 
# the updated point. If history=True, the function returns a flattened 
# array of all the intermediate points in the iteration.

def iterate(function, R, P, iter_count, history=False):
    if history:
        population = [P]
    for i in range(iter_count):
        P = function(R, P)
        if history:
            population.append(P)
    return np.array(population).ravel() if history else P

# Function class: This class defines a function object with a name,
# equation, and a function that computes the value of the function 
# for a given point. The limits attribute specifies the range of 
# valid inputs for the function. The __call__ method allows the class
# instance to be called like a regular function.

class Function:
    def __init__(self, name, equation, function, limits=(0.0, 1.0)):
        self.name = name
        self.equation = equation
        self.function = function
        self.limits = limits
        return

    def __call__(self, *args):
        return self.function(*args)

# This code defines a class named ChaosPlot that inherits from QMainWindow, 
# which is a part of the PyQt or PySide library for creating graphical user 
# interfaces Python. The class is used to create a main window for a plotting 
# application that displays chaotic functions.

# The ChaosPlotter class has a class level attribute PROBLEMS, 
# which is a list of Function objects. Each Function object is defined 
# by a tuple that contains the name of the function, its formula as a string, 
# a lambda function that represents the function, and a tuple of parameter values.

# The Function objects in the PROBLEMS list are:

# Function("stub", "Select...", lambda r, p: p, (0, 0)): 
# This is a placeholder function with the name "stub" and the formula "Select...". 
# It takes two parameters r and p, but it simply returns the second parameter p. 
# The tuple (0, 0) represents the default values for the parameters r and p.

# Function("logistic", "R \u00b7 P\u2099(1 - P\u2099)", lambda r, p: r * p * (1-p), (1, 4)): 
# This is the logistic function with the name "logistic" and the formula "R \u00b7 P\u2099(1 - P\u2099)". 
# It takes two parameters r and p, and it is represented by the lambda function lambda r, p: r * p * (1-p). 
# The tuple (1, 4) represents the default values for the parameters r and p.

# Function("sin", "R \u00b7 sin(P\u2099)", lambda r, p: r * np.sin(np.pi * p), (0.31, 1.0)): 
# This is the sine function with the name "sin" and the formula "R \u00b7 sin(P\u2099)". 
# It takes two parameters r and p, and it is represented by the lambda function lambda r, p: r * np.sin(np.pi * p). 
# The tuple (0.31, 1.0) represents the default values for the parameters r and p.

# Function("triangle", "R \u0394(P\u2099)", lambda r, p: r * np.minimum(p, 1-p), (1.0, 2.0)): 
# This is the triangle function with the name "triangle" and the formula "R \u0394(P\u2099)". 
# It takes two parameters r and p, and it is represented by the lambda function lambda r, p: 
# r * np.minimum(p, 1-p). The tuple (1.0, 2.0) represents the default values for the parameters r and p.

# The ChaosPlotter class uses these Function objects to create a plotting application that allows the user 
# to select a function and adjust its parameters to see how the function changes.




class ChaosPlotter(QMainWindow):
    PROBLEMS = [
        Function("stub", "Select...", lambda r, p: p, (0, 0)),
        Function("logistic", "R \u00b7 P\u2099(1 - P\u2099)", lambda r, p: r * p * (1-p), (1, 4)),
        Function("sin", "R \u00b7 sin(P\u2099)", lambda r, p: r * np.sin(np.pi * p), (0.31, 1.0)),
        Function("triangle", "R \u00b7 \u0394(P\u2099)", lambda r, p: r * np.minimum(p, 1-p), (1.0, 2.0)),
    ]

# This code defines a list of Function objects, where each function has a name, a LaTeX representation, 
# a Python function that computes the function's value, and a tuple specifying the function' domain.

# The Function objects in this list represent the following functions:

# population (P\u2099): This represents the population at a given time point. 
# The LaTeX representation uses the subscript notation P_ ninety nine to denote the population variable. 
# The Python function that computes the function's value is the identity function (lambda x: x), 
# which simply returns its input. The domain of this function is (0, 1), indicating that it takes a single argument between 0 and 1.

# fft(pop) (\u2131[P\u2099]): This represents the Fourier transform of the population function. 
# The LaTeX representation uses the Fourier transform symbol \u2131 followed by the population variable P_ ninety nine in square brackets.
# The Python function that computes the function's value is the dft function with the norm argument set to 'ortho'. 
# The dft function computes the discrete Fourier transform of its input. The domain of this function is (-10, 4), indicating that it takes a single argument between -10 and 4.

# diff (P\u2099\u208A\u2081 - P\u2099): This represents the difference between the population at the current time point and the population at the previous time point. 
# The LaTeX representation uses the difference symbol - followed by the population variable P_ ninety nine with the subtraction symbol \u208A\u2081 between the two occurrences of the variable. 
# The Python function that computes the function's value is the np.diff function, which computes the difference between consecutive elements of its input. The domain of this function is (-1, 1), 
# indicating that it takes a single argument that is a list or array with at least two elements.

# fft(diff) (\u2131[P\u2099\u208A\u2081 - P\u2099]): This represents the Fourier transform of the difference between the population at the current time point 
# and the population at the previous time point. The LaTeX representation uses the Fourier transform symbol \u2131 followed by the difference expression P_ ninety nine - P_ ninety nine\u208A\u2081 
# in square brackets. The Python function that computes the function's value is the dft function with the norm argument set to 'ortho', applied to the result of calling np.diff on its input. 
# The domain of this function is (-10, 4), indicating that it takes a single argument that is a list or array with at least two elements.




    PROCESSORS = [
        Function("population", "P\u2099", lambda x: x, (0, 1)),
        Function("fft(pop)", "\u2131[P\u2099]", lambda x: dft(x, norm='ortho'), (-10, 4)),
        Function("diff", "P\u2099\u208A\u2081 - P\u2099", lambda x: np.diff(x), (-1, 1)),
        Function("fft(diff)", "\u2131[P\u2099\u208A\u2081 - P\u2099]",
                 lambda x: dft(np.diff(x), norm='ortho'), (-10, 4)),
    ]

    def __init__(self):
        super().__init__()
        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.main.setLayout(createUI(self, self.PROBLEMS, self.PROCESSORS))
        self.r_slider.setMinimum(0)
        self.r_slider.setMaximum(10000)
        self.r_slider.setValue(5000)
        self.r_slider.setInterval(1, 4)
        self.r_slider.setEnabled(False)
        self.updateRfactor(self.r_slider)
        self.population_slider.setMinimum(0)
        self.population_slider.setMaximum(1000)
        self.population_slider.setValue(500)
        self.population_slider.setEnabled(False)
        self.updatePopulation(self.population_slider)
        self.doConnections()
        self.processor_index = 0
        self.problem_index = 0
        self.graph.adjust(left=0.02, right=0.99, top=0.975, bottom=0.075)
        return

    def updatePopulation(self, sender):
        self.population_label.setText("P = {}".format(round(sender.valueNormalized(), 2)))
        return

    def updateRfactor(self, sender):
        self.r_label.setText("R = {}".format(round(sender.valueNormalized(), 3)))
        return

    def refreshGraph(self):
        function = self.getCurrentFunction()
        P = np.array([self.population_slider.valueNormalized()])
        R = self.r_slider.valueNormalized()
        population = iterate(function, R, P, 5040, history=True)
        processor = self.getCurrentProcessor()
        y_val = processor(population)
        x_val = np.arange(0, len(y_val), 1)
        self.graph.clear()
        limits = processor.limits
        self.graph.axes.set_ylim(*limits)
        self.graph.plot(x_val, y_val, '.', markersize=4.0)
        self.graph.draw()

        self.plot.indicator(R)
        return

    def plotBifurcation(self):
        function = self.getCurrentFunction()
        r_limits = function.limits
        R_count = 110880  # refactor to settings
        # currently not supported:
        # splits > 1
        # splits is actually the number of jobs for a threadpool
        # severe bugs are present if splits is not 1
        # i literally have no idea how to fix it, bit this is fast enough
        splits = 1  # refactor to settings
        iter_count = 3000  # refactor to settings
        self.plot.clear()
        self.plot.axes.set_xlim(*r_limits)
        self.plot.axes.set_ylim(0.0, 1.0)
        self.plot.adjust(left=0.005, right=0.995, bottom=0.0, top=1.0)
        self.progress.setRange(0, splits)
        self.progress.setValue(0)
        self.progress.show()
        self.plot.indicator(self.r_slider.valueNormalized())
        Thread(target=self.makeplot, args=(self.plot, function, r_limits, R_count, splits, iter_count)).start()
        return

    def makeplot(self, plot, function, r_limits, R_count, splits, iter_count, callback=None):
        R = np.linspace(*r_limits, R_count)
        with cf.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(iterate, function, r, np.random.random(R_count // splits), iter_count, False): r
                for r in np.split(R, splits)
            }
            for future in cf.as_completed(futures):
                r = futures[future]
                p = future.result()
                plot.scatter(r, p, s=0.1, c='black')
                self.progress.setValue(self.progress.value() + 1)
                plot.draw_idle()
        return

    def handleFunctionChange(self, index):
        self.problem_index = index
        if index > 0:
            self.r_slider.setEnabled(True)
            self.population_slider.setEnabled(True)
            r_limits = self.getCurrentFunction().limits
            self.r_slider.setInterval(*r_limits)
            self.refreshGraph()
            self.plotBifurcation()
        else:
            self.r_slider.setEnabled(False)
            self.population_slider.setEnabled(False)
        return

    def handleProcessorChange(self, index):
        self.processor_index = index
        self.refreshGraph()
        return

    def doConnections(self):
        self.population_slider.valueChanged.connect(lambda t: self.updatePopulation(self.sender()))
        self.population_slider.valueChanged.connect(lambda t: self.refreshGraph())
        self.r_slider.valueChanged.connect(lambda t: self.updateRfactor(self.sender()))
        self.r_slider.valueChanged.connect(lambda t: self.refreshGraph())
        self.functions_cb.currentIndexChanged.connect(lambda t: self.handleFunctionChange(t))
        self.graph_cb.currentIndexChanged.connect(lambda t: self.handleProcessorChange(t))
        return

    def getCurrentFunction(self):
        return self.PROBLEMS[self.problem_index]

    def getCurrentProcessor(self):
        return self.PROCESSORS[self.processor_index]


if __name__ == "__main__":
    sys.argv[0] = "Chaos Plotter"
    qapp = QApplication(sys.argv)
    plotter = ChaosPlotter()
    plotter.show()
    qapp.exec()
