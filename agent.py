from mcts import MCTSTreeNode
import copy

class GobangAI:
    def __init__(self, game, mcts):
        self.game = game
        self.mcts = mcts

    def get_action(self, state):
        root = MCTSTreeNode(None, None)
        for n in range(self.mcts.n_playout):
            current_game = copy.deepcopy(self.game)
            node = root
            while not current_game.check_win(1) and not current_game.check_win(2):
                if not node.is_leaf():
                    action = self.mcts.select_action(node)
                    node = node.children[action]
                    current_game.place_piece(*action)
                else:
                    break
            if not node.is_leaf():
                continue
            reward = self.mcts.playout(node)
            while node is not None:
                node.update(reward)
                node = node.parent
        action = self.mcts.search(root)
        return action