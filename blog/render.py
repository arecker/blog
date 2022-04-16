class Renderer:
    def __init__(self):
        self.text = ''

    def write(self,
              content: str,
              add_newline=True,
              add_blankline=False,
              indent_level=0):

        self.text += (' ' * indent_level) + content

        if add_newline:
            self.text += '\n'

        if add_blankline:
            self.write('')
