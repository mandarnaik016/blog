---
layout: post
title: Machine Learning - Incidents Similarity Index
subtitle: Pattern Recognition On Historical Incident 
cover-img: /assets/img/aiml/aiml.jpg
thumbnail-img: ""
tags: [artificial intelligence, machine learning, security]
---

## INTRODUCTION

Hello, in this post, we will use machine learning concepts to identify patterns across ingested incidents, enabling better correlation and helping determine appropriate actions based on historical responses.

Building on the previous article, [Predicting Cyber Attacks][predict], where we used a boosting algorithm i.e. [XGBoost][xgboost] to predict whether new incidents are _malicious_ or _benign_ based on historical labels.

Using the same dataset, we can go a step further by adding similarity indexing alongside our predictions. This helps us find similar incidents from the past, revisit the actions taken, and connect related incidents to gain better insights.

## SIMILARITY INDEXING

We install and import required libraries,

```python
%pip install pandas numpy scikit-learn chromadb 

import pandas as pd
import chromadb

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
```

Usage:

1. _Pandas_: Load and manipulate the dataset.
2. _ChromaDB_: Store vector embeddings and perform similarity searches.
3. _ColumnTransformer_: Apply preprocessing steps to numerical and categorical features.
4. _StandardScaler_: Standardize numerical features so they are on a comparable scale.
5. _OneHotEncoder_: Convert categorical features into numerical representations.
6. _SimpleImputer_: Handle missing values in the dataset.
7. _Pipeline_: Combine preprocessing steps into a reusable workflow.

The data can now be loaded and shown,

```python
df = pd.read_csv("cybersecurity_intrusion_data.csv")
df.head()
```

![Load dataset][load-dataset]

We clean the dataset by removing unnecessary columns like `session_id` and `attack_detected` since they are not needed for similarity indexing. This helps us focus on the actual incident details when comparing similar events.

{: .box-note}
**NOTE:** Similar incidents don't necessarily mean they have the same attack outcome. It only reflects how closely their features match.

```python
features = df.drop(columns=["session_id","attack_detected"])
features.head()
```

Next, we separate numerical and categorical columns because the data needs to be converted into numerical vectors before it can be stored in ChromaDB.

```python
numerical_columns = features.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_columns = features.select_dtypes(
    exclude=["number"]
).columns.tolist()
```

![Identified columns][identified-columns]

We create two separate pipelines:
1. _Numerical pipeline_: Fills missing values using the **median** and standardizes the numerical data so that features with larger values don't dominate the comparison.
2. _Categorical pipeline_: Fills missing values using the **most frequently occurring value** and converts categories into numerical representations using OneHotEncoder.

```python
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    ))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numerical_columns),
    ("categorical", categorical_pipeline, categorical_columns)
])

vectors = preprocessor.fit_transform(features)
```

Finally, `fit_transform()` processes the dataset and converts each incident into a numerical vector

We initialize a ChromaDB client to store our vectors locally. Then, we create an `incidents` collection and configure it to use cosine distance for comparing similar incidents.

```python
client = chromadb.PersistentClient(
    path="./incident_chromadb"
)

collection = client.get_or_create_collection(
    name="incidents",
    metadata={"hnsw:space": "cosine"}
)

print("Collection created!.")
```

Finally, we store the processed vectors in the collection in batches of 5,000 to handle large datasets efficiently.

```python
expected_count = len(vectors)
existing_count = collection.count()
if existing_count == 0:
    batch_size = 5000
    for start in range(0, expected_count, batch_size):
        end = min(start + batch_size, expected_count)
        collection.add(
            ids=[str(i + 1) for i in range(start, end)],
            embeddings=vectors[start:end].tolist(),
            documents=df["session_id"].iloc[start:end].tolist()
        )
        print(f"Inserted {end}/{expected_count}")
    print("Insertion completed.")
else:
    print("Collection already contains data. Skipping insertion.")
print("Total records:", collection.count())
```

<br>

## RESULTS

**Sample 1**

For the sample event below, our earlier model predicted it as not an attack, with a probability of 0.24.

```python
test_incident = pd.DataFrame([{
    "network_packet_size": 420,
    "protocol_type": "UDP",
    "login_attempts": 3,
    "session_duration": 128,
    "encryption_used": "AES",
    "ip_reputation_score": 0.4,
    "failed_logins": 1,
    "browser_type": "Chrome",
    "unusual_time_access": 0
}])
```

