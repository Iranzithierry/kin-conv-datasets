import pandas as pd

df = pd.read_csv("data.csv")

request_counts = df['Request'].value_counts(sort=True)

top_requests = request_counts.head(10)
print("\nTop Used Requests:")
print(top_requests)
