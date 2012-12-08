(define ! (lambda (n)
    (if (>= 1 n)
        1
        (* n (! (- n 1))))))

(define !-it (lambda (x)
    (define !-internal (lambda (n current)
        (if (= n 0)
            current
            (!-internal (- n 1) (* n current)))))
    (!-internal x 1)))

(display (string-concatenate (list
	"factorial: "
	(number->string (! 10)))))
(newline)

(display (string-concatenate (list
	"factorial (iterative): "
	(number->string (!-it 10)))))
(newline)
