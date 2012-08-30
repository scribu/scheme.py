(define PI 3.41)

(define factorial (lambda (n)
    (if (>= 1 n)
        1
        (* n (factorial (- n 1))))))

(print (concat
	"result: "
	(* 0.3 (factorial 10))))

(print (cdr (list 1 2 3 "foo")))

(print #t #f)
