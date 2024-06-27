# myapp/predictor.py

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import KNeighborsClassifier

class SkillPredictor:
    def __init__(self, dataset_path='bookapp/course.csv'):
        self.dataset_path = dataset_path
        self.load_data()
        self.prepare_model()

    def load_data(self):
        self.df = pd.read_csv(self.dataset_path, encoding='latin-1', usecols=['Category', 'Sub-Category', 'Skills'],
                              dtype={'Category': 'str', 'Sub-Category': 'str', 'Skills': 'str'})
        self.df.dropna(inplace=True)
        self.df['Skills'] = self.df['Skills'].str.split(',').apply(lambda x: ','.join(x[:3]))

    def prepare_model(self):
        self.mlb = MultiLabelBinarizer()
        skills_encoded = pd.DataFrame(self.mlb.fit_transform(self.df['Skills'].str.split(',')),
                                      columns=self.mlb.classes_)
        self.df_encoded = pd.concat([self.df[['Category', 'Sub-Category']], skills_encoded], axis=1)

        X = self.df_encoded.drop(['Category', 'Sub-Category'], axis=1)
        y = self.df_encoded[['Category', 'Sub-Category']]

        self.knn_model = KNeighborsClassifier(n_neighbors=5)
        self.knn_model.fit(X, y)

    def predict_category(self, input_skills):
        input_skills = input_skills.split(',')
        input_skills_encoded = self.mlb.transform([input_skills])
        predicted_category_subcategory = self.knn_model.predict(input_skills_encoded)
        return predicted_category_subcategory[0]

    def predict_category_from_skills(self,skill1,skill2,skill3):
        input_skills = [skill1, skill2, skill3]
    
        
        try:
            input_skills_encoded = self.mlb.transform([input_skills])
        except ValueError as e:
            return "Error:", e

        predicted_category_subcategory = self.knn_model.predict(input_skills_encoded)
        result = {"Category": predicted_category_subcategory[0][0]}
        if predicted_category_subcategory.shape[1] > 1:
            result["Subcategory"] = predicted_category_subcategory[0][1]
        else:
            result["Subcategory"] = "Subcategory prediction not available."

        return result

