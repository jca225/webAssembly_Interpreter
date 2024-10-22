package main


type node struct {

	value int
	next *node
}

type linkedlist struct {
	head *node
	len int
}


func (l *linkedlist) add(value int) {
	newNode := new(node)
	newNode.value = value
	newNode.next = nil

	if l.head == nil {
		linkedlist.head = newNode
	} else {
		iterator := l.head
		for ; iterator.next != nil; iterator = iterator.next {

		}
		iterator.next = newNode
	}

}


func (l *linkedlist) remove(value int) {
	iterator := linkedlist.head
	while (iterator.head != nil) {
		if iterator.value == value {
			iterator.next = iterator.next.next
			break
		}
		iterator = iterator.next
	}
}


func (l linkedlist) get(value int) *node {
	
}

fun (l linkedlist) String() string {
	
}