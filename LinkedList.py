class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def travel(self):
        currentNode = self.head
        while currentNode is not None:
            print(currentNode.data, end=" ")
            currentNode = currentNode.next
        print()

    def add(self, value):
        newNode = ListNode(value)
        newNode.next = self.head
        self.head = newNode

    def search(self, target):
        currentNode = self.head
        while currentNode is not None and currentNode.data != target:
            currentNode = currentNode.next
        return currentNode is not None
    
    @staticmethod
    def create(array):
        if len(array) == 0:
            return None
        
        head = ListNode(array[0])
        currentNode = head
        for i in range(1, len(array)):
            newNode = ListNode(array[i])
            currentNode.next = newNode
            currentNode = newNode

        linked_list = LinkedList()
        linked_list.head = head
        return linked_list
    
    def remove(self, target):
        preNode = None
        currentNode = self.head
        while currentNode is not None and currentNode.data != target:
            preNode = currentNode
            currentNode = currentNode.next

        if currentNode is self.head:
            self.head = currentNode.next
        else:
            preNode.next = currentNode.next



array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
linked_list = LinkedList.create(array)

linked_list.travel()

if linked_list.search(4):
    print("Found 4")
else:
    print("4 not found")

linked_list.remove(3)
linked_list.add(11)

linked_list.travel()
