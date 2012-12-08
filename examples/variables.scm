(define var)

(define (fn)
	(define (inner)
		(set! var "still in global scope")
		#f)
	(inner))

(fn)

(display var)  ; Expect "still in global scope"
(newline)
