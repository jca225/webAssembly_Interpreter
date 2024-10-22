package main

import "fmt"

// The problem lies innthe construction of the list
type Frame struct {
  StringVal []string
}

func (f *Frame) editFrame() {
  f.StringVal[0] = "changed"
}

type structNode struct {
  Intval int       // pass by value
  Fr     *Frame // pass by reference

}
func main() {
  example := structNode{}
  example.Intval = 4
  f := Frame{}
  f.StringVal=append(f.StringVal, "unchanged")
  example.Fr = &f  
  g(example)

  fmt.Println(example.Fr.StringVal[0])


}


func g(s structNode) {
  fr := *s.Fr
  // an explicit copy mechanism allows this to happen
  fr.StringVal = make([]string, len(s.Fr.StringVal))
  fr.editFrame()
  fmt.Println(fr.StringVal[0])

}
