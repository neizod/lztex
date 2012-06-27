# FIXME
# - check why slash something (e.g. \abcdefg) doesn't raise a parser error,
#   but pass silently (and seems to work?).
# - in ezmath's text, why regex fail for open group?
# - newline?
# - positioning a[1][2][3] -> _{2}^{3}a_{1}

import argparse

def get_shell_args():
    '''Get command line arguments for initialize program'''
    # TODO write a user-friendly description

    parser = argparse.ArgumentParser(description="(a desc to this prog)")
    parser.add_argument('files', metavar='FILE', nargs='*',
                        type=argparse.FileType('r'),
                        help='(input file help desc)')
    args = parser.parse_args()

    return args


###############################################################################

from ply.lex import TOKEN
from re import escape

symbol = { r'+':    r'+',
           r'-':    r'-',
           r'*':    r'\times',
           r'.':    r'\cdot',

           r'(+)':   r'\oplus',
           r'(-)':   r'\ominus',
           r'(*)':   r'\otimes',
           r'(.)':   r'\odot',
           r'(\*)':  r'\circleast',
           r'(\/)':  r'\oslash',

           r'+-':    r'\pm',
           r'-+':    r'\mp',

           r'~':     r'\sim',

           r'||':    r'\|',
           r'|':     r'|',

           r"'":    r"'",
           r':':    r':',
           r'!':    r'!',
           r'@':    r'@',
           r'?':    r'?',
           r'%':    r'\%',
           r'&':    r'\&',

           r'\*':   r'*',
           r'\.':   r'.',
           r'\,':   r',',
           r'\;':   r';',
           r'\/':   r'\div',
           r'\^':   r'\^',
           r'\$':   r'\$',
           r'\\':   r'\setminus',

           # ================================

           r'=':      r'=',
           r'==':     r'\equiv',
           r'~=':     r'\cong',
           r'~~':     r'\approx',
           r'propto': r'\propto',
           r'!=':     r'\neq',
           r'<':      r'\lt',
           r'>':      r'\gt',
           r'<<':     r'\ll',
           r'>>':     r'\gg',
           r'<=':     r'\leq',    # '=<' like haskell due to arrow conflict
           r'>=':     r'\geq',
           r'-<':     r'\prec',
           r'>-':     r'\succ',

           r'and':    r'\land',
           r'or':     r'\lor',
           r'not':    r'\neg',
           r'<->':    r'\leftrightarrow',
           r'<-->':   r'\longleftrightarrow',
           r'->':     r'\rightarrow',
           r'-->':    r'\longrightarrow',
           r'<-':     r'\leftarrow',
           r'<--':    r'\longleftarrow',
           r'<=>':    r'\Leftrightarrow',
           r'<==>':   r'\Longleftrightarrow',
           r'=>':     r'\Rightarrow',
           r'==>':    r'\Longrightarrow',
           #'<=':     r'\Leftarrow',       # see above
           r'<==':    r'\Longleftarrow',
           r'|->':    r'\mapsto', 

           r'...':    r'\ldots',

           r'infinity':   r'\infty',

           r'deg':   r'{^\circ}',     # degree?
           r'star':  r'\star',

           r'der':    r'\partial',
           r'nabla':  r'\nabla',          # grad?

           # force wrap this with \e ... \e ??
           r'for all':    r'\forall',
           r'exists':     r'\exists',
           r'in':         r'\in',
           r'not in':     r'\notin',
           r'subset':     r'\subseteq',
           r'superset':   r'\supseteq',

           r'union':      r'\cup',
           r'intersect':  r'\cap',

           r'empty':      r'\emptyset',
           r'Eset':       r'\varnothing',
           r'Nset':       r'\mathbb{N}',
           r'Zset':       r'\mathbb{Z}',
           r'Pset':       r'\mathbb{P}',
           r'Qset':       r'\mathbb{Q}',
           r'Rset':       r'\mathbb{R}',
           r'Cset':       r'\mathbb{C}',
           r'Hset':       r'\mathbb{H}',
           r'Aleph':      r'\aleph',       # lower case?
           r'Re':         r'\Re',
           r'Im':         r'\Im',

           r'hbar':       r'\hbar',
           r'ell':        r'\ell',
           r'inodot':     r'\imath',        # as original imath, jmath?
           r'jnodot':     r'\jmath',

           # TODO function names

           }

