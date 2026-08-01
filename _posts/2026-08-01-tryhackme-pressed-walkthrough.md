---
layout: post
title: TryHackMe - Pressed Walkthrough
subtitle: A Smooth Operator
cover-img: /assets/img/analysis/analysis.jpeg
thumbnail-img: ""
tags: [analysis, security, network, tryhackme]
---

Hello, in this post, we will walk through a challenge [Pressed](https://tryhackme.com/room/pressedroom).

We are presented with a PCAP file and description as _packet capture (PCAP) was recorded during the incident, capturing the attacker's initial entry and subsequent actions. Your task is to analyse the traffic, identify how the attacker gained access, and uncover the sequence of malicious activity. Reconstruct the attack timeline and determine the final impact by finding the attacker's objective hidden within the captured data._

## Hunt Begins

Master Roshi said "Always start the PCAP analysis with Snort/Suricata, detecting events and furnishing alerts".

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/snort-alerts.png" img_datasrc="../assets/img/analysis/pressed/snort-alerts.png" img_caption="Figure 1: Snort alerts" img_alt="Snort alerts" %}
Let’s hypothesize that these IP(s) are involved in malicious activity i.e. 10[.]13[.]44[.]207 & 10[.]10[.]86[.]57.


To reduce noise, we check for endpoints having significant conversations.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/conversations-statistic.png" img_datasrc="../assets/img/analysis/pressed/conversations-statistic.png" img_caption="Figure 2: Conversations statistic" img_alt="Conversations statistic" %}
The earlier flagged IPs had the most packets to and fro.

We use zeek to get oversight of services used by both the IPs.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/application-services.png" img_datasrc="../assets/img/analysis/pressed/application-services.png" img_caption="Figure 3: Application services" img_alt="Application services" %}
After analysis, we didn’t find any successful login to POP service. Although SMTP service had a successful login.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/auth-smtp.png" img_datasrc="../assets/img/analysis/pressed/auth-smtp.png" img_caption="Figure 4: Auth smtp" img_alt="Auth smtp" %}
Down the flow, we find a mail with subject _Urgent_.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/suspicious-subject.png" img_datasrc="../assets/img/analysis/pressed/suspicious-subject.png" img_caption="Figure 5: Suspicious subject" img_alt="Suspicious subject" %}

When followed in stream, It had a content disposition with filename _sheet.ods_.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/artifact.png" img_datasrc="../assets/img/analysis/pressed/artifact.png" img_caption="Figure 6: Artifact" img_alt="Artifact" %}
I was able to open the _sheet.ods_ file using doc viewer. For some reason the file was empty but had **Macros**.

CyberChef flagged it’s file type as _ZIP_.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/artifact-filetype.png" img_datasrc="../assets/img/analysis/pressed/artifact-filetype.png" img_caption="Figure 7: Artifact filetype" img_alt="Artifact filetype" %}

I out smartly renamed the file from _.ods_ to _.zip_ and extracted the content.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/artifact-extracted.png" img_datasrc="../assets/img/analysis/pressed/artifact-extracted.png" img_caption="Figure 8: Artifact extracted" img_alt="Artifact extracted" %}
A subfolder contained file named _evil.xml_ that contained following,

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/answer1.png" img_datasrc="../assets/img/analysis/pressed/answer1.png" img_caption="Figure 9: Answer1" img_alt="Answer1" %}
The echo command displays the first answer of the room. Additionally, We can verify command that downloads _client.exe_ and executes.


## Connecting Dots

We dump the binary file and perform static analysis.

From the _main_ function we can interpret that it is making a connection to attacker machine on port 443.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/remote-connection.png" img_datasrc="../assets/img/analysis/pressed/remote-connection.png" img_caption="Figure 10: Remote connection" img_alt="Remote connection" %}
The binary encrypts and decrypts the data using AES while send and receiving.

We get the **IV** and **Key** from the decompiled source code.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/aes-key.png" img_datasrc="../assets/img/analysis/pressed/aes-key.png" img_caption="Figure 11: AES key" img_alt="AES key" %}
{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/aes-iv.png" img_datasrc="../assets/img/analysis/pressed/aes-iv.png" img_caption="Figure 12: AES IV" img_alt="AES IV" %}
We locate the TLS communication and corresponding payload.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/tls-payload.png" img_datasrc="../assets/img/analysis/pressed/tls-payload.png" img_caption="Figure 13: TLS payload" img_alt="TLS payload" %}
The exported payloads.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/exported-payloads.png" img_datasrc="../assets/img/analysis/pressed/exported-payloads.png" img_caption="Figure 14: Exported payloads" img_alt="Exported payloads" %}
We can decrypt all the payloads all at once using the earlier found key and IV.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/decrypted-payloads.png" img_datasrc="../assets/img/analysis/pressed/decrypted-payloads.png" img_caption="Figure 15: Decrypted payloads" img_alt="Decrypted payloads" %}
The decrypted data contains the second and third answer of the room.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/answer2-3.png" img_datasrc="../assets/img/analysis/pressed/answer2-3.png" img_caption="Figure 16: Answer2 3" img_alt="Answer2 3" %}

## The Reveal

We can concatenate all the answers and decode the base64 encoded flag.

{% include lazyimg.html img_src="../assets/img/analysis/pressed/lowly/flag.png" img_datasrc="../assets/img/analysis/pressed/flag.png" img_caption="Figure 17: Flag" img_alt="Flag" %}
