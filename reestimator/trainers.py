# IMPLEMENT THE MAIN CLASS TO EXECUTE OUR GLOBAL PIPELINE(S)
"""
The Trainer class is the main class. It should have:

- an __init__ method called when the class is instanciated
- a set_pipeline method that builds the pipeline
- a run method that trains the pipeline
- an evaluate method evaluating the model
"""

class Trainer:

    def __init__(self, df):
        self.df=df

    def temp_test():
        return "OK structures on going"

    def get_data():
        """
        Function used in order to get the training data (or a portion of it)
        from Cloud Storage
        """
        pass

    def train_model(self):

        pass

    def preprocess(df):
        """
        Function that pre-processes the data
        """
        pass

    def train_model(X_train, y_train):
        """
        Function that trains the model
        """
        pass

    def save_model(reg):
        """
        Method that saves the model into a .joblib file
        and uploads it on Google Storage /models folder
        """
        pass
