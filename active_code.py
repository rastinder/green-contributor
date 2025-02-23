def data_structures_and_algorithms():
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None
    
    class DoublyLinkedList:
        def __init__(self):
            self.head = None
            self.tail = None
        
        def append(self, data):
            new_node = Node(data)
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                new_node.prev = self.tail
                self.tail.next = new_node
                self.tail = new_node
        
        def prepend(self, data):
            new_node = Node(data)
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node
        
        def delete(self, data):
            current = self.head
            while current:
                if current.data == data:
                    if current.prev:
                        current.prev.next = current.next
                    else:
                        self.head = current.next
                    
                    if current.next:
                        current.next.prev = current.prev
                    else:
                        self.tail = current.prev
                    return True
                current = current.next
            return False
        
        def display(self):
            elements = []
            current = self.head
            while current:
                elements.append(str(current.data))
                current = current.next
            return "->".join(elements)
    
    class AVLNode:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.height = 1
    
    class AVLTree:
        def get_height(self, node):
            if not node:
                return 0
            return node.height
        
        def get_balance(self, node):
            if not node:
                return 0
            return self.get_height(node.left) - self.get_height(node.right)
        
        def right_rotate(self, y):
            x = y.left
            T2 = x.right
            x.right = y
            y.left = T2
            y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
            x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
            return x
        
        def left_rotate(self, x):
            y = x.right
            T2 = y.left
            y.left = x
            x.right = T2
            x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
            y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
            return y
        
        def insert(self, root, key):
            if not root:
                return AVLNode(key)
            
            if key < root.key:
                root.left = self.insert(root.left, key)
            elif key > root.key:
                root.right = self.insert(root.right, key)
            else:
                return root
            
            root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1
            balance = self.get_balance(root)
            
            # Left Left Case
            if balance > 1 and key < root.left.key:
                return self.right_rotate(root)
            
            # Right Right Case
            if balance < -1 and key > root.right.key:
                return self.left_rotate(root)
            
            # Left Right Case
            if balance > 1 and key > root.left.key:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
            
            # Right Left Case
            if balance < -1 and key < root.right.key:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)
            
            return root
    
    # Example usage
    def example_usage():
        # Test DoublyLinkedList
        dll = DoublyLinkedList()
        dll.append(1)
        dll.append(2)
        dll.append(3)
        dll.prepend(0)
        print("Doubly Linked List:", dll.display())
        dll.delete(2)
        print("After deleting 2:", dll.display())
        
        # Test AVL Tree
        avl_tree = AVLTree()
        root = None
        numbers = [10, 20, 30, 40, 50, 25]
        for num in numbers:
            root = avl_tree.insert(root, num)
        print("AVL Tree root value:", root.key)
        print("Left subtree height:", avl_tree.get_height(root.left))
        print("Right subtree height:", avl_tree.get_height(root.right))
    
    return example_usage




def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def calculate_sum(numbers):
    return sum(numbers)


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1