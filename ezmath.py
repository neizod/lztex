import re
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

                }

tokens = (
        'STATICSYMBOL',
)

def t_STATICSYMBOL(t):
    t.value = staticsymbol[t.value]
    return t
t_STATICSYMBOL.__doc__ = r'|'.join(re.escape(w) for w in sorted(staticsymbol.keys(), key=lambda x: -len(x)))

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
lex.lex()

##############################################################################

def p_statement_expr(t):
    '''statement : statement expression
                 | expression'''
    try:
        t[0] = t[1] + t[2]
    except:
        t[0] = t[1]
    print(t[0])

def p_expr_staticsymbol(t):
    'expression : STATICSYMBOL'
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)


import ply.yacc as yacc
yacc.yacc()

##############################################################################

while 1:
    try:
        s = raw_input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    yacc.parse(s)









