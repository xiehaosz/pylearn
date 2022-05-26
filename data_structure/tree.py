from graphviz import Digraph
import uuid
from random import sample
import time

# # binarytree模块: https://pypi.org/project/binarytree/
# from binarytree import tree
# my_tree = tree(height=4, is_perfect=False)
# # print(my_tree.height)
# # print(my_tree.leaves)
# # print(my_tree.preorder)
# # print(my_tree.is_complete)
# print(my_tree)

# 利用Graphviz实现二叉树的可视化


def func_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func()
        end = time.time()
        msecs = (end - start) * 1000
        print('time elapse:',  end-start)
    return wrapper


class Node:
    def __init__(self, data):
        self.data = data    # 节点值
        self.left = None    # 左子节点
        self.right = None   # 右子节点

        # 如果在节点属性中添加parent, 平衡的时候需要同步修改
        # 如果不添加parent属性, 在查找过程中需要记录父节点, 便于后续的回溯处理

    def add_node(self, data, avl=False):
        """
        （递归）插入节点
        :param data: 待插入节点的值
        :param avl:  是否平衡节点(生成avl树）
        :return:
        """
        # 递归实现树的创建
        new_node = Node(data)

        if self.data is None:
            self.data = data
        else:
            if data == self.data:               # 插入值已存在直接返回
                return
            else:
                if data < self.data:            # 新值较小，放左边
                    if self.left is None:       # 若空，则新建插入节点
                        self.left = new_node
                    else:                       # 否则，递归往下查找
                        self.left.add_node(data, avl)
                else:                           # 新值较大，放右边
                    if self.right is None:      # 若空，则新建插入节点
                        self.right = new_node
                    else:                       # 否则，递归往下查找
                        self.right.add_node(data, avl)
                if avl:
                    self.judge_node()

    def _add_node_rec(self, data, avl=False):
        """
        （非递归）插入节点
        :param data: 待插入节点的值
        :param avl:  是否平衡节点(生成avl树）
        :return:
        """
        branch = []     # 记录查找路径, 用于回溯父节点和平衡
        if self.data is None:
            self.data = data
        else:
            cur_node = self
            new_node = Node(data)

            while cur_node:
                branch.append(cur_node)
                if data == cur_node.data:                   # 插入值已存在直接返回
                    return
                else:
                    if data < cur_node.data:
                        if cur_node.left:
                            cur_node = cur_node.left
                        else:
                            cur_node.left = new_node
                            break
                    else:
                        if cur_node.right:
                            cur_node = cur_node.right
                        else:
                            cur_node.right = new_node
                            break
            if avl:
                while branch:
                    branch.pop().judge_node()

    def _height(self, node):
        """
        （递归）获得深度
        :param node:
        :return:
        """
        if node is None:
            return 0
        return max(self._height(node.left), self._height(node.right)) + 1

    def height(self, node=None, notice=False):
        """
        （递归）调用递归获得深度
        :param node:
        :param notice:
        :return:
        """
        node = self if node is None else node
        height = self._height(node)
        if notice:
            print('height: %s' % height)
        return height

    def leaves(self):
        """
        （递归）获得二叉树的叶子节点
        :return:
        """
        res = list()
        if self.data is None:
            return res
        if self.left is None and self.right is None:
            res.append(self)
        else:
            if self.left:
                res.extend(self.left.leaves())
            if self.right:
                res.extend(self.right.leaves())
        return res

    def min_node(self, node=None):
        # 最小(左)叶子
        cur_node = node if node else self
        parent = None
        while cur_node.left:
            parent = cur_node
            cur_node = cur_node.left
        return cur_node, parent

    def max_node(self, node=None):
        # 最大(右)叶子
        cur_node = node if node else self
        parent = None
        while cur_node.right:
            parent = cur_node
            cur_node = cur_node.right
        return cur_node, parent

    def _del_node(self, node, parent):
        """
        从树中删除节点, 返回节点值
        :param node: 待删除节点
        :param parent: 待删除节点的父节点
        :return:
        """
        if parent:  # 非根节点
            if not (parent.left == node or parent.right == node):
                raise RuntimeError('节点关系错误.')

        # 第一种情况: 待删除节点有两棵子树, 取左子树的最大元素或者右子树的最小元素进行替换, 然后将最大元素最小元素原位置置空
        if node.left and node.right:
            # 这里用左子树的最大元素替换
            sub_node, sub_parent = self.max_node(node.left)
            node.data = sub_node.data

            if sub_parent:  # 原位置置空, 是否要考虑左子树的最大元素有左孩子的情况?
                sub_parent.right = sub_node.left if sub_node.left else None
            else:
                node.left = sub_node.left if sub_node.left else None

        # 第二种情况: 待删除节点只有只有一棵子树, 将孩子连接到父节点的原分支上(删除根节点要特殊处理)
        # elif node.left or node.right:
        #     if parent.data > node.data:  # 自身是左节点
        #         parent.left = node.left if node.left else node.right
        #     else:
        #         parent.right = node.left if node.left else node.right
        elif node.left or node.right:   # 直接用孩子的值替换原节点, 可以兼容根节点
            sub_node = node.left if node.left else node.right
            node.data = sub_node.data
            node.left = sub_node.left
            node.right = sub_node.right

        # 第三种情况: 叶子节点, 直接将父节点的对应分支置为None
        else:
            if parent:
                if parent.data > node.data:
                    parent.left = None
                else:
                    parent.right = None
            else:
                # 能进入到这个分支的树, 只有根节点
                print('Only one node in this tree.')

    def del_node(self, data, avl=False):
        """
        实现平衡树的节点删除
        :param data:
        :param avl:  是否平衡节点(生成avl树）
        :return:
        """
        node, branch = self.find(data)              # 先找到目标节点和节点路径
        if node:
            parent = branch[-1] if branch else None
            self._del_node(node, parent)

            if avl:
                while branch:       # 平衡回溯
                    branch.pop().judge_node()

    def _del_node_rec(self, data, avl=False):
        """
        TODO （递归）实现平衡树的节点删除
        :param data:
        :param avl:  是否平衡节点(生成avl树）
        :return:
        """
        node, branch = self.find(data)              # 先找到节点
        if node:
            parent = branch[-1] if branch else None
            self._del_node(node, parent)

            if avl:
                while branch:       # 平衡回溯
                    branch.pop().judge_node()

    def find(self, data, notice=False):
        """
        :param data: 查找目标
        :param notice: 打印提示信息
        :return: 返回目标节点和节点路径
        """
        branch = []     # 记录查找路径, 用于回溯父节点和平衡
        cur_node = self
        layer = 0       # 节点所在的深度(根节点的深度为0)
        while cur_node:
            if cur_node.data == data:
                break
            else:
                layer += 1
                branch.append(cur_node)
                if data < cur_node.data:
                    cur_node = cur_node.left
                else:
                    cur_node = cur_node.right

        if notice and cur_node:
            print('%s is in layer %s.' % (data, layer))
        else:
            print('%s is not in tree.' % data)
            return cur_node, branch

    def _find_rec(self, node, data):
        """
        （递归）实现查找
        :param data: 查找目标
        :return:
        """
        # TODO: 采用递归方式实现查找，如果要返回搜索路径，要改为列表返回
        if node:
            if data < node.data:
                return self._find_rec(node.left, data)
            elif data > node.data:
                return self._find_rec(node.right, data)
            else:
                return node
        return None

    def level_order(self, node=None, full=False, notice=True):
        node = self if node is None else node
        if full:
            # 空节点也打印出来, 方便观察结构
            return self._full_order(node)
        else:
            res = []
            level_node = [node]
            while level_node:
                level_data = list()
                for i in range(len(level_node)):
                    # 循环一层的节点, 并使用其左右子节点进行替换, 获得下一层节点
                    node = level_node.pop(0)
                    if node.left:
                        level_node.append(node.left)
                    if node.right:
                        level_node.append(node.right)

                    level_data.append(node.data)
                res.append(level_data)
            if notice:
                print('tree height: %s' % len(res))
                for lv in res:
                    print('\t%s' % lv)
                print('level-order: %s' % res)
            return res

    def level_order_2(self):
        """另一种层遍历的逻辑, 先获得树的高度"""
        # 返回某个节点的左孩子
        def get_left_child(node):
            return node.left if node.left is not None else None

        # 返回某个节点的右孩子
        def get_right_child(node):
            return node.right if node.right is not None else None

        # 层序遍历列表
        level_order = []
        # 是否添加根节点中的数据
        if self.data is not None:
            level_order.append([self])

        # 二叉树的高度
        height = self.height()
        if height >= 1:
            # 对第二层及其以后的层数进行操作, 在level_order中添加节点而不是数据
            for _ in range(2, height + 1):
                level = []  # 该层的节点
                for node in level_order[-1]:
                    # 如果左孩子非空，则添加左孩子
                    if get_left_child(node):
                        level.append(get_left_child(node))
                    # 如果右孩子非空，则添加右孩子
                    if get_right_child(node):
                        level.append(get_right_child(node))
                # 如果该层非空，则添加该层
                if level:
                    level_order.append(level)

            # 取出每层中的数据
            for i in range(0, height):  # 层数
                for index in range(len(level_order[i])):
                    level_order[i][index] = level_order[i][index].data
        return level_order

    def _full_order(self, node, null_data=0):
        res = [[node.data]]
        null = Node(null_data)      # 填充空节点

        level_node = [[node.left if node.left else null, node.right if node.right else null]]
        for l in range(self._height(node) - 1):
            level_data = list()
            for i in range(len(level_node)):
                # 循环一层的节点, 并使用其左右子节点进行替换, 获得下一层节点
                node_pair = level_node.pop(0)
                level_data.extend([node.data for node in node_pair])
                for node in node_pair:
                    level_node.append([node.left if node.left else null, node.right if node.right else null])
            res.append(level_data)
        print('tree height: %s' % len(res))
        for lv in res:
            print('\t%s' % lv)
        return res

    def get_order(self, order='inorder', node=None, notice=False):
        node = self if node is None else node
        if order == 'preorder':
            res = node._preorder(node)
        elif order == 'inorder':
            res = node._inorder(node)
        elif order == 'postorder':
            res = node._postorder(node)
        else:  # order == 'level_order':
            res = node.level_order(node)
        if notice:
            print('%s: %s' % (order, res))
        return res

    def _preorder(self, node):
        # 递归实现先序遍历: 当到达某个节点时, 先输出该节点, 再访问左子节点, 最后访问右子节点
        res = list()
        if node:
            res.append(node.data)
            res.extend(self._preorder(node.left))
            res.extend(self._preorder(node.right))
        return res

    def _inorder(self, node):
        # 递归实现中序遍历: 当到达某个节点时, 先访问左子节点, 再输出该节点, 最后访问右子节点
        res = list()
        if node:
            res = self._inorder(node.left)
            res.append(node.data)
            print(node.data, node.parent)
            res.extend(self._inorder(node.right))
        return res

    def _postorder(self, node):
        # 递归实现后序遍历: 当到达某个节点时, 先访问左子节点, 再访问右子节点, 最后输出该节点
        res = []
        if node:
            res = self._postorder(node.left)
            res.extend(self._postorder(node.right))
            res.append(node.data)
        return res

    def preorder(self, node=None, notice=False):
        # 栈实现先序遍历: Root -> Left -> Right
        node = self if node is None else node

        res = list()
        stack = list()
        node = node
        while node or stack:
            while node:
                res.append(node.data)   # 输出节点值
                stack.append(node)      # 为了后续查找右节点,入栈缓存
                node = node.left        # 向左
            node = stack.pop(-1).right  # 左节点为空,从最近的历史节点开始向右
        if notice:
            print('preorder: %s' % res)
        return res

    def inorder(self, node=None, notice=False):
        # 栈实现中序遍历: Left -> Root -> Right
        node = self if node is None else node
        res = list()
        stack = list()
        node = node
        while node or stack:
            while node:
                stack.append(node)      # 为了后续查找右节点,入栈缓存
                node = node.left        # 向左
            node = stack.pop(-1)
            res.append(node.data)       # 输出节点值
            node = node.right           # 左节点为空,从最近的历史节点开始向右
        if notice:
            print('inorder: %s' % res)
        return res

    def postorder(self, node=None, notice=False):
        # 栈实现后序遍历: Left -> Right -> Root
        # 后续遍历和先序、中序遍历不太一样, 在决定是否可以输出当前节点的值的时候，需要考虑其左右子树是否都已经遍历完成
        node = self if node is None else node
        res = list()
        stack = []
        last_visit = None               # 若lastVisit等于当前考查节点的右子树, 表示已经遍历完右树, 可以输出该节点
        node = node
        while node or stack:
            while node:
                stack.append(node)      # 为了后续查找右节点,入栈缓存
                node = node.left        # 向左

            node = stack[-1]            # peek()
            if node.right is None or node.right == last_visit:
                res.append(node.data)       # 输出节点值
                last_visit = stack.pop(-1)
                node = None
            else:
                node = node.right           # 左节点为空,从最近的历史节点开始向右
        if notice:
            print('postorder: %s' % res)
        return res

    @staticmethod
    def _right_rotate(node):
        # https://blog.csdn.net/weixin_45666566/article/details/108092977
        # https://blog.csdn.net/weixin_44778155/article/details/101839017
        # LL型: 左高右旋转
        temp = Node(node.data)          # 创建新的结点，以当前根结点的值
        temp.right = node.right         # 把新结点的右子树设为当前结点的右子树
        temp.left = node.left.right     # 把新结点的左子树设为当前结点的左子树的右子树
        node.data = node.left.data      # 把当前结点的值替换成它的左子结点的值
        node.left = node.left.left      # 把当前结点的左子树设置成当前结点的左子树的左子树
        node.right = temp               # 把当前结点的右子结点设置成（指向）新的结点

    @staticmethod
    def _left_rotate(node):
        # RR型: 右高左旋转
        temp = Node(node.data)          # 创建新的结点，以当前根结点的值
        temp.left = node.left           # 把新结点的左子树设为当前结点的左子树
        temp.right = node.right.left    # 把新结点的右子树设为当前结点的右子树的左子树
        node.data = node.right.data     # 把当前结点的值替换成它的右子结点的值
        node.right = node.right.right   # 把当前结点的右子树设置成当前结点的右子树的右子树
        node.left = temp                # 把当前结点的左子结点设置成（指向）新的结点

    def judge_node(self):
        # 二叉排序树平衡(AVL: Adelson-Velsky and Landis Tree)
        # self.level_order(full=True)   # 打印层级结构
        if self._height(self.left) - self._height(self.right) > 1:
            # 很多代码会判断self.left不为空, 实际上如果上一个条件满足, self.left必定不为空

            if self._height(self.left.right) > self._height(self.left.left):
                # LR型: 左子树先左旋, 再右旋
                self._left_rotate(self.left)
            self._right_rotate(self)  # LL型: 右旋

        elif self._height(self.right) - self._height(self.left) > 1:
            if self._height(self.right.left) > self._height(self.right.right):
                # RL型: 右子树先右旋, 再左旋
                self._right_rotate(self.right)
            self._left_rotate(self)   # RR型: 右旋


