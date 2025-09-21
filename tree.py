""" Module for defining a balanced binary search tree with visualization capabilities """

import matplotlib.pyplot as plt
import matplotlib.patches as pat
from matplotlib.animation import FuncAnimation
from typing import Optional, Any

class Node:
    """ Node of a Binary Search Tree """
    parent: Optional["Node"] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    value: Any = 0
    height: int = 1

    def __init__(self, value):
        """ 
        Node constructor
        Args:
            value (Any): The value of the node
        """
        self.value = value
    
    def prev(self) -> Optional["Node"]:
        """ 
        Returns the previous node in in-order traversal
        """
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
    
    def next(self) -> Optional["Node"]:
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
    
    def has_childs(self) -> bool:
        """ Returns True if has at least one child """
        return self.left != None or self.right != None
    
    def has_full_capacity(self) -> bool:
        """ Returns True if has both childs """
        return self.left != None and self.right != None
    
    def update_height(self):
        """ Updates the height of the node """
        left_h = self.left.height if self.left else 0
        right_h = self.right.height if self.right else 0
        self.height = 1 + max(left_h, right_h)

    def balance_factor(self) -> int:
        """ Returns the balance factor of the node """
        left_h = self.left.height if self.left else 0
        right_h = self.right.height if self.right else 0
        return left_h - right_h
    
    def __str__(self):
        return f"{self.value}[{self.balance_factor()}]"

