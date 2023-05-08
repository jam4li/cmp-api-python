
class CompleteBinaryTree:
    def __init__(self):
        # Add None at the 0th index, so the actual nodes start from index 1.
        # This helps in simplifying the calculations for parent and child indices.
        self.nodes = [None]
        # Initialize a dictionary to store the binary place for each user.
        self.binary_places = {}

    def insert(self, user_id, parent_id, child_side=None):
        # The tree should start with the root user, parent_id should be None for root user.
        if not self.nodes and parent_id is not None:
            raise ValueError("Root user must be inserted first")

        # If the parent_id is None, it means we are inserting the root user.
        if parent_id is None:
            self.nodes.append(user_id)
            # The root node has a binary place of "0"
            self.binary_places[user_id] = "0"
            return 0

        # If the parent_id is not in the nodes, raise an error.
        if parent_id not in self.nodes:
            raise ValueError("Parent not found in the tree")

        # Find the indices for the left and right children of the parent.
        parent_index = self.nodes.index(parent_id)
        left_child_index = self.find_left_child_index(parent_index)
        right_child_index = self.find_right_child_index(parent_index)

        # If the child_side is 'left', insert the new user to the left of the parent.
        if child_side == 'left':
            # If the left child position is empty, insert the new user there.
            if left_child_index >= len(self.nodes) or self.nodes[left_child_index] is None:
                self.nodes.extend(
                    [None] * (left_child_index + 1 - len(self.nodes)),
                )
                self.nodes[left_child_index] = user_id
                # Append "0" for left child
                self.binary_places[user_id] = self.binary_places[parent_id] + "0"

        # If the child_side is 'right', insert the new user to the right of the parent.
        elif child_side == 'right':
            # If the right child position is empty, insert the new user there.
            if right_child_index >= len(self.nodes) or self.nodes[right_child_index] is None:
                self.nodes.extend(
                    [None] * (right_child_index + 1 - len(self.nodes)),
                )
                self.nodes[right_child_index] = user_id
                # Append "1" for right child
                self.binary_places[user_id] = self.binary_places[parent_id] + "1"

    def find_left_child_index(self, index):
        # Calculate the left child index.
        return 2 * index

    def find_right_child_index(self, index):
        # Calculate the right child index.
        return 2 * index + 1

    def find_left_most_descendant(self, index):
        # Keep traversing the left children until there are no more left children.
        while index < len(self.nodes):
            left_child_index = self.find_left_child_index(index)
            if left_child_index >= len(self.nodes) or self.nodes[left_child_index] is None:
                break
            index = left_child_index
        return index

    def insert_new_user(self, new_user_id, parent_user_id, child_side="left"):
        # Get the parent user index
        parent_user_index = self.nodes.index(parent_user_id)

        if child_side == "left":
            # Find the left child index of the parent user
            child_index = self.find_left_child_index(parent_user_index)
        elif child_side == "right":
            # Find the right child index of the parent user
            child_index = self.find_right_child_index(parent_user_index)
        else:
            raise ValueError("Invalid child_side, must be 'left' or 'right'")

        # If the child position is empty, insert the new user there
        if child_index >= len(self.nodes) or self.nodes[child_index] is None:
            self.insert(new_user_id, parent_user_id, child_side)
        else:
            # If the child position is taken, find the left-most or right-most descendant
            if child_side == "left":
                descendant_index = self.find_left_most_descendant(
                    parent_user_index)
            else:
                descendant_index = self.find_right_most_descendant(
                    parent_user_index)

            # Insert the new user as the left or right child of the left-most or right-most descendant
            self.insert(new_user_id, self.nodes[descendant_index], child_side)

    def find_right_most_descendant(self, index):
        # Keep traversing the right children until there are no more right children.
        while index < len(self.nodes):
            right_child_index = self.find_right_child_index(index)
            if right_child_index >= len(self.nodes) or self.nodes[right_child_index] is None:
                break
            index = right_child_index
        return index

    def __str__(self):
        # If there are no nodes in the tree, return "Empty tree".
        if not self.nodes:
            return "Empty tree"

        # Initialize an empty list to store the string representation of each level.
        result = []
        level = 0

        # Iterate through the levels of the tree.
        while 2**level - 1 < len(self.nodes):
            # Calculate the start and end indices for the current level.
            start = 2**level - 1
            end = 2**(level + 1) - 1
            # Create a string representation of the nodes in the current level.
            nodes = ', '.join(
                str(x) if x is not None else '-' for x in self.nodes[start:end])
            # Append the string representation of the current level to the result list.
            result.append(f"Level {level}: {nodes}")
            level += 1

        # Join the result list into a single string and return it.
        return "\n".join(result)


if __name__ == '__main__':
    tree = CompleteBinaryTree()

    tree.insert_new_user("user1", None)  # User1 is the root
    tree.insert_new_user("user2", "user1", "left")
    tree.insert_new_user("user3", "user1", "right")

    tree.insert_new_user("user4", "user1", "left")

    tree.insert_new_user("user5", "user1", "left")

    tree.insert_new_user("user6", "user3", "right")

    tree.insert_new_user("user7", "user3", "left")

    print(tree.nodes)
    print(tree.binary_places)
