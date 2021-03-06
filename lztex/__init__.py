#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ply.lex import TOKEN
from re import escape, sub

logo = { r'TeX':      r'\TeX{}',
         r'LaTeX':    r'\LaTeX{}',
         r'LaTeX2e':  r'\LaTeXe{}',
         r'AmS':      r'\AmS{}',
         r'LzTeX':    r'\LzTeX{}',
         r'EzMath':   r'\EzMath{}', }

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

def escape_latex(matched_char):
    c = matched_char.group()
    if c in '#$%&_{}':
        return '\\{char}'.format(char=c)
    elif c in '[]<>|':
        return '{{{char}}}'.format(char=c)
    else:
        d = { '^':  '^',
              '`':  '`',
              "'":  'textquotesingle',
              '~':  'textasciitilde',
              '\\': 'textbackslash', }
        return '\\{char}{{}}'.format(char=d[c])


###############################################################################

tokens = (
        'LOGO',
        'CHARACTER',
        'WHITESPACE',
        'QUOTE',
        'CODE',
        'BLOCKCODE',
        'IPA',
        'LINK',
        'ITEM',
        'TITLELINE',
        'UNDERLINE',
        'NEWLINE',
        'ESCAPE',
        'EMPHASIS',


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

@TOKEN(r'|'.join(w for w in sorted(logo, key=sort_len)))
def t_LOGO(t):
    if t.value == 'LzTeX':
        flag.lztex_logo = True
    elif t.value == 'EzMath':
        flag.ezmath_logo = True
    elif t.value == 'AmS':
        flag.amsmath = True
    t.value = logo[t.value]
    t.lexer.begin_quote = False
    return t

def t_WHITESPACE(t):
    '[ \t]+'
    t.lexer.begin_quote = True
    return t
#   if t.value[-1] in ("'", '"'):
#       t.lexer.backward(1)
#       t.lexer.begin_quote = True
#       t.value = t.value[:-1]

def t_EMPHASIS(t):
    r'(?P<star>(\*|_){1,3})[^\*]+(?P=star)'
    # TODO enable escape \*, \_ inside
    if t.value[:3] in ('***', '___'):
        t.value = r'\textbf{{\emph{{{text}}}}}'.format(text=t.value[3:-3])
    elif t.value[:2] in ('**', '__'):
        t.value = r'\textbf{{{text}}}'.format(text=t.value[2:-2])
    else:
        t.value = r'\emph{{{text}}}'.format(text=t.value[1:-1])
    t.lexer.begin_quote = False
    return t


def t_QUOTE(t):
    r'\'|"'
    if t.lexer.begin_quote:
        t.value = '`' if t.value == "'" else '``'
        t.lexer.begin_quote = False
    else:
        t.value = "'" if t.value == "'" else "''"
        t.lexer.begin_quote = True
    return t


def t_BLOCKCODE(t):
    r'(?<=\n)(?P<star>`+)\n(.*?\n)*?(?P=star)(?=\n)'
    code = t.value.strip('`')
    t.value = r'\begin{{verbatim}}{code}\end{{verbatim}}'.format(code=code)
    return t

def t_CODE(t):
    r'(?P<star>`+).*?(?P=star)'
    pattern = r'|'.join(escape(w) for w in r"\#$%&`'_{}[]^~<>|")
    code = t.value.strip('`').strip()
    code = sub(pattern, escape_latex, code)
    t.value = r'\texttt{{{code}}}'.format(code=code)
    return t


def t_IPA(t):
    r'/.*/'
    flag.tipa = True
    # TODO parse to full IPA
    t.value = t.value.\
            replace("ˈ", '"').\
            replace('ɪ', 'I').\
            replace('ɛ', '@')
    t.value = r'\textipa{{{word}}}'.format(word=t.value)
    return t

def t_ITEM(t):
    r'\n(-|\+|\*)[ \t]+'
    t.lexer.begin_quote = True
    return t

def t_LINK(t):
    r'<[^ >]+?@[^ >]+?>|<[^ >]+?://[^ >]+?>'
    flag.hyperref = True
    if '@' in t.value:
        t.value = r'\href{{mailto:{name}}}{{\texttt{{<{name}>}}}}'.format(name=t.value[1:-1])
    else:
        t.value = r'\url{{{name}}}'.format(name=t.value[1:-1])
    return t

def t_TITLELINE(t):
    r'\n\#+\n'
    return t

def t_UNDERLINE(t):
    r'\n(-|=)+\n'
    if t.value[1] == r'=':
        t.value = 'section'
    else:
        t.value = 'subsection'
    return t


def t_BEGIN_EZMATH(t):
    r'\n?\$'
    t.lexer.begin('matrix')
    t.lexer.begin_quote = False
    return t

def t_ezmath_matrix_END_EZMATH(t):
    r'\$\n?'
    t.lexer.begin('INITIAL')
    t.lexer.begin_quote = False
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.begin_quote = True
    return t

def t_ESCAPE(t):
    r'\\.'
    # TODO check if \n, \t, \somthing that need to be convert as escape char.
    t.lexer.begin_quote = False
    if t.value == r'\n':
        t.value = r'\newline'
    elif t.value == r'\`':
        t.value = r'\`{}'
    elif t.value == r'\\':
        t.value = r'\textbackslash'
    else:
        t.value = t.value[-1]
    return t

def t_CHARACTER(t):
    r'.'
    #r'[a-zA-Z0-9]'
    if t.value in '([{':
        t.lexer.begin_quote = True
    else:
        t.lexer.begin_quote = False
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
    r'[0-9]+\.[0-9]*(...)[0-9]+(...)|[0-9]+(\.[0-9]+(...)?)?'
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
lexer = lex.lex()


###############################################################################

def p_document(t):
    '''document : section
                | title section'''
    document = r'\documentclass{article}' + '\n'

    prerequisite = flag.make_prerequisite()
    if prerequisite != '':
        document = ''.join([document, prerequisite])

    try:
        body = '\n'.join([t[1], r'\begin{document}', r'\maketitle', t[2], r'\end{document}'])
    except:
        body = '\n'.join([r'\begin{document}', t[1], r'\end{document}'])

    t[0] = ''.join([document, body])

    # finale output.
    return t[0]

def p_title(t):
    '''title : line TITLELINE line'''
    t[1] = r'\title{{{title}}}'.format(title=t[1])
    t[3] = r'\author{{{name}}}'.format(name=t[3])
    t[0] = '\n'.join([t[1], t[3], r'\date{}'])

def p_section_empty(t):
    '''section : '''
    t[0] = ''

def p_section(t):
    '''section : block
               | section block'''
    try:
        t[0] = t[1] + t[2]
    except:
        t[0] = t[1]
    
def p_block(t):
    '''block : header
             | content
             | itemize
             | BLOCKCODE
             | NEWLINE'''
             #| blockquote
    t[0] = t[1]

def p_header(t):
    '''header : line UNDERLINE'''
    try:
        t[0] = r'\{head}{{{body}}}'.format(head=t[2], body=t[1]) + '\n'
    except:
        t[0] = t[1]

# TODO
def p_blockquote(t):
    '''blockquote : line
                  | blockquote line'''
    try:
        t[0] = t[1] + t[2]
    except:
        t[0] = t[1]


def p_itemize(t):
    '''itemize : item_list'''
    t[0] = '\n'.join([r'\begin{itemize}', t[1], r'\end{itemize}'])

def p_item_list(t):
    '''item_list : item_each
                 | item_list item_each'''
    try:
        t[0] = '\n'.join([t[1], t[2]])
    except:
        t[0] = t[1]

def p_item_each(t):
    '''item_each : ITEM line'''
    t[0] = ' '.join([r'\item', t[2]])


def p_content(t):
    '''content : line'''
               #| content NEWLINE'''
    try:
        t[0] = t[1] + t[2]
    except:
        t[0] = t[1]

def p_line(t):
    '''line : component
            | line component'''
    try:
        t[0] = t[1] + t[2]
    except:
        t[0] = t[1]

def p_component(t):
    '''component : text
                 | LOGO
                 | WHITESPACE
                 | QUOTE
                 | CODE
                 | IPA
                 | LINK
                 | ESCAPE
                 | EMPHASIS
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
        t[0] = '\n' + t[0] + '\n'
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

    # simple debug inside math.
    # print('... {0}'.format(t[0]))

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
        t[0] = r'\limits_{' + t[2] + '=' + t[4] + r'}^{' + t[6] + r'}'
    except:
        try:
            if t[1] == 'for':
                sep = ' ' if t[4][0].isalpha() else ''
                t[0] = r'\limits_{' + t[2] + r'\to' + sep + t[4] + r'}'
            else:
                t[0] = r'\limits_{' + t[2] + r'}^{' + t[4] + r'}'
        except:
            t[0] = r'\limits_{' + t[2] + r'}'

def p_parentheses(t):
    '''parentheses : OP sentence CP'''
    t[0] = r'\left({body}\right)'.format(body=t[2])

def p_function(t):
    '''function : FUNCTION parentheses'''
    t[2] = rm_parentheses(t[2])
    sep = ' ' if t[2][0].isalpha() else ''
    if t[1] == r'abs':
        t[0] = r'\left|{body}\right|'.format(body=t[2])
    elif t[1] == r'norm':
        t[0] = r'\left\|{body}\right\|'.format(body=t[2])
    elif t[1] == r'bra':
        t[0] = r'\left\langle{body}\right|'.format(body=sep+t[2])
    elif t[1] == r'ket':
        t[0] = r'\left|{body}\right\rangle'.format(body=t[2])
    elif t[1] == r'braket' or t[1] == r'inner':
        t[0] = r'\left\langle{body}\right\rangle'.format(body=sep+t[2])
    elif t[1] == r'floor':
        t[0] = r'\left\lfloor{body}\right\rfloor'.format(body=sep+t[2])
    elif t[1] == r'ceil':
        t[0] = r'\left\lceil{body}\right\rceil'.format(body=sep+t[2])
    elif t[1] == r'round':
        t[0] = r'\left\lfloor{body}\right\rceil'.format(body=sep+t[2])
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
# yacc.yacc(write_tables=0, debug=0)  # for release version.
yacc.yacc()


###############################################################################

class ParserFlag:
    def __init__(self):
        # package
        self.amsmath = False
        self.hyperref = False
        self.tipa = False

        # command
        self.lztex_logo = False
        self.ezmath_logo = False

    def make_prerequisite(self):
        prerequisite = ''
        prerequisite += r'\usepackage[T1]{fontenc}' + '\n'
        prerequisite += r'\usepackage{lmodern}' + '\n'
        prerequisite += r'\usepackage{upquote}' + '\n'

        if self.amsmath:
            prerequisite += r'\usepackage{amsmath}' + '\n'
        if self.tipa:
            prerequisite += r'\usepackage{tipa}' + '\n'
        if self.hyperref:
            prerequisite += r'\usepackage{hyperref}' + '\n'
        if self.lztex_logo:
            prerequisite += r'\usepackage{relsize}' + '\n'
            prerequisite += r'\newcommand{\LzTeX}{L\kern-.31em\lower-.47ex\hbox{\smaller{\smaller{Z}}}\kern-.09emT\kern-.16em\lower+.51ex\hbox{E}\kern-.27exX}' + '\n'
        if self.ezmath_logo:
            prerequisite += r'\usepackage{graphicx}' + '\n'
            prerequisite += r'\newcommand{\EzMath}{\(\mathcal{E}\)\kern-.18em\lower+.51ex\hbox{\(\mathcal{Z}\)}\kern-.18em\(\mathcal{M}\)\kern-.12em\lower-.51ex\hbox{\scalebox{0.6}{\(\mathcal{ATH}\)}}}' + '\n'
        return prerequisite


def parse(s):
    global flag
    flag = ParserFlag()
    lexer.begin_quote = True
    return yacc.parse(s)

