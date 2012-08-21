import lisp

lisp.eval( (



('def', 'gt1', ('x'),
    ('print', 'crunching...'),
    ('if', ('<', 1, 'x'), 'yes', 'no')
),
('print', ('concat', 'result: ', ('gt1', 1))),
('print', ('concat', 'result: ', ('gt1', 2)))



) )