# FIXME use { ... } as set instead of tuple (ignore py26-- compatibility issue)
greek = ( r'alpha',
          r'beta',
          r'(G|g)amma',
          r'(D|d)elta',
          r'(var)?epsilon',
          r'zeta',
          r'eta',
          r'(T|(var)?t)heta',
          r'iota',
          r'kappa',
          r'(L|l)ambda',
          r'mu',
          r'nu',
          r'(X|x)i',
          r'omicron',
          r'(P|(var)?p)i',
          r'(var)?rho',
          r'(S|(var)?s)igma',
          r'tau',
          r'(U|u)psilon',
          r'(P|(var)?p)hi',
          r'chi',
          r'(P|p)si',
          r'(O|o)mega', )

matrix = ( r'matrix',
           r'borderless',
           r'parentheses',
           r'det',
           r'norm',
           r'cases',
           r'', )

function = ( r'abs',
             r'norm',
             r'bra',
             r'ket',
             r'braket',
             r'inner',
             r'floor',
             r'ceil',
             r'round',
             r'list',

             r'sqrt',
             r'dot',
             r'ddot',
             r'hat',
             r'vec',
             r'bar', )

summation = { r'Summation':  r'\sum',
              r'Product':    r'\prod',
              r'Coproduct':  r'\coprod',
              r'Union':      r'\bigcup',
              r'Intersect':  r'\bigcap',
              r'integral':   r'\int',
              # TODO \oint -> round integral,
              #      \iint -> double integral,
              #      \iiint -> tripple integral
              r'limit':      r'\lim',
              r'limit superior':     r'\limsup',
              r'limit inferior':     r'\liminf', }

sort_len = lambda x: -len(x)
repeat_num = lambda a: a[0] + r'\overline{' + a[1] + '}'
rm_parentheses = lambda t: t[6:-7] if t[:6] == r'\left(' and t[-7:] == r'\right)' else t

###############################################################################

tokens = (
        'CHARACTER',
        'NEWLINE',


        'BEGIN_EZMATH',
        'END_EZMATH',

        'SYMBOL',
        'GREEK',
        'ENGLISH',
        'NUMBER',
        'TEXT',

        'OP_MOD',
        'OP',
        'CP',
        'OB_MATRIX',
        'OB',
        'CB',
        'OS',
        'CS',

        'KW_DIVISION',
        'KW_POWER',
        'KW_CHOOSE',
        'KW_ROOT',

        'CONTROL',
        'FUNCTION',

        'SUMMATION',
        'FOR',
        'FROM',
        'TO',
)

states = (
        ('ezmath', 'exclusive'),
        ('matrix', 'inclusive'),
)

precedence = (
        ('left', 'KW_DIVISION'),
        ('right', 'SUMMATION'),
        ('right', 'FOR', 'FROM', 'TO'),
)


###############################################################################

def t_SYMBOL(t):   # TODO rename this not to make confuse with ezmath envoroinment.
    r'LzTeX|EzMath'
    if t.value == 'LzTeX':
        t.value = r'\LzTeX{}'
        flag.lztex_logo = True
    elif t.value == 'EzMath':
        t.value = r'\EzMath{}'
        flag.ezmath_logo = True
    return t

def t_CHARACTER(t):
    r'.'
    return t

def t_BEGIN_EZMATH(t):
    r'\n?\$'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_END_EZMATH(t):
    r'\$\n?'
    t.lexer.begin('INITIAL')
    return t

def t_NEWLINE(t):
    r'\n'
    return t


# Math lexer

def t_ezmath_matrix_OP_MOD(t):
    r'\([ \t]*mod'
    t.lexer.begin('matrix')
    t.value = 'pmod'
    return t

def t_ezmath_matrix_OP(t):
    r'\('
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_CP(t):
    r'\)'
    t.lexer.begin('ezmath')
    return t

@TOKEN(r'|'.join(escape(w) + r'\[' for w in sorted(matrix, key=sort_len)))
def t_matrix_OB_MATRIX(t):
    if 'parentheses' in t.value:
        t.value = 'pmatrix'
    elif 'borderless' in t.value:
        t.value = 'matrix'
    elif 'det' in t.value:
        t.value = 'vmatrix'
    elif 'norm' in t.value:
        t.value = 'Vmatrix'
    elif 'cases' in t.value:
        t.value = 'cases'
    else:
        t.value = 'bmatrix'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_OB(t):
    r'\['
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_CB(t):
    r'\]'
    t.lexer.begin('ezmath')
    return t

