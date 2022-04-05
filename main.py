from kivy.app import App
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

import numpy as np


from math_functions import find_vk


class MatrixScreen(Screen):
    matrix_input = ListProperty([])
    matrix_dimension = NumericProperty(2)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        n = self.matrix_dimension

        for i in range(n):
            row = []
            for j in range(n):
                element = MatrixElementInput(text="1")
                row.append(element)
            self.matrix_input.append(row)

        # Make a grid
        self.make_grid()

    def make_grid(self):
        """Creates a new grid with given matrix_input"""

        n = self.matrix_dimension

        grid = self.ids.matrix_grid
        grid.clear_widgets()

        for i in range(n):
            for j in range(n):
                grid.add_widget(self.matrix_input[i][j])


    def calculate_det(self):
        try:
            matrix = [[float(element.text) for element in line]
                      for line in self.matrix_input]
            answer = np.linalg.det(np.matrix(matrix))
            self.ids.answer_label.text = f"{answer:.4g}"
        except ValueError:
            self.ids.answer_label.text = "Непонятная матрица!"

    def increase_dimension(self):
        """Adds 1 to dimension"""

        self.matrix_dimension += 1

        # Add one element to each line
        for line in self.matrix_input:
            element = MatrixElementInput()
            line.append(element)

        # Add new line at the bottom
        row = []
        for j in range(self.matrix_dimension):
            element = MatrixElementInput()
            row.append(element)
        self.matrix_input.append(row)

        # Update grid
        self.make_grid()

    def decrease_dimension(self):
        """Subtracts 1 from dimension"""

        self.matrix_dimension -= 1

        # Add one element to each line
        for line in self.matrix_input:
            line.pop(-1)

        # Add new line at the bottom
        self.matrix_input.pop(-1)

        # Update grid
        self.make_grid()

    def start_jordan(self):
        """Starts process of finding jordan form"""
        matrix = [[float(element.text) for element in line]
                  for line in self.matrix_input]

        # Find jordan screen
        jordan_screen = self.manager.get_screen("jordan")
        self.manager.current = "jordan"

        # Set matrix
        jordan_screen.start(matrix)


class MatrixElementInput(TextInput):

    input_filter = 'float'
    halign = 'center'


class MenuScreen(Screen):
    pass


class JordanScreen(Screen):
    matrix = ListProperty([[1,0], [0,1]])

    def start(self, matrix):
        """Begins the process of jordan calculation"""

        # Save and draw the matrix
        self.matrix = matrix
        self.draw_matrix()

        # Find and output spectrum
        values, vectors = np.linalg.eig(matrix)
        spectrum = set(np.round(values, 12))
        self.ids.spectrum_label.text = f"Спектр: {spectrum}"

        # Find all V_k
        gen_eig_spaces = []
        for c in spectrum:
            gen_eig_spaces += find_vk(matrix, c)

        # Output V_k
        for space in gen_eig_spaces:
            text_item = Label(text=str(space), color=(1,1,1))
            self.ids.place_for_vk.add_widget(text_item)

    def draw_matrix(self):

        n = len(self.matrix)
        grid = self.ids.matrix_grid
        grid.clear_widgets()

        for i in range(n):
            for j in range(n):
                element = Label(text = f"{self.matrix[i][j]:.4g}",
                                color=(0,0,0),
                                font_size=30)
                grid.add_widget(element)




class AlgebraApp(App):

    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(MatrixScreen(name="matrix"))
        sm.add_widget(JordanScreen(name="jordan"))

        return sm



if __name__ == '__main__':
    app = AlgebraApp()
    app.run()


