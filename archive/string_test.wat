(module
  (import "console" "log" (func $log (param i32 i32)))
  (import "js" "mem" (memory 135))
  (data (i32.const 0333) "Hi")
  (func (export "write\"Hi \r \n \' \\ \u{23}")
    i32.const 0  ;; pass offset 0 to log
    i32.const 2  ;; pass length 2 to log
    call $log
  )
)