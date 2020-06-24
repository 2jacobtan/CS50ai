import sys
from collections import deque
import itertools

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, domain in self.domains.items():
            self.domains[variable] = {
                word for word in domain if len(word) == variable.length}

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return False

        # respective positions of overlap on each variable
        x_index, y_index = overlap

        y_chars = {word[y_index] for word in self.domains[y]}

        # filter out incompatible words from domain of x
        new_domain_x = {word for word in self.domains[x]
                        if word[x_index] in y_chars}

        is_revision_made = (
            True if len(new_domain_x) < len(self.domains[x])
            else False)

        self.domains[x] = new_domain_x

        return is_revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # use set to avoid requeueing duplicate arc
        if arcs is None:
            arcs = set(filter(
                lambda key: self.crossword.overlaps[key] is not None,
                self.crossword.overlaps
            ))
        else:
            arcs = set(arcs)

        arc_set = arcs.copy()  # keep arcs unmutated for later use
        arc_queue = deque(arc_set)

        # queue is used together with set

        def pop():
            arc = arc_queue.popleft()
            arc_set.remove(arc)
            return arc

        def extend(new_arcs, arc_set):  # ::set -> ()
            new_arcs -= arc_set  # exclude duplicate arcs
            arc_queue.extend(new_arcs)  # add new arcs to queue
            arc_set |= new_arcs  # add new arcs to set

        while arc_set:
            x, y = pop()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                extend(
                    set(filter(
                        lambda arc: arc[1] == x,
                        arcs
                    )) - {(y, x)},
                    arc_set
                )

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # uniqueness
        if not (len(set(assignment.values())) == len(assignment)):
            return False

        # correct length
        if not (all(map(
            lambda var_value: var_value[0].length == len(var_value[1]),
            assignment.items()
        ))):
            return False

        pairs = itertools.combinations(assignment,2)

        overlaps = {
            key: val
            for key, val in self.crossword.overlaps.items()
            if key in pairs
            and val is not None
        }

        # no conflict with neighbors
        for (v1, v2), (i1, i2) in overlaps.items():
            if assignment[v1][i1] != assignment[v2][i2]:
                return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # # replaced by better version below
        # overlaps = {
        #     (v1,v2): val
        #     for (v1,v2), val in self.crossword.overlaps.items()
        #     if v1 == var and v2 not in assignment
        #     and val is not None
        # }
        overlaps = {
            (var, v2): self.crossword.overlaps[var, v2]
            for v2 in self.crossword.variables - {var}
            if v2 not in assignment
            and self.crossword.overlaps[var, v2]
        }

        size_before_elimination = sum(
            len(self.domains[v2]) for (v1, v2) in overlaps
        )

        def sort_by(val):
            size_of_elimination = sum(
                sum(1 for word in self.domains[v2]
                    if word[i2] != val[i1]
                    )
                for (v1, v2), (i1, i2) in overlaps.items()
            )
            return size_of_elimination

        return list(sorted(self.domains[var], key=sort_by))

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables0 = self.crossword.variables - set(assignment)

        # minimum number of remaining values
        variables1 = [variables0.pop()]
        min_ = len(self.domains[variables1[0]])
        for var in variables0:
            length = len(self.domains[var])
            if length < min_:
                min_ = length
                variables1 = [var]
            elif length == min_:
                variables1.append(var)

        if len(variables1) == 1:
            return variables1[0]

        # highest degree
        return max(variables1, key=lambda var: sum(
            1 for (v1, v2), _ in self.crossword.overlaps.items()
            if v1 == var and _ is not None))

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
