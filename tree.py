import matplotlib.pyplot as plt
from typing import Optional, Any

class Node:
    """ Node of a Binary Search Tree """
    parent: Optional["Node"] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    value: Any = 0
    height: int = 1

    def __init__(self, value):
        """ Node constructor """
        self.value = value
    
    def prev(self):
        """ Returns the previous node in in-order traversal """
        node = self
        # si hay arbol izquierdo le entra
        if node.left:
            # entra al arbol izquierdo
            node = node.left
            # Obtiene el nodo más a la derecha
            while node != None and node.right != None:
                node = node.right
            return node
        # Si no hay nodos izquierdos
        while node.parent and node == node.parent.left:
            node = node.parent
        return node.parent
    
    def next(self):
        """ Returns the next node in in-order traversal """
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
        """ Detach this node from its parent """
        if (self.parent == None):
            return
        elif self == self.parent.left:
            self.parent.left = None
        else:
            self.parent.right = None
        self.parent = None
    
    def has_childs(self):
        """ Returns True if has at least one child """
        return self.left != None or self.right != None
    
    def has_full_capacity(self):
        """ Returns True if has both childs """
        return self.left != None and self.right != None
    
    def update_height(self):
        left_h = self.left.height if self.left else 0
        right_h = self.right.height if self.right else 0
        self.height = 1 + max(left_h, right_h)

    def balance_factor(self):
        left_h = self.left.height if self.left else 0
        right_h = self.right.height if self.right else 0
        return left_h - right_h
    
    def __str__(self):
        return f"{self.value}[{self.balance_factor()}]"

class Tree:
    """ Binary Search Tree """
    root: Optional["Node"] = None

    def search_closer(self, item, cmp_func = None):
        """ 
            Search but return allways
            - returns (Node, True) if found
            - returns (Node, False) if not found, Node is the parent where it could be added
            - returns (None, False) if tree is empty
        """
        if self.root == None:
            return (None, False)
        node = self.root
        if cmp_func != None:
            while node != None:
                if cmp_func(node.value) == 0:
                    return (node, True)
                elif cmp_func(node.value) < 0 and node.left != None:
                    node = node.left
                elif cmp_func(node.value) > 0 and node.right != None:
                    node = node.right
                else:
                    return (node, False)
            return (None, False)
        else:
            while node != None:
                if (item == node.value):
                    return (node, True)
                elif (item < node.value and node.left != None):
                    node = node.left
                elif (item > node.value and node.right != None):
                    node = node.right
                else:
                    return (node, False)
            return (None, False)

    def search(self, item):
        """ Search and return None if not found """
        target = self.search_closer(item)
        if target[1]:
            return target[0]
        return None
    
    def rotate_left(self, node: Node):
        """ Rotates the node to the left and returns the new root of the subtree """
        if node == None or node.right == None:
            return None
        
        X = node
        Y = X.right
        B = Y.left
        
        # Exchange parents
        Y.parent = X.parent
        if X.parent:
            if X == X.parent.left:
                X.parent.left = Y
            else:
                X.parent.right = Y

        # Rotate upper
        Y.left = X
        X.parent = Y

        # Exchange child
        X.right = B
        if B:
            B.parent = X
        
        # Update heights
        X.update_height()
        Y.update_height()
        # Ensure root has no parent
        if X == self.root:
            self.root = Y
        return Y
    
    def rotate_right(self, node: Node):
        """ Rotates the node to the right and returns the new root of the subtree """
        if node == None or node.left == None:
            return None
        
        X = node
        Y = X.left
        B = Y.right
        
        # Exchange parents
        Y.parent = X.parent
        if X.parent:
            if X == X.parent.left:
                X.parent.left = Y
            else:
                X.parent.right = Y

        # Rotate upper
        Y.right = X
        X.parent = Y

        # Exchange child
        X.left = B
        if B:
            B.parent = X
        
        # Update heights
        X.update_height()
        Y.update_height()
        # Ensure root has no parent
        if X == self.root:
            self.root = Y
        return Y

    def rebalance(self, node: Node):
        """ Rebalances the tree from the given node upwards """
        if node == None:
            return
        node.update_height()
        balance = node.balance_factor()
        # LL
        if balance > 1 and node.left.balance_factor() >= 0:
            node = self.rotate_right(node)
        # RR
        elif balance < -1 and node.right.balance_factor() <= 0:
            node = self.rotate_left(node)
        # LR
        elif balance > 1 and node.left.balance_factor() < 0:
            self.rotate_left(node.left)
            node = self.rotate_right(node)
        # RL
        elif balance < -1 and node.right.balance_factor() > 0:
            self.rotate_right(node.right)
            node = self.rotate_left(node)
        self.rebalance(node.parent)
    
    def add(self, *args):
        """ Add only if not exists """
        for item in args:
            target = self.search_closer(item)
            if target[0] == None: # Tree is empty
                self.root = Node(item)
                self.root.parent = None
            elif not target[1]: # Not found
                parent = target[0]
                if item < parent.value:
                    parent.left = Node(item)
                    parent.left.parent = parent
                else:
                    parent.right = Node(item)
                    parent.right.parent = parent
                self.rebalance(parent)
    
    def __del(self, node: Node):
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
            self.__del(ino)
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
    
    def delete(self, *args):
        for item in args:
            target = self.search(item)
            if target != None:
                self.__del(target)
    
    def __contains__(self, item):
        return self.search(item) != None
    
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

def plot_tree(node, x = 0, y = 0, x_distance = 1.0, level_gap = 1.5, axes = None, min_value = None, max_value = None):
    """ Recursively plot the tree using matplotlib """
    if node is None:
        return x
    
    if min_value is not None and max_value is not None:
        if node.value < max_value and node.value > min_value:
            color = "lightgreen"
        elif node.value == max_value or node.value == min_value:
            color = "yellow"
        else:
            color = "lightgray"

    # Plot left subtree
    if node.left:
        plot_tree(node.left, x - x_distance, y - level_gap, x_distance / 2, level_gap, axes, min_value=min_value, max_value=max_value)
        axes.plot([x, x - x_distance], [y, y - level_gap], 'k-')  # edge line
    
    if node.right:
        plot_tree(node.right, x + x_distance, y - level_gap, x_distance / 2, level_gap, axes, min_value=min_value, max_value=max_value)
        axes.plot([x, x + x_distance], [y, y - level_gap], 'k-')  # edge line

    axes.scatter(x, y, s=400, c=color, edgecolors="k", zorder=3)
    axes.text(x, y, str(node), ha="center", va="center", fontsize=10, zorder=4)

def draw_tree(tree: Tree, min_value = None, max_value = None):
    fig,ax = plt.subplots(figsize=(10, 6))
    ax.set_axis_off()
    if tree.root:
        plot_tree(tree.root, x=0, y=0, level_gap=2, axes=ax, min_value=min_value, max_value=max_value)
    ax.set_xlim(-0.5, 0.5)
    plt.show()