class Tree:
    """ Binary Search Tree """
    root: Optional["Node"] = None

    def search_closer(self, item, cmp_func = None) -> tuple[Optional[Node], bool]:
        """
        Search but return allways
        - returns (Node, True) if found
        - returns (Node, False) if not found, Node is the parent where it could be added
        - returns (None, False) if tree is empty

        Args:
            item (Any): The item to search for
            cmp_func (callable, optional): A comparison function that takes an item and returns: If None, the default comparison operators will be used.
        
        Returns:
            (Optional[Node], bool): A tuple containing the found node (or parent)
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

    def search(self, item) -> Optional[Node]:
        """ 
        Search and return None if not found
        Args:
            item (Any): The item to search for
        Returns:
            Optional[Node]: The found node or None if not found
        """
        target = self.search_closer(item)
        if target[1]:
            return target[0]
        return None
    
    def rotate_left(self, node: Node) -> Optional[Node]:
        """ 
        Rotates the node to the left and returns the new root of the subtree
        Args:
            node (Node): The node to rotate
        Returns:
            Optional[Node]: The new root of the subtree or None if rotation is not possible
        """
        if node == None or node.right == None:
            return node
        
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
    
    def rotate_right(self, node: Node) -> Optional[Node]:
        """ 
        Rotates the node to the right and returns the new root of the subtree
        Args:
            node (Node): The node to rotate
        Returns:
            Optional[Node]: The new root of the subtree or None if rotation is not possible
        """
        if node == None or node.left == None:
            return node
        
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
        """ 
        Rebalances the tree from the given node upwards
        Args:
            node (Node): The node to start rebalancing from
        """
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
        """ 
        Add only if not exists
        Args:
            *args (Any): The items to add
        """
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
        """
        Delete items if they exist
        Args:
            *args (Any): The items to delete
        """
        for item in args:
            target = self.search(item)
            if target != None:
                self.__del(target)
    
    def __contains__(self, item):
        return self.search(item) != None
    
    def contains(self, item) -> bool:
        """
        Check if the tree contains the item
        Args:
            item (Any): The item to check for
        Returns:
            bool: True if the item is in the tree, False otherwise
        """
        return item in self
    
    def clear(self):
        """ Clear the tree """
        self.root = None
    
    def LIR_list(self) -> list:
        """
        Returns the in-order traversal of the tree as a list
        """
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
    
    def ILR_list(self) -> list:
        """
        Returns the pre-order traversal of the tree as a list
        """
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
    
    def LRI_list(self) -> list:
        """
        Returns the post-order traversal of the tree as a list
        """
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
    
    def BREADTH_list(self) -> list:
        """
        Returns the breadth-first traversal of the tree as a list
        """
        arr = []
        def _add(node: Node, depth=0):
            if (len(arr) <= depth):
                arr.append([])
            arr[depth].append(node.value)
            if (node.left):
                _add(node.left, depth + 1)
            if (node.right):
                _add(node.right, depth + 1)
        if (self.root):
            _add(self.root)
        return [item for sublist in arr for item in sublist]

def draw_tree(tree: Tree, min_value = None, max_value = None):
    """ 
    Draws the tree with its traversals using matplotlib
    Args:
        tree (Tree): The tree to draw
        min_value (Any, optional): A minimum value to highlight
        max_value (Any, optional): A maximum value to highlight
    """
    figure, axes = plt.subplots(figsize=(10, 6))
    axes.set_axis_off()

    positions = {}

    def _fill(node, x=0, y=0, depth=0):
        if node is None:
            return
        
        color = "lightgray"
        if min_value is not None and max_value is not None:
            if node.value < max_value and node.value > min_value:
                color = "lightgreen"
            elif node.value == max_value or node.value == min_value:
                color = "yellow"

        positions[(node.value.x, node.value.y)] = (x, y)

        if node.left:
            axes.plot([x, x - 1/(2**depth)], [y, y - 1], 'k-') 
            _fill(node.left, x - 1/(2**depth), y - 1, depth + 1)
        if node.right:
            axes.plot([x, x + 1/(2**depth)], [y, y - 1], 'k-') 
            _fill(node.right, x + 1/(2**depth), y - 1, depth + 1)

        w = 0.4 / 10
        h = 0.4
        axes.add_patch(pat.Rectangle((x - w / 2, y - h / 2), width=w, height=h, color=color, zorder=3))
        axes.text(x, y, f"{node.value.x},{node.value.y}", ha="center", va="center", fontsize=7, zorder=4)

    _fill(tree.root)

    axes.set_xlim(-0.5, 0.5)
    axes.text(-0.15, -1, "PRE", ha="center", va="center", fontsize=12, zorder=4, color=(1, 0, 0, 0.8))
    axes.text(-0.05, -1, "INO", ha="center", va="center", fontsize=12, zorder=4, color=(0, 1, 0, 0.8))
    axes.text(0.05, -1, "POS", ha="center", va="center", fontsize=12, zorder=4, color=(0, 0, 1, 0.8))
    axes.text(0.15, -1, "Breadth", ha="center", va="center", fontsize=12, zorder=4, color=(1, 1, 0, 0.8))

    h = 0.6
    w = h / 10
    preo_f = axes.add_patch(pat.Rectangle((0, 0), width=w, height=h, color=(1, 0, 0, 0.8), zorder=1))
    ino_f = axes.add_patch(pat.Rectangle((0, 0), width=w, height=h, color=(0, 1, 0, 0.8), zorder=1))
    poso_f = axes.add_patch(pat.Rectangle((0, 0), width=w, height=h, color=(0, 0, 1, 0.8), zorder=1))
    deptho_f = axes.add_patch(pat.Rectangle((0, 0), width=w, height=h, color=(1, 1, 0, 0.8), zorder=1))
    while plt.fignum_exists(figure.number):
        PRE_l = tree.ILR_list()
        INO_l = tree.LIR_list()
        POS_l = tree.LRI_list()
        DEP_l = tree.BREADTH_list()
        for i in range(len(PRE_l)):
            pos = positions[(PRE_l[i].x, PRE_l[i].y)]
            preo_f.set_xy((pos[0] - w / 2, pos[1] - h / 2))

            pos = positions[(INO_l[i].x, INO_l[i].y)]
            ino_f.set_xy((pos[0] - w / 2, pos[1] - h / 2))

            pos = positions[(POS_l[i].x, POS_l[i].y)]
            poso_f.set_xy((pos[0] - w / 2, pos[1] - h / 2))

            pos = positions[(DEP_l[i].x, DEP_l[i].y)]
            deptho_f.set_xy((pos[0] - w / 2, pos[1] - h / 2))
            plt.pause(0.4)
            if not plt.fignum_exists(figure.number):
                break
    
    plt.show()