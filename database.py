import pickle

# Enum pickles
USERS = "users.p"
CHATHISTORY = "chat.p"


def save(obj, file):
    pickle.dump(obj, open(file, "wb"))


def load(file):
    return pickle.load(open(file, "rb"))