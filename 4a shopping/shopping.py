import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    int_fields = set(
        "Administrative, Informational, ProductRelated, OperatingSystems, Browser, Region, TrafficType".split(", "))

    float_fields = set(
        "Administrative_Duration, Informational_Duration, ProductRelated_Duration, BounceRates, ExitRates, PageValues, SpecialDay".split(", "))

    bool_fields = set(("Weekend", "Revenue"))

    # ensure that sets are pairwise disjoint
    sets = [int_fields, float_fields, bool_fields]
    assert len(set.union(*sets)) == sum(map(len, sets))

    month_names = "Jan Feb Mar Apr May June Jul Aug Sep Oct Nov Dec".split()
    month_mappings = dict(zip(month_names, range(12)))

    def month_transform(month):
        return month_mappings[month]

    def visitor_transform(visitor):
        return 1 if visitor == "Returning_Visitor" else 0

    def bool_transform(bool_string):
        if bool_string == "FALSE":
            return 0
        if bool_string == "TRUE":
            return 1
        raise Exception(f"Invalid value {repr(bool_string)} for bool_string.")

    def invalid_transform(_):
        raise Exception(f"Field name {repr(_)} is not handled.")

    # To produce list of transformation needed for each field
    def field_transforms(field_names):
        return list(map(
            lambda field:
                int if field in int_fields else
                float if field in float_fields else
                month_transform if field == "Month" else
                visitor_transform if field == "VisitorType" else
                bool_transform if field in bool_fields else
                invalid_transform,
            field_names))

    evidence = []
    labels = []

    with open("shopping.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)

        field_names = next(reader)  # extract field names from first row

        # list of transformation needed for each field
        field_transforms_ = field_transforms(field_names)

        # # debug
        # for _ in zip(field_names,field_transforms_):
        #     print(_)

        for row in reader:
            transformed_row = list(map(
                lambda field, transform: transform(field),
                row,
                field_transforms_
            ))

            evidence.append(transformed_row[:-1])
            labels.append(transformed_row[-1])

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    
    return neigh.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # format: <label>_<predict>
    true_true = 0
    true_false = 0
    false_true = 0
    false_false = 0

    for label, predict in zip(labels, predictions):
        if label == 1:
            if predict == 1:
                true_true += 1
            else:
                true_false += 1
        else:
            if predict == 1:
                false_true += 1
            else:
                false_false += 1

    sensitivity = true_true / (true_true + true_false)
    specificity = false_false / (false_true + false_false)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
