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
                'nable':  r'\nabla',

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
                'Aleph':      r'\aleph',
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

tokens = (
        'STATICSYMBOL',
        'GREEKSYMBOL',
        'ENGLISHSYMBOL',

        'OP',
        'CP',
        'OB_M',
        'OB',
        'CB',

        'POW',
)

states = (
        ('matrix', 'inclusive'),
)

sort_len = lambda x: -len(x)


###############################################################################

def t_OP(t):
    r'\('
    t.lexer.begin('matrix')
    return t

def t_CP(t):
    r'\)'
    t.lexer.begin('INITIAL')
    return t

def t_OB(t):
    r'\['
    t.lexer.begin('matrix')
    return t

def t_matrix_OB_M(t):
    r'\['
    t.lexer.begin('matrix')
    return t

def t_CB(t):
    r'\]'
    t.lexer.begin('INITIAL')
    return t

def t_POW(t):
    r'\^'
    t.lexer.begin('matrix')
    return t

@TOKEN(r'[ \t]')
def t_WHITESPACE(t):
    t.lexer.begin('matrix')

@TOKEN(r'|'.join(escape(w) for w in sorted(staticsymbol.keys(), key=sort_len)))
def t_STATICSYMBOL(t):
    t.lexer.begin('INITIAL')
    t.value = staticsymbol[t.value]
    return t

@TOKEN(r'|'.join(w for w in sorted(greeksymbol, key=sort_len)))
def t_GREEKSYMBOL(t):
    t.lexer.begin('INITIAL')
    t.value = '\\' + t.value
    return t

def t_ENGLISHSYMBOL(t):
    r'[a-zA-Z]'
    t.lexer.begin('INITIAL')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.begin('matrix')
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
lex.lex()


###############################################################################


def p_statement_expr(t):
    '''statement : statement expression
                 | expression'''
    try:
        if t[2][0].isalpha() and t[1][-1].isalpha():
            t[0] = t[1] + ' '+ t[2]
        else:
            t[0] = t[1] + t[2]
    except:
        t[0] = t[1]

    # simple debug.
    print('... {0}'.format(t[0]))
    # FIXME remove 0 inside {} due to make compatible w/ python27 and py3k only.

def p_expr_staticsymbol(t):
    '''expression : atom_sup
                  | prts
                  | matrix'''
    t[0] = t[1]

def p_prts(t):
    '''prts : OP statement CP'''
    # first -- test -- easy -- not accroding to spec implement of (...)
    t[0] = r'\left(' + t[2] + r'\right)'

def p_matrix(t):
    '''matrix : OB_M statement CB'''
    t[0] = r'\begin{matrix}' + t[2] + r'\end{matrix}'

def p_atom_sup(t):
    '''atom_sup : atom_sub
                | atom_sub POW expression'''
    try:
        t[0] = t[1] + r'^{' + t[3] + r'}'
    except:
        t[0] = t[1]

def p_atom_sub(t):
    '''atom_sub : atom
                | atom OB statement CB'''
    try:
        t[0] = t[1] + r'_{' + t[3] + r'}'
    except:
        t[0] = t[1]

def p_atom(t):
    '''atom : STATICSYMBOL
            | GREEKSYMBOL
            | ENGLISHSYMBOL'''
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc
yacc.yacc()


###############################################################################

while 1:
    try:
        s = raw_input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    yacc.parse(s)









