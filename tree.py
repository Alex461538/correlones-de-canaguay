from typing import Optional, Any

class Node:
    parent: Optional["Node"] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    value: Any = 0

    def __init__(self, value):
        self.value = value

    """     def get_next_ref_non_terminal(self):
        node = self.right
        while node != None and node.left != None:
            node = node.left
        return node """
    
    def next(self):
        node = self
        # si hay arbol derecho le entra
        if node.right:
            # entra al arbol derecho
            node = node.right
            # Obtiene el nodo más a la izquierda
            while node != None and node.left != None:
                node = node.left
            return node
        # Si no hay nodos derechos
        while node.parent and node == node.parent.right:
            node = node.parent
        return node.parent
    
    def detach_from_parent(self):
        if (self.parent == None):
            return
        elif self == self.parent.left:
            self.parent.left = None
        else:
            self.parent.right = None
        self.parent = None
    
    def has_childs(self):
        return self.left != None or self.right != None
    
    def has_full_capacity(self):
        return self.left != None and self.right != None
    
class Tree:
    root: Optional["Node"] = None

    def __del_loc(self, node: Node):
        # It's a leaf!
        if not node.has_childs():
            if (node == self.root):
                self.root = None
            else:
                node.detach_from_parent()
        # pass the headache to someone else
        elif node.has_full_capacity():
            ino = node.next()
            node.value = ino.value
            self.__del_loc(ino)
        # It has one child
        else:
            child = node.left
            if node.left == None:
                child = node.right
            child.detach_from_parent()
            node.value = child.value
            node.left = child.left
            node.right = child.right
            if node.right:
                node.right.parent = node
            if node.left:
                node.left.parent = node

    def __del(self, item):
        if self.root == None:
            return False
        node = self.root
        while node != None:
            if (item == node.value):
                self.__del_loc(node)
                break
            elif (item < node.value and node.left != None):
                node = node.left
            elif (item > node.value and node.right != None):
                node = node.right
            else:
                break

    def __add(self, item):
        if self.root == None:
            self.root = Node(item)
            self.root.parent = None
        else:
            node = self.root
            while node != None:
                if (item < node.value):
                    if node.left != None:
                        node = node.left # Pasarle el problema a otro
                    else:
                        node.left = Node(item) # Tomar el problema
                        node.left.parent = node
                        break
                elif (item > node.value):
                    if node.right != None:
                        node = node.right
                    else:
                        node.right = Node(item)
                        node.right.parent = node
                        break
                else:
                    break

    def add(self, *args):
        for item in args:
            self.__add(item)
    
    def delete(self, *args):
        for item in args:
            self.__del(item)
    
    def __contains__(self, item):
        if self.root == None:
            return False
        node = self.root
        while node != None:
            if (item == node.value):
                return True
            elif (item < node.value and node.left != None):
                node = node.left
            elif (item > node.value and node.right != None):
                node = node.right
            else:
                return False
        return False
    
    def contains(self, item):
        return item in self
    
    def clear(self):
        self.root = None
    
    def LIR_list(self):
        arr = []
        def _add(node: Node):
            if (node.left):
                _add(node.left)
            arr.append(node.value)
            if (node.right):
                _add(node.right)
        if (self.root):
            _add(self.root)
        return arr
    
    def ILR_list(self):
        arr = []
        def _add(node: Node):
            arr.append(node.value)
            if (node.left):
                _add(node.left)
            if (node.right):
                _add(node.right)
        if (self.root):
            _add(self.root)
        return arr
    
    def LRI_list(self):
        arr = []
        def _add(node: Node):
            if (node.left):
                _add(node.left)
            if (node.right):
                _add(node.right)
            arr.append(node.value)
        if (self.root):
            _add(self.root)
        return arr
    
    def begin(self):
        node = self.root
        while node.left:
            node = node.left
        return node
    
    def search_lax(self, item, cmp_func = None):
        node = self.root
        if cmp_func == None:
            while node != None:
                if item == node.value:
                    break
                elif item < node.value and node.left != None:
                    node = node.left
                elif item > node.value and node.right != None:
                    node = node.right
                else:
                    break
        else:
            while node != None:
                if cmp_func(node.value) == 0:
                    break
                elif cmp_func(node.value) < 0 and node.left != None:
                    node = node.left
                elif cmp_func(node.value) > 0 and node.right != None:
                    node = node.right
                else:
                    break
            """ if item == node.value:
                break
            elif item < node.value:
                if node.left != None:
                    node = node.left
                else:
                    break
            else:
                if node.right != None:
                    node = node.right
                else:
                    break """
        return node
    
    def get_in_range(self, low, high, cmp_func = None):
        return (self.search_lax(low, cmp_func), self.search_lax(high, cmp_func))

""" 
D = Tree()

D.add(2,1,4,3,5)

print("ILR: ", D.ILR_list())
print("LIR: ", D.LIR_list())
print("LRI: ", D.LRI_list())

print(34, D.contains(34))

K = D.begin()

while K:
    print(K.value)
    K = K.next() """