def t_ezmath_matrix_OS(t):
    r'\{'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_CS(t):
    r'\}'
    t.lexer.begin('ezmath')
    return t


def t_ezmath_matrix_KW_DIVISION(t):
    r'\/'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_KW_POWER(t):
    r'\^'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_KW_CHOOSE(t):
    r'choose'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_KW_ROOT(t):
    r'root'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_CONTROL(t):
    r',|;|\n+'
    t.lexer.begin('matrix')
    return t
#       t.lexer.lineno += t.value.count('\n')


@TOKEN(r'|'.join(escape(w) for w in sorted(summation.keys(), key=sort_len)))
def t_ezmath_matrix_SUMMATION(t):
    t.lexer.begin('matrix')
    t.value = summation[t.value]
    return t

def t_ezmath_matrix_FOR(t):
    r'for'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_FROM(t):
    r'from'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_TO(t):
    r'to'
    t.lexer.begin('matrix')
    return t


@TOKEN(r'|'.join(escape(w) for w in sorted(function, key=sort_len)))
def t_ezmath_matrix_FUNCTION(t):
    t.lexer.begin('matrix')
    return t

@TOKEN(r'|'.join(escape(w) for w in sorted(symbol.keys(), key=sort_len)))
def t_ezmath_matrix_SYMBOL(t):
    t.lexer.begin('ezmath')
    t.value = symbol[t.value]
    return t

@TOKEN(r'[ \t]')
def t_ezmath_matrix_WHITESPACE(t):
    t.lexer.begin('matrix')

@TOKEN(r'|'.join(w for w in sorted(greek, key=sort_len)))
def t_ezmath_matrix_GREEK(t):
    t.lexer.begin('ezmath')
    t.value = '\\' + t.value
    return t

def t_ezmath_matrix_ENGLISH(t):
    r'[a-zA-Z]'
    t.lexer.begin('ezmath')
    return t

def t_ezmath_matrix_NUMBER(t):
    r'[0-9]+\.[0-9]*(...)[0-9](...)|[0-9]+(\.[0-9]+(...)?)?'
    t.lexer.begin('ezmath')
    if t.value.count('.') == 7:
        t.value = repeat_num(t.value.rsplit('...'))
    return t

def t_ezmath_matrix_TEXT(t):
    r'"([^"\\]*?(\\.[^"\\]*?)*?)"'
    t.lexer.begin('ezmath')
    # TODO chk str identifier: frak"A" -> iden=frak, body=A
    t.value = r'\text{{{body}}}'.format(body=t.value[1:-1])
    return t



def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
lex.lex()


###############################################################################

def p_document(t):
    '''document : paragraph'''
    document = r'\documentclass{article}' + '\n'
    prerequisite = ''
    if flag.amsmath:
        prerequisite += r'\usepackage{amsmath}' + '\n'
    if flag.lztex_logo:
        # FIXME make use of its own class
        prerequisite += r'\usepackage{relsize}' + '\n'
        prerequisite += r'\newcommand{\LzTeX}{L\kern-.31em\lower-.47ex\hbox{\smaller{\smaller{Z}}}\kern-.09emT\kern-.16em\lower+.51ex\hbox{E}\kern-.27exX}' + '\n'
    if flag.ezmath_logo:
        # FIXME make use of its own class
        prerequisite += r'\usepackage{graphicx}' + '\n'
        prerequisite += r'\newcommand{\EzMath}{\(\mathcal{E}\)\kern-.18em\lower+.51ex\hbox{\(\mathcal{Z}\)}\kern-.18em\(\mathcal{M}\)\kern-.12em\lower-.51ex\hbox{\scalebox{0.6}{\(\mathcal{ATH}\)}}}' + '\n'
    if prerequisite != '':
        document = ''.join([document, prerequisite])
    document_body = '\n'.join([r'\begin{document}', t[1], r'\end{document}'])
    t[0] = ''.join([document, document_body])
    # TODO push \n after: \documentclass, \usepackage, \begin, \end --
    #   AFTER remove interactive class when runnig prog
    # TODO include only needed package by checking math_flag

    # finale output.
    print(t[0])


def p_paragraph(t):
    '''paragraph :
                 | paragraph component'''
    try:
        t[0] = t[1] + t[2]
    except:
        t[0] = ''

#   def p_lztex(t):
#       '''lztex :
#                | lztex component'''

def p_component(t):
    '''component : text
                 | SYMBOL
                 | NEWLINE
                 | ezmath'''
    t[0] = t[1]

