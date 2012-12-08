(define (make-adder x)
	(lambda (y) (+ x y)))

(define add-3 (make-adder 3))

(display (add-3 2))
(newline)
