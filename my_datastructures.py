import ctypes
from typing import Any
from my_exceptions import EmptyError


class Array:
    def __init__(self, type: Any, capacity: int = 1) -> None:
        """Initialize an array with a specified type and capacity.

        Args:
            type (Any): The type of elements the array will hold.
            capacity (int, optional): The initial capacity of the array. Defaults to 1.
        """

        self._type = type
        self._size = 0
        self._capacity = capacity
        self._Array = self._make_array(self._capacity) 


    def _make_array(self, capacity: int) -> ctypes.py_object: 
        """Create a new array with the specified capacity.

        Args:
            capacity (int): The capacity of the new array.

        Returns:
            ctypes.py_object: The new array object.
        """

        return (capacity * ctypes.py_object)()


    def __len__(self) -> int:
        """Return the size of the array.

        Returns:
            int: The number of elements in the array.
        """

        return self._size
    

    def __getitem__(self, k: int) -> Any:
        """Return the element at the specified index.

        Args:
            k (int): The index of the element.

        Returns:
            Any: The element at the specified index.

        Raises:
            IndexError: If the index is out of range.
        """

        if not 0 <= k < len(self):
            raise IndexError('Invalid index')
        return self._Array[k]    
    

    def __setitem__(self, k: int, item) -> None:
        """Set the element at the specified index.

        Args:
            k (int): The index of the element.
            item: The element to be set.

        Raises:
            ValueError: If the item's type is different from the array's type.
            IndexError: If the index is out of range.
        """

        if not type(item) is self._type:
            raise ValueError('You cant add an item of another type other than the type initialised with')
        
        if not 0 <= k <= len(self):
            raise IndexError('Invalid index')
        
        self._Array[k] = item   

        if k == len(self):
            self._size += 1


    def resize(self, capacity: int) -> None:
        """Resize the internal array to a new capacity.

        Args:
            capacity (int): The new capacity of the array.
        """

        new_array = self._make_array(capacity)

        for k in range(self._size):
            new_array[k] = self._Array[k]

        self._Array = new_array
        self._capacity = capacity


    def pop(self, index: int = 0) -> Any:
        """Remove and return the element at the specified index.

        Args:
            index (int, optional): The index of the element to remove. Defaults to 0.

        Returns:
            Any: The removed element.

        Raises:
            EmptyError: If the array is empty.
            IndexError: If the index is out of range.
        """

        if len(self) == 0:
            raise EmptyError()

        if not 0 <= index < len(self):
            raise IndexError('Invalid index')
        
        elem = self[index]
        for k in range(index, len(self) - 1):
            self[k] = self[k+1]

        self._size -= 1
        return elem     
        

class Heap:
    def __init__(self, type: Any) -> None:
        """Initialize a heap with a specified type.

        Args:
            type (Any): The type of elements the heap will hold.
        """

        self._type = type
        self._content = Array(type)

    
    def __len__(self) -> int:
        """Return the number of nodes in the heap.

        Returns:
            int: The number of nodes in the heap.
        """

        return len(self._content)


    def push(self, item: Any) -> None:
        """Add an element to the heap.

        Args:
            item (Any): The element to be added to the heap.
        """
        
        if len(self._content) == self._content._capacity:
            self._content.resize(self._content._capacity * 2)

        self._content[len(self)] = item
        index = len(self) - 1

        while index > 0:
            parent = (index - 1) // 2
            if self._content[index] < self._content[parent]:
                self._swap(index, parent)
                index = parent
            else:
                break


    def pop(self) -> Any:
        """Remove and return the root element from the heap.

        Returns:
            Any: The removed root element.

        Raises:
            EmptyError: If the heap is empty.
        """

        if len(self) == 0:
            raise EmptyError()
        
        self._swap(0, len(self._content) - 1)
        item = self._content.pop(index= len(self._content) - 1)

        n, index = len(self._content), 0
        while index < n:
            left_child = (2 * index) + 1
            right_child = (2 * index) + 2
            smallest = index

            if left_child < n and self._content[left_child] < self._content[smallest]:
                smallest = left_child
            if right_child < n and self._content[right_child] < self._content[smallest]:
                smallest = right_child

            if smallest == index:
                break

            self._swap(index, smallest)
            index = smallest

        return item
    

    def _swap(self, i: int, j: int) -> None:
        """Swap two elements in the heap.

        Args:
            i (int): The index of the first element.
            j (int): The index of the second element.
        """
        
        self._content[i], self._content[j] = self._content[j], self._content[i]


class Stack:    
    class _node:
        def __init__(self, element, next_) -> None:
            """Initialize a node with the given element and next node.

            Args:
                element: The element to be stored in the node.
                next_ (Optional[_node]): The next node in the linked list. Defaults to None.
            """

            self._element = element
            self._next = next_
        

    def __init__(self) -> None:
        """Initialize an empty stack."""

        self.head = None
        self.size = 0
        

    def __len__(self) -> int:
        """Return the size of the stack.

        Returns:
            int: The number of elements in the stack.
        """

        return self.size
   
   
    def is_empty(self) -> bool:
        """Check if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
        """

        return self.size == 0
   
       
    def peek(self) -> Any:
        """Return the top element of the stack.

        Returns:
            Any: The top element of the stack.

        Raises:
            EmptyError: If the stack is empty.
        """

        if self.is_empty():
            raise EmptyError()
       
        return self.head._element
   

    def push(self, element) -> None:
        """Add an element to the top of the stack.

        Args:
            element: The element to be added to the stack.
        """
        
        self.head = self._node(element, self.head)
        self.size += 1


    def pop(self) -> Any:
        """Remove and return the top element of the stack.

        Returns:
            Any: The removed top element of the stack.

        Raises:
            EmptyError: If the stack is empty.
        """
        
        if self.is_empty():
            raise EmptyError()
       
        answer = self.head._element
        self.head = self.head._next
        self.size -= 1
        return answer


    def reverse(self):
        """Return a new stack with elements in reversed order.

        Returns:
            Stack: A new stack with elements in reversed order.
        """

        stack = Stack()
        while len(self) != 0:
            stack.push(self.pop())
        
        return stack