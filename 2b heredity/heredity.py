import csv
import itertools
import sys
from functools import reduce
import operator

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    def individual_probability(person):
        def num_genes(pers):  # ::person -> number of genes
            return (
                2 if pers in two_genes else
                1 if pers in one_gene else
                0
            )

        def p_gene_from_parent(parent):  # ::parent -> P(get gene from parent)
            n = num_genes(parent)
            p_mut = PROBS["mutation"]
            return (
                1 - p_mut if n == 2 else
                0.5 * (1 - p_mut) + 0.5 * p_mut if n == 1 else
                p_mut
            )

        def Not(p): return 1 - p

        mother = people[person]["mother"]
        father = people[person]["father"]
        n_genes = num_genes(person)
        print(person, n_genes, "genes")

        # early return if no parent data
        if mother is None:
            assert father is None
            return_value = PROBS["gene"][n_genes] * PROBS["trait"][n_genes][person in have_trait]
            print(person, return_value)
            return return_value

        p_from_mom = p_gene_from_parent(mother)
        p_from_dad = p_gene_from_parent(father)


        gene_probability = (
            p_from_mom * p_from_dad
            if n_genes == 2 else
            Not(p_from_mom) * p_from_dad + p_from_mom * Not(p_from_dad)
            if n_genes == 1 else
            Not(p_from_mom) * Not(p_from_dad)
        )

        trait_probability = (
            PROBS["trait"][n_genes][person in have_trait]
        )

        print(person, gene_probability, "*", trait_probability, "=", gene_probability * trait_probability)
        return gene_probability * trait_probability

    return reduce(
        operator.mul,  # multiply each individual probability
        map(
            individual_probability,  # compute individual probabily
            people
        )
    )


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
