from search import Problem, breadth_first_tree_search, uniform_cost_search

class MissionariesCannibals(Problem):
    def __init__(self, M, C, boat_capacity):
        """
        M: total missionaries
        C: total cannibals
        boat_capacity: maximum number of people in the boat
        """
        self.M = M
        self.C = C
        self.boat_capacity = boat_capacity
        self.expanded = 0     # count of node expansions
        initial = (M, C, 1)   # all people and the boat start on the wrong side
        goal = (0, 0, 0)      # goal: no one on the wrong side, boat on the right
        super().__init__(initial, goal)

    def actions(self, state):
        """
        Returns a list of possible moves.
        A move is represented as a tuple (i, j) where
          - i is the number of missionaries to move,
          - j is the number of cannibals to move.
        """
        # Count a node expansion.
        self.expanded += 1

        m, c, b = state
        possible_actions = []

        if b == 1:
            # Boat is on the wrong side: choose people from that side.
            for i in range(0, self.boat_capacity + 1):
                for j in range(0, self.boat_capacity + 1):
                    if 1 <= i + j <= self.boat_capacity:
                        # If any missionary is on board, they must not be outnumbered by cannibals.
                        if i > 0 and i < j:
                            continue
                        # Cannot take more people than are present.
                        if i <= m and j <= c:
                            new_state = (m - i, c - j, 0)
                            if self.is_valid_state(new_state):
                                possible_actions.append((i, j))
        else:
            # Boat is on the right side: choose people from that side.
            right_m = self.M - m
            right_c = self.C - c
            for i in range(0, self.boat_capacity + 1):
                for j in range(0, self.boat_capacity + 1):
                    if 1 <= i + j <= self.boat_capacity:
                        if i > 0 and i < j:
                            continue
                        if i <= right_m and j <= right_c:
                            new_state = (m + i, c + j, 1)
                            if self.is_valid_state(new_state):
                                possible_actions.append((i, j))
        return possible_actions

    def result(self, state, action):
        """
        Returns the new state after applying action to state.
        """
        m, c, b = state
        i, j = action
        if b == 1:
            # Boat goes from wrong to right.
            return (m - i, c - j, 0)
        else:
            # Boat goes from right to wrong.
            return (m + i, c + j, 1)

    def goal_test(self, state):
        """
        The goal is reached when there are no missionaries or cannibals
        on the wrong side (and the boat is on the right).
        """
        return state == self.goal

    def is_valid_state(self, state):
        """
        Checks that the state is within bounds and that on both banks
        the missionaries are not outnumbered by cannibals (if any missionary is present).
        """
        m, c, b = state
        # Check that numbers are within the total counts.
        if m < 0 or c < 0 or m > self.M or c > self.C:
            return False

        # Check the wrong side.
        if m > 0 and m < c:
            return False

        # Check the other (right) side.
        rm = self.M - m
        rc = self.C - c
        if rm > 0 and rm < rc:
            return False

        return True


def main():
    # For the problem, we use 4 missionaries, 4 cannibals, boat capacity 3.
    problem = MissionariesCannibals(4, 4, 3)

    # Use BFS from AIMA's search module.
    solution = breadth_first_tree_search(problem)

    if solution:
        # The length of the path (including the initial state) is given by len(solution.path())
        print("Number of nodes expanded:", problem.expanded)
        print("Length of optimal path:", len(solution.path()))
        print("\nThe optimal path (each state is in the form (missionaries, cannibals, boat)): ")
        for node in solution.path():
            print(node.state)
    else:
        print("No solution found.")

    # For the problem, we use 6 missionaries, 6 cannibals, boat capacity 4.
    problem = MissionariesCannibals(6, 6, 4)

    # Use UCS from AIMA's search module.
    solution = uniform_cost_search(problem)

    if solution:
        # The length of the path (including the initial state) is given by len(solution.path())
        print("Number of nodes expanded:", problem.expanded)
        print("Length of optimal path:", len(solution.path()))
        print("\nThe optimal path (each state is in the form (missionaries, cannibals, boat)): ")
        for node in solution.path():
            print(node.state)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()