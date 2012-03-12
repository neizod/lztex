'''only use this in meta and markdown section.'''

def corrected_quoatation(q):
    return q.group(1) + ('`' if q.group(2) == "'" else '``')

###############################################################################

import re

raw = input()

out = re.sub(r'(^|\s)("|\')', corrected_quoatation, raw)

print(out)
