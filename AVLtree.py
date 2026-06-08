class Node:
    def __init__(self, key: int):
        self.key = key
        self.left: Node | None = None
        self.right: Node | None = None
        self.height: int = 1

class AVL_tree:
    def __init__(self):
        pass

    def get_height(self, node: Node | None = None) -> int:
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node: Node | None) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y: Node) -> Node:
        x = y.left
        T2 = x.right #type: ignore

        x.right = y #type: ignore
        y.left = T2

        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right)) #type: ignore
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right)) #type: ignore

        return x #type: ignore
    
    def left_rotate(self, x: Node) -> Node:
        y = x.right
        T2 = y.left #type: ignore

        y.left = x #type: ignore
        x.right = T2

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right)) #type: ignore
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right)) #type: ignore

        return y #type: ignore
    
    def insert(self, root: Node | None, key: int) -> Node:
        # 1. Обычная вставка как в BST (Бинарное дерево поиска)
        if not root:
            return Node(key)
        
        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root # Дубликаты не вставляем

        # 2. Обновляем высоту текущего узла
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Получаем фактор баланса, чтобы проверить, не нарушился ли он
        balance = self.get_balance(root)

        # 4. Если баланс нарушен, разбираем 4 случая:

        # Case 1: Left-Left
        if balance > 1 and key < root.left.key: # type: ignore
            return self.right_rotate(root)

        # Case 2: Right-Right
        if balance < -1 and key > root.right.key: # type: ignore
            return self.left_rotate(root)

        # Case 3: Left-Right
        if balance > 1 and key > root.left.key: # type: ignore
            root.left = self.left_rotate(root.left) # type: ignore
            return self.right_rotate(root)

        # Case 4: Right-Left
        if balance < -1 and key < root.right.key: # type: ignore
            root.right = self.right_rotate(root.right) # type: ignore
            return self.left_rotate(root)

        return root

    def preorder(self, root: Node | None, res: None | list[str] = None) -> list[str]:
        if res is None: res: list[str] = []
        if root:
            res.append(f"{root.key}(H:{root.height})")
            self.preorder(root.left, res)
            self.preorder(root.right, res)
        return res