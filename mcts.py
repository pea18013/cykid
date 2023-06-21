import copy
import math
import random


class MCTSTreeNode:
    def __init__(self, parent, action):
        self.parent = parent
        self.action = action
        self.children = {}
        self.n_visits = 0
        self.q_value = 0.0
        self.u_value = 0.0

    def add_child(self, action):
        if action not in self.children:
            self.children[action] = MCTSTreeNode(self, action)

    def update(self, reward):
        self.n_visits += 1
        self.q_value += (reward - self.q_value) / self.n_visits

    def get_value(self, c_puct):
        self.u_value = c_puct * math.sqrt(self.parent.n_visits) / (1 + self.n_visits)
        return self.q_value + self.u_value

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None


class MCTS:
    def __init__(self, game, c_puct=1.0, n_playout=1000):
        self.game = game
        self.c_puct = c_puct
        self.n_playout = n_playout

    def playout(self, node):
        current_game = copy.deepcopy(self.game)
        while not current_game.check_win(1) and not current_game.check_win(2):
            action = self.select_action(node)
            current_game.place_piece(*action)
            node = node.children[action]
        return self.get_reward(current_game)

    def select_action(self, node):
        max_value = -float('inf')
        best_action = None
        for action, child in node.children.items():
            value = child.get_value(self.c_puct)
            if value > max_value:
                max_value = value
                best_action = action
        return best_action

    def get_reward(self, game):
        if game.check_win(1):
            return 1.0
        elif game.check_win(2):
            return -1.0
        else:
            return 0.0

    def search(self, root):
        for n in range(self.n_playout):
            node = root
            while not node.is_leaf():
                action = self.select_action(node)
                node = node.children[action]
            node.add_child(random.choice(self.game.get_legal_actions()))
            reward = self.playout(node)
            while node is not None:
                node.update(reward)
                node = node.parent
        best_action = None
        best_value = -float('inf')
        for action, child in root.children.items():
            if child.q_value > best_value:
                best_value = child.q_value
                best_action = action
        return best_action