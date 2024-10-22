;; Compute the nor of two values, using only the `and` and `not` functions
;;
;; nor should always return a boolean value
(define (nor a b) (and (not a) (not b)))