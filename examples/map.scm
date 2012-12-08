(define (map fn lst)
	(if (null? lst)
		lst
		(cons (fn (car lst)) (map fn (cdr lst)))))

(display (map (lambda (x) (* 2 x)) (list 1 2 3)))
(newline)
