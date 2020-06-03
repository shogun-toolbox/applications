import shogun as sg

import numpy as np

slope0 = 4.7
slope1 = 2
slope2 = -1

x_train = np.random.rand(3, 700) * 10
y_train = slope0 * (x_train[0]) + slope1 * (x_train[1]) + slope2 * (
    x_train[2]) + np.random.randn(700) * 5 + 5
y_true = slope0 * (x_train[0]) + slope1 * (x_train[1]) + slope2 * (
    x_train[2]) + 5
x_test = np.vstack((np.vstack(
        (np.linspace(0, 10, 300), np.random.rand(300) * 10)),
                    np.random.rand(300) * 10))
y_test = slope0 * (x_test[0]) + slope1 * (x_test[1]) + slope2 * (x_test[2]) + 5

features_train = sg.create_features(x_train)
features_test = sg.create_features(x_test)
labels_train = sg.create_labels(y_train)
labels_test = sg.create_labels(y_test)

lrr = sg.create_machine("LinearRidgeRegression", tau=0.001,
                        labels=labels_train)
lrr.train(features_train)
labels_predict = lrr.apply(features_test)

b = lrr.get("bias")
w = lrr.get("w")

eva = sg.create_evaluation("MeanSquaredError")
mse = eva.evaluate(labels_predict, labels_test)
output = labels_predict.get("labels")

print('Shogun Weights:')
print(w)
print('Shogun Bias:')
print(b)

sg_storage = sg.DynamicObjectArray()
sg_storage.append_element_real(b, "b")
sg_storage.append_element_real_vector(w, "w")
sg_storage.append_element_real(mse, "mse")
sg_storage.append_element_real_vector(output, "output")
sg_serializer = sg.JsonSerializer()
sg.serialize("linear_ridge_regression.dat", sg_storage, sg_serializer)
