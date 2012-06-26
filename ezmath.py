from ply.lex import TOKEN
from re import escape

staticsymbol = {'+':    r'+', 
                '-':    r'-',
                '*':    r'\times',
                '.':    r'\cdot',
                'ast':  r'*',
                '//':   r'\div',

                '(+)':   r'\oplus',
                '(-)':   r'\ominus',
                '(*)':   r'\otimes',
                '(.)':   r'\odot',
                '(ast)': r'\circleast',
                '(/)':   r'\oslash',

                '+-':    r'\pm',
                '-+':    r'\mp',

                '~':     r'\sim',
                'deg':   r'{^\circ}', # degree?
                'star':  r'\star',

                '||':    r'\|',
                '|':     r'|',

                # ================================

                '=':      r'=',
                '==':     r'\equiv',
                '~=':     r'\cong',
                '~~':     r'\approx',
                'propto': r'\propto',
                '!=':     r'\neq',
                '<':      r'\lt',
                '>':      r'\gt',
                '<<':     r'\ll',
                '>>':     r'\gg',
                '<=':     r'\leq',    # '=<' like haskell due to arrow conflict
                '>=':     r'\geq',
                '-<':     r'\prec',
                '>-':     r'\succ',

                'and':    r'\land',
                'or':     r'\lor',
                'not':    r'\neg',
                '<->':    r'\leftrightarrow',
                '<-->':   r'\longleftrightarrow',
                '->':     r'\rightarrow',
                '-->':    r'\longrightarrow',
                '<-':     r'\leftarrow',
                '<--':    r'\longleftarrow',
                '<=>':    r'\Leftrightarrow',
                '<==>':   r'\Longleftrightarrow',
                '=>':     r'\Rightarrow',
                '==>':    r'\Longrightarrow',
                #'<=':     r'\Leftarrow',       # see above
                '<==':    r'\Longleftarrow',
                '|->':    r'\mapsto', 

                '...':    r'\ldots',
                'infinity':   r'\infty',

                'der':    r'\partial',
                'nabla':  r'\nabla',

                # force wrap this with \e ... \e ??
                'for all':    r'\forall',
                'exists':     r'\exists',
                'in':         r'\in',
                'not in':     r'\notin',
                'subset':     r'\subseteq',
                'superset':   r'\supseteq',

                'union':      r'\cup',
                'intersect':  r'\cap',

                'empty':      r'\emptyset',
                'Eset':       r'\varnothing',
                'Nset':       r'\mathbb{N}',
                'Zset':       r'\mathbb{Z}',
                'Pset':       r'\mathbb{P}',
                'Qset':       r'\mathbb{Q}',
                'Rset':       r'\mathbb{R}',
                'Cset':       r'\mathbb{C}',
                'Hset':       r'\mathbb{H}',
                'Aleph':      r'\aleph',       # lower case?
                'Re':         r'\Re',
                'Im':         r'\Im',

                # TODO function names

                }
greeksymbol = ( r'alpha',
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
                r'(O|o)mega',
                )

matrix = ( r'matrix',
           r'borderless',
           r'parentheses',
           r'det',
           r'norm',
           r'cases',
           r'',
           )

function = ( r'abs',
             r'norm',
             r'bra',
             r'ket',
             r'braket',
             r'inner',
             r'floor',
             r'ceil',
             r'round',
             r'sqrt',
             )

summation = { r'Summation':  r'\sum',
              r'Product':    r'\prod',
              r'Coproduct':  r'\coprod',
              r'Union':      r'\bigcup',
              r'Intersect':  r'\bigcap',
              r'integral':   r'\int',
              r'limit':      r'\lim',
              r'limit superior':     r'\limsup',
              r'limit inferior':     r'\liminf',
              }

sort_len = lambda x: -len(x)
repeat_num = lambda a: a[0] + r'\overline{' + a[1] + '}'
rm_parentheses = lambda t: t[6:-7] if t[:6] == r'\left(' and t[-7:] == r'\right)' else t

###############################################################################

