;; substring-wildcard is like contains-substring, but it understands
;; single-character wildcards in the pattern string.  Wildcards are represented
;; by the ? character.  Note that this is a slightly broken way of doing
;; wildcards: the '?' character cannot be matched exactly.
;;
;; Here's an example execution: 
;; (contains-substring "hello" "e?lo") <-- returns true
;; (contains-substring "hello" "yell") <-- returns false
;; (contains-substring "The quick brown fox jumps over lazy dogs" "q?ick") <-- returns true
;;
;; You should implement this on your own, by comparing one character at a time,
;; and should not use any string comparison functions that are provided by gsi.

;; TODO: implement this function
(define (contains-substring source pattern) '())