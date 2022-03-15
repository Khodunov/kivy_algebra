from kivy.app import App
from kivy.properties import ListProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

import numpy as np


class MatrixAnalysis(Widget):
    matrix_input = ListProperty([])

    def calculate_det(self):
        try:
            matrix = [[float(element.text) for element in line]
                      for line in self.matrix_input]
            answer = np.linalg.det(np.matrix(matrix))
            self.ids.answer_label.text = f"{answer:.2f}"
        except ValueError:
            self.ids.answer_label.text = "Непонятная матрица!"


class MatrixElementInput(TextInput):

    input_filter = 'float'
    halign = 'center'


class AlgebraApp(App):
    def build(self):
        return MatrixAnalysis()



if __name__ == '__main__':
    app = AlgebraApp()
    app.run()