tokens = (
        'EZMATH',
        'STATICSYMBOL',
        'GREEKSYMBOL',
        'ENGLISHSYMBOL',
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

def t_EZMATH(t):
    r'\n?\$\n?'
    t.lexer.begin('matrix')
    return t

def t_ezmath_matrix_OP_MOD(t):
    r'\([ \t]*mod'
    t.lexer.begin('matrix')
    t.value = 'pmod'
    return t

def t_OP(t):
    r'\('
    t.lexer.begin('matrix')
    return t

def t_CP(t):
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

def t_OB(t):
    r'\['
    t.lexer.begin('matrix')
    return t

def t_CB(t):
    r'\]'
    t.lexer.begin('ezmath')
    return t

def t_OS(t):
    r'\{'
    t.lexer.begin('matrix')
    return t

def t_CS(t):
    r'\}'
    t.lexer.begin('ezmath')
    return t


def t_KW_DIVISION(t):
    r'\/'
    t.lexer.begin('matrix')
    return t

def t_KW_POWER(t):
    r'\^'
    t.lexer.begin('matrix')
    return t

def t_KW_CHOOSE(t):
    r'choose'
    t.lexer.begin('matrix')
    return t

def t_KW_ROOT(t):
    r'root'
    t.lexer.begin('matrix')
    return t

def t_CONTROL(t):
    r',|;'
    t.lexer.begin('matrix')
    return t


@TOKEN(r'|'.join(escape(w) for w in sorted(summation.keys(), key=sort_len)))
def t_SUMMATION(t):
    t.lexer.begin('matrix')
    t.value = summation[t.value]
    return t

def t_FOR(t):
    r'for'
    t.lexer.begin('matrix')
    return t

def t_FROM(t):
    r'from'
    t.lexer.begin('matrix')
    return t

def t_TO(t):
    r'to'
    t.lexer.begin('matrix')
    return t


@TOKEN(r'|'.join(escape(w) for w in sorted(function, key=sort_len)))
def t_FUNCTION(t):
    t.lexer.begin('matrix')
    return t

@TOKEN(r'|'.join(escape(w) for w in sorted(staticsymbol.keys(), key=sort_len)))
def t_STATICSYMBOL(t):
    t.lexer.begin('ezmath')
    t.value = staticsymbol[t.value]
    return t

@TOKEN(r'[ \t]')
def t_WHITESPACE(t):
    t.lexer.begin('matrix')

@TOKEN(r'|'.join(w for w in sorted(greeksymbol, key=sort_len)))
def t_GREEKSYMBOL(t):
    t.lexer.begin('ezmath')
    t.value = '\\' + t.value
    return t

def t_ENGLISHSYMBOL(t):
    r'[a-zA-Z]'
    t.lexer.begin('ezmath')
    return t

def t_NUMBER(t):
    r'[0-9]+\.[0-9]*(...)[0-9](...)|[0-9]+(\.[0-9]+(...)?)?'
    t.lexer.begin('ezmath')
    if t.value.count('.') == 7:
        t.value = repeat_num(t.value.rsplit('...'))
    return t

def t_TEXT(t):
    r'"([^"\\]*?(\\.[^"\\]*?)*?)"'
    t.lexer.begin('ezmath')
    # TODO chk str identifier: frak"A" -> iden=frak, body=A
    t.value = r'\text{{{body}}}'.format(body=t.value[1:-1])
    return t


def t_newline(t):
    r'\n+'
    t.lexer.begin('matrix')
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
lexer = lex.lex()
lexer.begin('matrix')        # force input start with matrix state


###############################################################################

def p_lztex(t):
    '''lztex :
             | lztex ezmath'''
    try:
        t[0] = t[1] + t[2]
    except:
        t[0] = ''

    # finale output.
    print('fin {0}'.format(t[0]))
    # FIXME remove 0 inside {} due to make compatible w/ python27 and py3k only.


def p_ezmath(t):
    '''ezmath : EZMATH sentence EZMATH'''
    t[0] = t[2]

def p_ezmath_error(t):
    '''ezmath : EZMATH error EZMATH'''
    # simple implementaion of error handler for ezmath part
    # TODO
    t[0] = r'\ezmath_parser_error'

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
    t[0] = t[1]


def p_matrix(t):
    '''matrix : OB_MATRIX matrix_sentence CB'''
    t[0] = r'\begin{{{head}}}{body}\end{{{head}}}'.format(head=t[1], body=t[2])

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
    else:
        t[0] = r'\\'


def p_summation(t):
    '''summation : SUMMATION sentence
                 | SUMMATION sentence summation_boundary'''
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
        t[0] = r'\left|' + t[2] + r'\right|'
    elif t[1] == r'norm':
        t[0] = r'\left\|' + t[2] + r'\right\|'
    elif t[1] == r'bra':
        t[0] = r'\left\langle' + t[2] + r'\right|'
    elif t[1] == r'ket':
        t[0] = r'\left|' + t[2] + r'\right\rangle'
    elif t[1] == r'braket' or t[1] == r'inner':
        t[0] = r'\left\langle' + t[2] + r'\right\rangle'
    elif t[1] == r'floor':
        t[0] = r'\left\lfloor' + t[2] + r'\right\rfloor'
    elif t[1] == r'ceil':
        t[0] = r'\left\lceil' + t[2] + r'\right\rceil'
    elif t[1] == r'round':
        t[0] = r'\left\lfloor' + t[2] + r'\right\rceil'
    else:
        t[0] = r'\sqrt{' + t[2] + r'}'


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
    '''atom : STATICSYMBOL
            | GREEKSYMBOL
            | ENGLISHSYMBOL
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

while 1:
    try:
        lexer.begin('matrix')      # force input to start with matrix state
        s = raw_input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    yacc.parse(s)









