(def factorial (n)
    (if (>= 1 n)
        1
        (* n (factorial (- n 1)))))

(print (concat
	"result: "
	(* 0.3 (factorial 10))))
