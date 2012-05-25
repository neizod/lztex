# TODO replace EzMath's external call from Shell with pure Python parser.
import subprocess as sp
import re
 
class LzTeX:
    r_words = { 'TeX': r'\TeX',
                'LaTeX': r'\LaTeX{}',
                'LaTeX2e': r'\LaTeXe', }

    r_symbs = { r'\n': r'\newline', }
            
    def __init__(self, ezmath, profile='standard'):
        '''init parser class:
            - profile:
                - standard, strict on full syntax e.g. integral only.
                - unstrict, for backward comp e.g. int, integral, Integral'''
        self.profile = profile
        self.ezmath = ezmath
        self.schema = self.schema_maker()

    def schema_maker(self):
        schema = {}
        if self.profile == 'standard':
            schema['document'] = 'article'
        else:
            schema['document'] = 'report'
        return schema

    def parse(self, text):
        # TODO considered profile usage.

        # procedure:
        # - latex
        #   - sub 'text'  to  `text'
        #   - sub "text"  to  ``text''
        #   - sub ...  to  \ldots
        #   - sub $math$  to  $\math{}$  depends on ezmath
        text = re.sub(r'\$(.*)\$', self.parse_math, text)

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

    def parse_math(self, matched):
        return self.ezmath.parse(matched.group(1))

    def wrapper(self, text):
        # TODO considered profile usage.

        head = r'\documentclass{{{}}}'.format(self.schema['document'])
        begin = r'\begin{document}'
        end = r'\end{document}'
        return '\n'.join([head, begin, text, end])


class EzMath:
    def __init__(self, profile='standard'):
        '''init parser class'''
        self.profile = profile

    def parse(self, text):
        # FIXME call external EzMath lex/yacc prog.
        text = sp.Popen(['./ezmath', text], stdout=sp.PIPE).stdout.read().decode()

        # FIXME handle \begin{align} ... \end{align} error of external EzMath.
        text = re.sub(r'^\\begin{align}\n|\n\\end{align}\n$', '', text)

        return text.join('$$')

def main():
    # TODO init profile for parser.
    ezmath = EzMath()
    lztex = LzTeX(ezmath)

    plain = input()
    result = lztex.parse(plain)
    print(result)

if __name__ == '__main__':
    main()

