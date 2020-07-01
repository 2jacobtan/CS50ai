https://cs50.harvard.edu/ai/2020/projects/5/traffic/

https://vimeo.com/434393422

I tried lowering dropout from 0.5 to 0.2: accuracy improved much.

Adding another hidden dense layer did not affect accuracy.

Doubling nodes from 128 to 256 on hidden dense layer, did not affect accuracy.

Doubling convolution filters from 32 to 64 did not affect accuracy.

Adding another set of convolution + pooling layers improved accuracy a few %.

Removing one pooling layer from the setup in previous line, improved accuracy by 2% on training set, but not on test set. Looks like a bit of overfitting.
