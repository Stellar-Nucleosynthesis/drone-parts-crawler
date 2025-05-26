import pickle

def save_to_pickle(obj, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)

def load_from_pickle(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)
