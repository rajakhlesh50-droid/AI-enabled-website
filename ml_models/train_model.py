import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

data = {
    "marks": [40, 50, 60, 70, 80, 90],
    "admission": [0, 0, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[["marks"]]
y = df["admission"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression()
model.fit(X_train, y_train)

pickle.dump(model, open("../backend/model.pkl", "wb"))

print("Model trained successfully!")