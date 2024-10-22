(module
  (type (;0;) (func (param i32) (result i32)))
  (import "env" "__linear_memory" (memory (;0;) 0))
  (func $fib (type 0) (param i32) (result i32)
    (local i32 i32 i32)
    block  ;; label = @1 - base case
      local.get 0
      i32.const 2
      i32.ge_s ;; local >= 2
      br_if 0 (;@1;)
      local.get 0
      i32.const 0
      i32.add
      return
    end
    i32.const 0
    local.set 1
    loop  ;; label = @1 - recursive step
      local.get 0
      i32.const -1
      i32.add
      call $fib
      local.get 1
      i32.add
      local.set 1
      local.get 0
      i32.const 3
      i32.gt_u
      local.set 2
      local.get 0
      i32.const -2
      i32.add
      local.tee 3
      local.set 0
      local.get 2
      br_if 0 (;@1;)
    end
    local.get 3
    local.get 1
    i32.add)
  (export "fib" (func $fib)) 
)
