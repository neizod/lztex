'''only use this in meta and markdown section.'''

def corrected_quoatation(q):
    return q.group(1) + ('`' if q.group(2) == "'" else '``')

###############################################################################

import re

lines = []
while 1:
    lines.append(input())
    if lines[-1] == '':
        break

raw = '\n'.join(lines)

out = re.sub(r'(^|\s)("|\')', corrected_quoatation, raw)

print(out)
