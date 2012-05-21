class LzTeX:
    r_words = { 'TeX': r'\TeX',
                'LaTeX': r'\LaTeX{}',
                'LaTeX2e': r'\LaTeXe', }

    r_symbs = { r'\n': r'\newline', }
            
    def __init__(self, profile='standard'):
        '''init parser class:
            - profile:
                - standard, strict on full syntax e.g. integral only.
                - unstrict, for backward comp e.g. int, integral, Integral'''
        self.profile = profile

    def parse(self, text):
        # TODO considered profile usage.

        # procedure:
        # - latex
        #   - sub 'text'  to  `text'
        #   - sub "text"  to  ``text''
        #   - sub ...  to  \ldots
        #   - sub $math$  to  $\math{}$  depends on ezmath
        #
        # - markdown
        #   - sub *text*  to  <i>text</i>
        #   - sub **text**  to  <b>text</b>
        #   - sub _text_  to  <u>text</u>
        #
        #   - sub markdown bullet  to  \begin{itemize} \item text \end{itemize}
        #   - sub markdown numlet  to  \begin{enumerate} \item text \end{...}
        #
        #   - sub [name](link)  to  name
        #   - sub [^num] ... [num] text  to  \footnote{text}
        #   - sub 

        # after finish sub all of those, wrap it with latex.
        text = self.wrapper(text)
        return text

    def wrapper(self, text):
        # TODO considered profile usage.

        head = r'\documentclass{article}'
        begin = r'\begin{document}'
        end = r'\end{document}'
        return '\n'.join([head, begin, text, end])


def main():
    # TODO init profile for parser.
    lztex = LzTeX()

    plain = input()
    result = lztex.parse(plain)
    print(result)

if __name__ == '__main__':
    main()

