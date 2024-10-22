;; Compute the nand of two values, using only the `or` and `not` functions
;;
;; nand should always return a boolean value
(define (nand a b) (or (not a) (not b)))