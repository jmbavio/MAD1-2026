import kagglehub
import pandas as pd
# Download latest version
path = kagglehub.dataset_download("sehaj1104/student-mental-health-and-burnout-dataset")

df=pd.read_csv("student_mental_health_burnout.csv")

print("Path to dataset files:", path)
print("Dataset shape:", df.shape)
print("Dataset columns:", df.columns)