def p_text(t):
    '''text : CHARACTER
            | text CHARACTER'''
    try:
        t[0] = t[1] + t[2]
    except:
        t[0] = t[1]

def p_ezmath(t):
    '''ezmath : BEGIN_EZMATH sentence END_EZMATH'''
    if t[1][0] == '\n' and t[3][-1] == '\n':
        t[0] = r'\[{body}\]'.format(body=t[2])
    else:
        t[0] = r'\({body}\)'.format(body=t[2])

def p_ezmath_error(t):
    '''ezmath : BEGIN_EZMATH error END_EZMATH'''
    # simple implementaion of error handler for ezmath part
    # TODO
    t[0] = r'/*ezmath_parser_error*/'

def p_sentence(t):
    '''sentence :
                | statement'''
    try:
        t[0] = t[1]
    except:
        t[0] = '/*nothing*/'  # FIXME

def p_statement(t):
    '''statement : expression
                 | statement expression'''
    try:
        # when assembly each part, check if going to joint alphabet?
        if t[2][0].isalpha() and t[1][-1].isalpha():
            t[0] = t[1] + ' '+ t[2]
        else:
            t[0] = t[1] + t[2]
    except:
        t[0] = t[1]

    # simple debug.
    print('... {0}'.format(t[0]))
    # FIXME remove 0 inside {} due to make compatible w/ python27 and py3k only.

def p_expression(t):
    '''expression : element
                  | fraction
                  | summation
                  | control'''
    t[0] = t[1]

def p_element(t):
    '''element : atom_sup
               | parentheses_others
               | matrix'''
    t[0] = t[1]

def p_control(t):
    '''control : CONTROL'''
    if t[1] == ',' or t[1] == ';':
        t[0] = t[1]
    else:
        t[0] = r'\\'
    # TODO use ; as  & for paragraph alignment?


def p_matrix(t):
    '''matrix : OB_MATRIX matrix_sentence CB'''
    t[0] = r'\begin{{{head}}}{body}\end{{{head}}}'.format(head=t[1], body=t[2])
    flag.amsmath = True

def p_matrix_sentence(t):
    '''matrix_sentence :
                       | matrix_statement'''
    try:
        t[0] = t[1]
    except:
        t[0] = '/*nothing*/' # FIXME

def p_matrix_statement(t):
    '''matrix_statement : matrix_expression
                        | matrix_statement matrix_expression'''
    try:
        # when assembly each part, check if going to joint alphabet?
        if t[2][0].isalpha() and t[1][-1].isalpha():
            t[0] = t[1] + ' '+ t[2]
        else:
            t[0] = t[1] + t[2]
    except:
        t[0] = t[1]

    # simple debug.
    print('... {0}'.format(t[0]))
    # FIXME remove 0 inside {} due to make compatible w/ python27 and py3k only.

def p_matrix_expression(t):
    '''matrix_expression : element
                         | fraction
                         | matrix_control'''
    t[0] = t[1]

def p_matrix_control(t):
    '''matrix_control : CONTROL'''
    if t[1] == ',':
        t[0] = r'&'
    elif t[1] == ';':
        t[0] = r'\\'
    else:
        t[0] = ''


def p_summation(t):
    '''summation : SUMMATION sentence
                 | SUMMATION sentence summation_boundary'''
    # TODO use \limits ro \displaystyle to force make it upper and lower of symb
    try:
        t[0] = t[1] + t[3] + t[2]
    except:
        sep = ' 'if t[2][0].isalpha() else ''
        t[0] = t[1] + sep + t[2]

def p_summation_boundary(t):
    '''summation_boundary : FOR expression
                          | FOR expression TO expression
                          | FROM expression TO expression
                          | FOR expression FROM expression TO expression'''
    try:
        t[2] = rm_parentheses(t[2])
        t[4] = rm_parentheses(t[4])
        t[6] = rm_parentheses(t[6])
        t[0] = r'_{' + t[2] + '=' + t[4] + r'}^{' + t[6] + r'}'
    except:
        try:
            if t[1] == 'for':
                sep = ' ' if t[4][0].isalpha() else ''
                t[0] = r'_{' + t[2] + r'\to' + sep + t[4] + r'}'
            else:
                t[0] = r'_{' + t[2] + r'}^{' + t[4] + r'}'
        except:
            t[0] = r'_{' + t[2] + r'}'

