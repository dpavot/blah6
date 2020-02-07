import pandas
import sklearn.model_selection
import sklearn.preprocessing
from numpy import unique
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers.merge import concatenate
from keras.utils import plot_model

def load_dataset(filename):
	data = pandas.read_csv(filename, delimiter = '\t', header = 0)
	dataset = data.values
	X = dataset[:, :-1]
	y = dataset[:,-1]
	X = X.astype(str)
	y = y.reshape((len(y), 1))
	return X, y

def prepare_inputs(X_train, X_test):
	X_train_enc, X_test_enc = list(), list()

	for i in range(X_train.shape[1]):
		le = sklearn.preprocessing.LabelEncoder()
		le.fit(X_train[:, i])
		# encode
		train_enc = le.transform(X_train[:, i])
		test_enc = le.fit_transform(X_test[:, i])  # not well
		# store
		X_train_enc.append(train_enc)
		X_test_enc.append(test_enc)
	return X_train_enc, X_test_enc

def prepare_targets(y_train, y_test):
	le = sklearn.preprocessing.LabelEncoder()
	le.fit(y_train)
	y_train_enc = le.transform(y_train)
	y_test_enc = le.transform(y_test)
	return y_train_enc, y_test_enc

X, y = load_dataset('data/fnu_gold_standard.tsv')
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 0.30, random_state = 1)

print('Train', X_train.shape, y_train.shape)
print('Test', X_test.shape, y_test.shape)

X_train_enc, X_test_enc = prepare_inputs(X_train, X_test)
y_train_enc, y_test_enc = prepare_targets(y_train, y_test)

y_train_enc = y_train_enc.reshape((len(y_train_enc), 1, 1))
y_test_enc = y_test_enc.reshape((len(y_test_enc), 1, 1))

in_layers = list()
em_layers = list()
for i in range(len(X_train_enc)):

	n_labels = len(unique(X_train_enc[i]))
	in_layer = Input(shape=(1,))
	em_layer = Embedding(n_labels, 10)(in_layer)
	in_layers.append(in_layer)
	em_layers.append(em_layer)

merge = concatenate(em_layers)
dense = Dense(10, activation='relu', kernel_initializer='he_normal')(merge)
output = Dense(1, activation='sigmoid')(dense)
model = Model(inputs=in_layers, outputs=output)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
plot_model(model, show_shapes=True, to_file='embeddings.png')
model.fit(X_train_enc, y_train_enc, epochs=100, batch_size=16)#, verbose=2)

_, accuracy = model.evaluate(X_test_enc, y_test_enc)#, verbose=0)
print('Accuracy: %.2f' % (accuracy*100))