import joblib

def load_model():
    return joblib.load("trained_model/model.pkl")

def predict(model, data):
    return model.predict([data])[0]