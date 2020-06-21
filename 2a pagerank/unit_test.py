import pagerank


def test(function_name, test_arguments, expected = None):
    function = getattr(pagerank, function_name)
    result = function(*test_arguments)
    print(f"___{function_name}")
    print(result)
    if expected is not None:
        print("* pass" if result == expected else "! fail")
    print()

CORPUS = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

transition_model_test = [
    CORPUS,
    "1.html",
    0.85
]
transition_model_expected = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}
test("transition_model", transition_model_test, transition_model_expected)

test("sample_pagerank", [CORPUS, pagerank.DAMPING, pagerank.SAMPLES])

test("iterate_pagerank", [CORPUS, pagerank.DAMPING])