The search returns the following results along with similarity (%):

![Result - sample 1][result-1]

The IDs and their corresponding column values:

| session_id | network_packet_size | protocol_type | login_attempts | session_duration   | encryption_used | ip_reputation_score | failed_logins | browser_type | unusual_time_access | attack_detected |
| ---------- | ------------------- | ------------- | -------------- | ------------------ | --------------- | ------------------- | ------------- | ------------ | ------------------- | --------------- |
| SID_05574  | 425                 | UDP           | 3              | 324.7386353725522  | AES             | 0.38357979139897275 | 1             | Chrome       | 0                   | 0               |
| SID_03910  | 352                 | UDP           | 3              | 92.41636861485787  | None            | 0.3780615505075108  | 1             | Chrome       | 0                   | 0               |
| SID_08375  | 463                 | UDP           | 3              | 90.047313613045    | AES             | 0.4511062131712881  | 1             | Chrome       | 0                   | 0               |
| SID_00089  | 394                 | UDP           | 4              | 190.77965331945086 | AES             | 0.38401499470902695 | 1             | Chrome       | 0                   | 1               |
| SID_02003  | 341                 | UDP           | 3              | 223.033911968344   | AES             | 0.3268841695105474  | 1             | Chrome       | 0                   | 0               |

Except for one event, the other similar incidents were not labelled as attacks.

**Sample 2**

For the sample event below, our earlier model predicted it as an attack, with a probability of 0.99.

```python
test_incident = pd.DataFrame([{
    "network_packet_size": 512,
    "protocol_type": "TCP",
    "login_attempts": 5,
    "session_duration": 256,
    "encryption_used": "DES",
    "ip_reputation_score": 0.6,
    "failed_logins": 2,
    "browser_type": "Unknown",
    "unusual_time_access": 1
}])
```

The search returns the following results along with similarity (%):

![Result - sample 2][result-2]

The IDs and their corresponding column values:

| session_id | network_packet_size | protocol_type | login_attempts | session_duration   | encryption_used | ip_reputation_score | failed_logins | browser_type | unusual_time_access | attack_detected |
| ---------- | ------------------- | ------------- | -------------- | ------------------ | --------------- | ------------------- | ------------- | ------------ | ------------------- | --------------- |
| SID_02927  | 476                 | TCP           | 5              | 523.4189303855626  | DES             | 0.5628344133277222  | 2             | Chrome       | 1                   | 1               |
| SID_01792  | 523                 | TCP           | 6              | 161.37544455931692 | DES             | 0.5551873243606777  | 2             | Chrome       | 1                   | 0               |
| SID_09134  | 554                 | TCP           | 3              | 3.4942529874545167 | DES             | 0.6608198256665023  | 2             | Safari       | 1                   | 1               |
| SID_01065  | 427                 | TCP           | 5              | 243.5440072188964  | AES             | 0.559804549671735   | 1             | Unknown      | 1                   | 1               |
| SID_09015  | 457                 | TCP           | 7              | 426.6712109096449  | DES             | 0.4064071216407788  | 1             | Unknown      | 1                   | 1               |

Except for one event, the other similar incidents were labelled as attacks.

## CONCLUSION

The similarity search was able to find historical incidents that closely matched our test event. Except for one incident, the remaining results aligned with the expected classification. This gives us a useful starting point to look back at previous incidents and understand how they were handled.

As we add more historical incidents to the dataset, we can make these searches more useful and can improve the insights.

Source code: [Incidents Similarity Index][chromadb]

Thank you. We meet next time to make security better. Until then, Sayonara!.


[predict]: /2026-02-22-machine-learning-predicting-cyber-attacks/
[xgboost]: https://xgboost.ai/
[chromadb]: ../assets/datastore/incidents-similarity-index.ipynb
[load-dataset]: ../assets/img/aiml/similarity-index/load-dataset.png
[identified-columns]: ../assets/img/aiml/similarity-index/identified-columns.png
[result-1]: ../assets/img/aiml/similarity-index/result-1.png
[result-2]: ../assets/img/aiml/similarity-index/result-2.png