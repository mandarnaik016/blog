---
layout: post
title: Decision Model - Email Threat Classification
subtitle: Fast Enough To Be Worthy ;)
cover-img: /assets/img/aiml/aiml.jpg
thumbnail-img: ""
tags: [artificial intelligence, machine learning, security]
---

## INTRODUCTION

Hello folks, long time no see! We’re back here another day, exploring AI.

In a traditional SOC, a significant portion of critical alerts come from phishing emails. Almost every employee has access to a mailbox, and tricking a human is often easier than tricking a machine.

Most organizations have a _Report Phishing_ feature that allows employees to report suspicious emails. A copy of the reported email is forwarded to a designated mailbox, which can then be ingested into a SIEM/SOAR solution for further processing by the SOC team.

An email contains several data points that can help determine whether it is legitimate, spam, or phishing.

Some of these parameters are visible to the naked eye:
- Sender
- Reply-To
- Subjecta
- Email body
- Embedded URLs

Others are less obvious but equally important:
- SPF
- DKIM
- DMARC
- Email headers
- Sender infrastructure information

Combining these data points and enriching them can provide valuable insights to SOC analysts. However, processing all this information, presenting the findings, and reaching a conclusion can be **computationally expensive** and still require manual intervention.

## AI-IN-LOOP

The instinct here would be to adopt Generative AI and pass all these data points as a payload to the model. However, this approach comes with a few challenges:

- _Token consumption_: Passing the entire email, including headers and other metadata, increases token usage.
- _Processing time_: More input data and complex reasoning can increase response time.
- _Output overhead_: Generative AI typically produces detailed responses, which then need to be parsed and interpreted.
- _Additional processing_: Extracting meaningful insights and converting them into actionable decisions introduces another layer of complexity.

Do we really need a detailed explanation every time we want to classify an email?

This is where a **single-decision model** comes into play.

Unlike Generative AI, which typically responds with a broader explanation, what if we could get an answer in just YES or NO? Imagine asking a coworker, "Would you like some tea?" The expected answer is either YES or, probably, a YES (come on, who refuses tea?).

On the other hand, if they start replying with something like, "The powder from the Assam valley, the aroma of Darjeeling…" you should probably consider changing coworkers. Jokes aside, the idea is simple.

What if we provide a prompt containing the sender, subject, and email body, and ask the model to identify a specific intent and respond with YES or NO, along with a confidence score? Instead of generating paragraphs of explanations, the model focuses on one classification task.

A smaller model with a well-defined objective can offer:

- Lower resource consumption.
- Shorter response times.
- Simplified output parsing.
- Easier integration with other applications.
- More predictable responses.

The idea is to keep the model focused on making a decision rather than generating an entire analysis report.

## IMPLEMENTATION

For the implementation, I used **Laya**, a lightweight model with an approximate footprint of ~900 MB, running locally through Ollama.

The Python pipeline handles email parsing, text preprocessing, prompt construction, and model inference through the following steps:

- _Email Parsing_: The input .eml file is processed to extract relevant attributes, including Sender, Reply-To, Subject, and Email Body.
- _URL Extraction_: URLs embedded in the email body are extracted separately or removed from the text to reduce unnecessary input and keep the prompt size manageable.
- _Text Preprocessing_: NLTK is used to tokenize the email body and remove common stopwords and unnecessary characters, reducing noise in the input.
- _Prompt Construction and Inference_: The extracted attributes and preprocessed body are assembled into a structured prompt and passed to Laya through the local Ollama instance for classification.
- _Result Presentation_: The model's responses are processed to obtain separate spam and phishing confidence scores, which are then displayed alongside the email subject and processing time.

Source code: [Mail Guardian](https://github.com/mandarnaik016/mail-guardian)