'''树的创建---------------------------------------------'''
root = 5
nodes = [4, 17, 2, 16, 3, 20, 7, 1, 12, 10, 18, 13, 15, 14, 8, 6, 11, 19, 1, 9]

# tree = Node(root)  # 第一个为根节点
# for n in nodes:
#     tree.add_node(n)
# print('tree1 height: %s, inorder: %s ' % (tree.height(), tree.inorder()))
# tree.level_order()
#
#
# tree = Node(root)  # 第一个为根节点
# for n in nodes:
#     tree.add_node_(n)
# print('tree1 height: %s, inorder: %s ' % (tree.height(), tree.inorder()))
# tree.level_order()

tree_avl = Node(root)
for n in nodes:
    tree_avl.add_node(n, avl=True)
print('tree2 height: %s, inorder: %s ' % (tree_avl.height(), tree_avl.inorder()))
tree_avl.level_order(full=True)

tree_avl = Node(root)
for n in nodes:
    tree_avl.add_node_(n, avl=True)
print('tree2 height: %s, inorder: %s ' % (tree_avl.height(), tree_avl.inorder()))
tree_avl.level_order(full=True)


print([n.data for n in tree_avl.leaves()])
# '''树的节点删除-----------------------------------------'''
# tree_1.del_node(20)
# print('tree2 height: %s, inorder: %s ' % (tree_1.height(), tree_1.inorder()))
# tree_1.level_order()

'''树的查找与遍历---------------------------------------------'''
# root = 5
# nodes = [4, 6, 2, 8, 3, 9, 7, 1]
# tree = Node(root)
# for i in nodes:
#     tree.insert(i)

# nodes = [4, 21, 6, 8]
# [tree_2.find(i, notice=True) for i in nodes]

# tree.get_order('preorder', notice=True)
# tree.preorder(notice=True)
#
# tree_2.get_order('inorder', notice=True)
# tree.inorder(notice=True)
#
# tree.get_order('postorder', notice=True)
# tree.postorder(notice=True)
#
# tree.level_order(notice=True)
# tree.level_order(full_node=True)
