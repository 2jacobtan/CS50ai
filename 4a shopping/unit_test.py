from shopping import * 

evidence, labels = load_data("shopping.csv")
zipped = zip(evidence,labels)

for i in range(4):
    e, l = next(zipped)
    print(e,l)
    if i == 0:
        assert e == [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0]
        assert l == 0
        print("* Test passed.")
