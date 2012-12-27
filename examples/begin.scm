(define (foo x)
  (if (< x 0)
	#f
	(begin
	  (display "it's positive")
	  (newline)
	  x
	  )))

(display (foo 3))
