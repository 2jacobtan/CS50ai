from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


def Xor(left, right):  # A xor B <-> (A or B) and not(A and B)
    return And(
        Or(left, right),
        Not(And(left, right))
    )


# Puzzle 0
# A says "I am both a knight and a knave."
A_says0 = And(AKnight, AKnave) # logical content of A's speech
knowledge0 = And(
    # context: either a knight or a knave
    Xor(AKnight, AKnave), # A is either a Knight or a Knave

    # context: knight speaks truth, knave speaks lies
    Implication(AKnight, A_says0), # if AKnight, then A_says is true
    Implication(AKnave, Not(A_says0)) # if AKnave, then A_says is false
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
A_says1 = And(AKnave, BKnave) # logical content of A's speech
knowledge1 = And(
    # context: either a knight or a knave
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),

    # context: knight speaks truth, knave speaks lies
    Implication(AKnight, A_says1), # if AKnight, then A_says is true
    Implication(AKnave, Not(A_says1)) # if AKnave, then A_says is false
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
A_says2 = Or( # logical content of A's speech; Xor also works but goes beyond what A says.
    And(AKnight, BKnight),
    And(AKnave, BKnave),
)
B_says2 = Or( # logical content of B's speech; Xor also works but goes beyond what B says.
    And(AKnight, BKnave),
    And(AKnave, BKnight),
)
knowledge2 = And(
    # context: either a knight or a knave
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),

    # context: knight speaks truth, knave speaks lies
    Implication(AKnight, A_says2), # if AKnight, then A_says is true
    Implication(AKnave, Not(A_says2)), # if AKnave, then A_says is false    
    Implication(BKnight, B_says2), 
    Implication(BKnave, Not(B_says2))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
A_says3 = Xor(AKnight, AKnave) # Trivially true; obviously A is a knight.
B_says3a = And(  # logical content of B's first speech; obviously false; B is a knave
    Implication(AKnight, AKnave),
    Implication(AKnave, Not(AKnave))
)
B_says3b = CKnave  # logical content of B's second speech
C_says3 = AKnight  # logical content of C's speech
knowledge3 = And(
    # context: either a knight or a knave
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    Xor(CKnight, CKnave),

    # context: knight speaks truth, knave speaks lies
    Implication(AKnight, A_says3), # if AKnight, then A_says is true
    Implication(AKnave, Not(A_says3)), # if AKnave, then A_says is false    

    # Two sets, one for each time B speaks.
    Implication(BKnight, B_says3a), 
    Implication(BKnave, Not(B_says3a)),
    Implication(BKnight, B_says3b), 
    Implication(BKnave, Not(B_says3b)),

    Implication(CKnight, C_says3), 
    Implication(CKnave, Not(C_says3))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
