(define map (lambda (fn lst)
	(if (null? lst)
		lst
		(cons (fn (car lst)) (map fn (cdr lst))))))

(define double (lambda (x) (* 2 x)))

(display (map double (list 1 2 3)))
(newline)
