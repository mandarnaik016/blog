---
layout: post
title: Machine Learning - Predicting Cyber Attacks
subtitle: History Leads Future!
cover-img: /assets/img/aiml/aiml.jpg
thumbnail-img: ""
tags: [machine learning, security]
---

Hello, in this post, we will use machine learning to predict whether an event is attack or not.

## Model Creation

We will be using a dataset readily available on [Kaggle](https://www.kaggle.com/datasets/dnkumars/cybersecurity-intrusion-detection-dataset) (PSSS: The About section provides good documentation about the dataset's content).

The dataset contains the following columns,
```
session_id,network_packet_size,protocol_type,login_attempts,session_duration,encryption_used,ip_reputation_score,failed_logins,browser_type,unusual_time_access,attack_detected
```

Since the dataset contains target data (labelled data), i.e., **attack_detected**, we proceed with supervised learning.

We import the following libraries,

{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/imports.png"
    img_datasrc="../assets/img/aiml/predict-attack/imports.png"
    img_caption="Figure 1: Imports"
    img_alt="Imports"
%}

1. Pandas: To read CSV and organize data.
2. LabelEncoder: To convert textual data to numbers for the model to understand, i.e., Chrome => 0 for *column browser_type*.
3. *train_test_split*: To split data into training and testing parts.
4. xgboost: A machine learning algorithm to find patterns and predict.
5. *classification_report* and *confusion_matrix*: To determine accuracy.

The data can now be loaded and shown,
{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/read_data.png"
    img_datasrc="../assets/img/aiml/predict-attack/read_data.png"
    img_caption="Figure 2: Read data"
    img_alt="Read data"
%}


Dropping the column *session_id* since it had no significance in learning. We converted the textual data (*protocol_type*, *encryption_used*, and *browser_type*) into integers for the algorithm to understand.
{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/filter_and_categorize.png"
    img_datasrc="../assets/img/aiml/predict-attack/filter_and_categorize.png"
    img_caption="Figure 3: Filter and categorize"
    img_alt="Filter and categorize"
%}

We split the data into training and testing using *train_test_split*, then create an XGBoost classifier. At last, we start the learning process for the features (*X_train*) and the correct answer (*y_train*).
{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/train_and_create_model.png"
    img_datasrc="../assets/img/aiml/predict-attack/train_and_create_model.png"
    img_caption="Figure 4: Train and create model"
    img_alt="Train and create model"
%}

To calculate accuracy, we use the test data (*X_test*) for making a prediction (*y_pred*) from the trained model and then compare this with the defined result (*y_test*) within the dataset.
{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/calculate_accuracy.png"
    img_datasrc="../assets/img/aiml/predict-attack/calculate_accuracy.png"
    img_caption="Figure 5: Calculate accuracy"
    img_alt="Calculate accuracy"
%}

The diagram below helps us to understand the accuracy in a better way.
{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/matrix.png"
    img_datasrc="../assets/img/aiml/predict-attack/matrix.png"
    img_caption="Figure 6: Matrix"
    img_alt="Matrix"
%}

1. The model was good at categorizing events that were benign, with the sole exception for two events.
2. On another hand, the model correctly categorized 637 events as attacks (Which were attack) and failed to detect 216 events as attack.


## Model Testing

Let's test the model on new events,

### Sample 1

For an input sample event as below,
{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/sample_1.png"
    img_datasrc="../assets/img/aiml/predict-attack/sample_1.png"
    img_caption="Figure 7: Sample 1"
    img_alt="Sample 1"
%}

The model makes the following prediction,
{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/sample_1_prediction.png"
    img_datasrc="../assets/img/aiml/predict-attack/sample_1_prediction.png"
    img_caption="Figure 8: Sample 1 Prediction"
    img_alt="Sample 1 Prediction"
%}

Since the input features were comparatively lower (Benign, With reference to the dataset), it was predicted as **No Attack**.


### Sample 2

We create another sample event with similarities to an event of an attack,

{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/sample_2.png"
    img_datasrc="../assets/img/aiml/predict-attack/sample_2.png"
    img_caption="Figure 9: Sample 2"
    img_alt="Sample 2"
%}

The model makes the following prediction,
{%  include lazyimg.html
    img_src="../assets/img/aiml/predict-attack/lowly/sample_2_prediction.png"
    img_datasrc="../assets/img/aiml/predict-attack/sample_2_prediction.png"
    img_caption="Figure 10: Sample 2 Prediction"
    img_alt="Sample 2 Prediction"
%}


The input features `browser_type` being Unknown, `ip_reputation_score` was comparatively high, etc. lead to the prediction as **Attack**.


## Conclusion

The model's overall accuracy is **Good**, to increase the accuracy, we can increase the size of the dataset where events are correctly categorized, recursively, and again train the model on those new data events.

Source code: [Predicting Cyber Attacks](https://drive.google.com/file/d/1U0RTd-BNbToI-42YVEK1vBH1cKHz9Esx/view?usp=sharing)

Thank you. We meet next time to make security better. Until then, Sayonara!.