def p_parentheses(t):
    '''parentheses : OP sentence CP'''
    t[0] = r'\left({body}\right)'.format(body=t[2])

def p_function(t):
    '''function : FUNCTION parentheses'''
    t[2] = rm_parentheses(t[2])
    if t[1] == r'abs':
        t[0] = r'\left|{body}\right|'.format(body=t[2])
    elif t[1] == r'norm':
        t[0] = r'\left\|{body}\right\|'.format(body=t[2])
    elif t[1] == r'bra':
        t[0] = r'\left\langle{body}\right|'.format(body=t[2])
    elif t[1] == r'ket':
        t[0] = r'\left|{body}\right\rangle'.format(body=t[2])
    elif t[1] == r'braket' or t[1] == r'inner':
        t[0] = r'\left\langle{body}\right\rangle'.format(body=t[2])
    elif t[1] == r'floor':
        t[0] = r'\left\lfloor{body}\right\rfloor'.format(body=t[2])
    elif t[1] == r'ceil':
        t[0] = r'\left\lceil{body}\right\rceil'.format(body=t[2])
    elif t[1] == r'round':
        t[0] = r'\left\lfloor{body}\right\rceil'.format(body=t[2])
    elif t[1] == r'list':
        t[0] = r'\left\[{body}\right\]'.format(body=t[2])
    else:
        # FIXME hat -> \widehat, vec -> \overrightarrow, bar -> overline ??
        t[0] = r'\{name}{{{body}}}'.format(name=t[1], body=t[2])


def p_fraction(t):
    '''fraction : expression KW_DIVISION element'''
    t[0] = r'\frac{{{div}}}{{{num}}}'.format(div=rm_parentheses(t[1]), num=rm_parentheses(t[3]))

def p_parentheses_others(t):
    '''parentheses_others : OS sentence CS
                          | OP_MOD sentence CP
                          | OP sentence KW_CHOOSE sentence CP
                          | OP sentence KW_ROOT sentence CP'''
    if t[1] == r'{':
        t[0] = r'\left\{{{body}\right\}}'.format(body=t[2])
    elif t[1] == r'pmod':
        t[0] = r'\pmod{{{num}}}'.format(num=t[2])
    elif t[3] == r'choose':
        t[0] = r'{{{div}\choose{num}}}'.format(div=t[2], num=t[4])
    else:
        t[0] = r'\sqrt[{nth}]{{{root}}}'.format(nth=t[2], root=t[4])

def p_atom_sup(t):
    '''atom_sup : atom_sub
                | atom_sub KW_POWER element'''
    try:
        t[0] = r'{base}^{{{sup}}}'.format(base=t[1], sup=rm_parentheses(t[3]))
    except:
        t[0] = t[1]

def p_atom_sub(t):
    '''atom_sub : atom
                | atom OB sentence CB'''
    try:
        t[0] = r'{base}_{{{sub}}}'.format(base=t[1], sub=t[3])
    except:
        t[0] = t[1]

def p_atom(t):
    '''atom : SYMBOL
            | GREEK
            | ENGLISH
            | NUMBER
            | TEXT
            | parentheses
            | function'''
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc
yacc.yacc()


###############################################################################

def py2_handler():
    # FIXME simple input handler for python2
    try:
        input = raw_input
    except:
        pass

class ParserFlag:
    def __init__(self):
        self.amsmath = False
        self.lztex_logo = False
        self.ezmath_logo = False

# FIXME quick hack for build-in help.
def LzTeX():
    '''some help?
    
    No <=, use =< instead (Haskell style).'''

def main():
    args = get_shell_args()

    welcome_message = '''
    LzTeX beta preview (nightly build, Wed, Jun 27, 2012 11:31:21 AM)
      Quick Docs: Type a document in LzTeX format when prompt.
      On empty line hit ^D to see result, and hit ^D again to quit.
    '''.strip().replace('    ', '')
    print(welcome_message)
    while True:
        global flag
        flag = ParserFlag()
        try:
            s = input('>>> ')

            # FIXME quick hack for invoke intepreter help command.
            if s == r'\h':
                help(LzTeX)
            elif s == r'\q':
                raise(EOFError)
            else:
                while True:
                    try:
                        s += '\n'
                        s += input('... ')
                    except EOFError:
                        print('')
                        yacc.parse(s)
                        break
        except EOFError:
            print('')
            exit('bye ^^)/')

if __name__ == '__main__':
    py2_handler()
    main()







