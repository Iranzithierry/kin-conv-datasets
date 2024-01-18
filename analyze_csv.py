
# /*
# * Copyright (c) 2024 IRANZI Dev
# * All rights reserved.
# * Conversations used in this project are licensed under the private property of IRANZI Dev and other contributors.
# */


import pandas as pd

df = pd.read_csv("data.csv")

request_counts = df['Request'].value_counts(sort=True)

top_requests = request_counts.head(10)
print("\nTop Used Requests:")
print(top_requests)
