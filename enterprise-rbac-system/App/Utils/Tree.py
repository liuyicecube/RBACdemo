"""Tree Utils"""

from typing import List, Dict, Any, Optional


class TreeUtils:
    """树形结构工具类"""

    @staticmethod
    def list_to_tree(
        data: List[Dict[str, Any]],
        id_key: str = "id",
        parent_id_key: str = "parent_id",
        children_key: str = "children"
    ) -> List[Dict[str, Any]]:
        """将列表转换为树形结构"""
        # 创建节点映射
        node_map = {item[id_key]: item for item in data}

        # 构建树形结构
        tree = []
        for item in data:
            parent_id = item[parent_id_key]
            if parent_id is None or parent_id == 0 or parent_id not in node_map:
                # 根节点：parent_id为None、0或不存在于节点映射中
                tree.append(item)
            else:
                # 子节点
                parent = node_map[parent_id]
                if children_key not in parent:
                    parent[children_key] = []
                parent[children_key].append(item)

        return tree

    @staticmethod
    def get_tree_node_by_id(
        tree: List[Dict[str, Any]],
        node_id: Any,
        id_key: str = "id",
        children_key: str = "children"
    ) -> Optional[Dict[str, Any]]:
        """根据ID获取树形结构中的节点"""
        for node in tree:
            if node[id_key] == node_id:
                return node
            if children_key in node:
                result = TreeUtils.get_tree_node_by_id(node[children_key], node_id, id_key, children_key)
                if result:
                    return result
        return None

    @staticmethod
    def get_tree_node_ancestors(
        tree: List[Dict[str, Any]],
        node_id: Any,
        id_key: str = "id",
        parent_id_key: str = "parent_id",
        children_key: str = "children"
    ) -> List[Dict[str, Any]]:
        """获取节点的所有祖先节点"""
        # 先将树形结构转换为节点映射
        node_map = {}

        def build_node_map(nodes):
            for node in nodes:
                node_map[node[id_key]] = node
                if children_key in node:
                    build_node_map(node[children_key])

        build_node_map(tree)

        # 查找祖先节点
        ancestors = []
        current = node_map.get(node_id)
        while current and parent_id_key in current and current[parent_id_key] is not None:
            parent = node_map.get(current[parent_id_key])
            if parent:
                ancestors.insert(0, parent)
                current = parent
            else:
                break

        return ancestors

    @staticmethod
    def get_tree_node_descendants(
        tree: List[Dict[str, Any]],
        node_id: Any,
        id_key: str = "id",
        children_key: str = "children"
    ) -> List[Dict[str, Any]]:
        """获取节点的所有后代节点"""
        descendants = []

        def collect_descendants(nodes):
            for node in nodes:
                descendants.append(node)
                if children_key in node:
                    collect_descendants(node[children_key])

        node = TreeUtils.get_tree_node_by_id(tree, node_id, id_key, children_key)
        if node and children_key in node:
            collect_descendants(node[children_key])

        return descendants

    @staticmethod
    def filter_tree(
        tree: List[Dict[str, Any]],
        filter_func: callable,
        children_key: str = "children"
    ) -> List[Dict[str, Any]]:
        """根据条件过滤树形结构"""
        filtered_tree = []

        for node in tree:
            # 复制节点，避免修改原数据
            node_copy = node.copy()

            # 处理子节点
            if children_key in node_copy:
                filtered_children = TreeUtils.filter_tree(node_copy[children_key], filter_func, children_key)
                node_copy[children_key] = filtered_children

            # 检查当前节点或其子节点是否需要保留
            if filter_func(node_copy) or (children_key in node_copy and node_copy[children_key]):
                filtered_tree.append(node_copy)

        return filtered_tree

    @staticmethod
    def flatten_tree(
        tree: List[Dict[str, Any]],
        children_key: str = "children"
    ) -> List[Dict[str, Any]]:
        """将树形结构展平为列表"""
        flattened = []

        def flatten(node):
            node_copy = node.copy()
            if children_key in node_copy:
                children = node_copy.pop(children_key)
                flattened.append(node_copy)
                for child in children:
                    flatten(child)
            else:
                flattened.append(node_copy)

        for node in tree:
            flatten(node)

        return flattened

    @staticmethod
    def build_tree(
        data: List[Dict[str, Any]],
        id_key: str = "id",
        parent_id_key: str = "parent_id",
        children_key: str = "children"
    ) -> List[Dict[str, Any]]:
        """构建树形结构"""
        return TreeUtils.list_to_tree(data, id_key, parent_id_key, children_key)

    @staticmethod
    def sort_tree(
        tree: List[Dict[str, Any]],
        sort_key: str = "sort",
        children_key: str = "children"
    ) -> List[Dict[str, Any]]:
        """根据指定键对树形结构进行排序"""
        # 先对当前层级的节点进行排序
        tree.sort(key=lambda x: x.get(sort_key, 0))

        # 递归对每个节点的子节点进行排序
        for node in tree:
            if children_key in node and node[children_key]:
                node[children_key] = TreeUtils.sort_tree(node[children_key], sort_key, children_key)

        return tree
