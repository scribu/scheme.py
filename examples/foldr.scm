(define (foldr op init lst)
	(if (null? lst)
		init
		(op (car lst) (foldr op init (cdr lst)))))

(define (sum lst)
	(foldr + 0 lst))

(display (sum (list 1 2 3)))
(newline)
