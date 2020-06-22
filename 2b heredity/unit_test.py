import heredity


def test(function_name, test_arguments, expected = None):
    function = getattr(heredity, function_name)
    result = function(*test_arguments)
    print(f"___{function_name}")
    print(result)
    if expected is not None:
        print("* pass" if result == expected else "! fail")
    print()


people = heredity.load_data("data/family0.csv")
test(
    "joint_probability",
    [
        people,
        {"Harry"},
        {"James"},
        {"James"}
    ],
)