---
layout: post
title: TryHackMe - Carnage Walkthrough
subtitle: Following The Trace....
cover-img: /assets/img/analysis/analysis.jpeg
thumbnail-img: ""
tags: [analysis, security, network, tryhackme]
---

Hello, in this post, we will walk through a challenge [Carnage](https://tryhackme.com/room/c2carnage).

**Scenario**

Eric Fischer from the Purchasing Department at Bartell Ltd has received an email from a known contact with a Word document attachment. Upon opening the document, he accidentally clicked on "Enable Content." The SOC Department immediately received an alert from the endpoint agent that Eric's workstation was making suspicious connections outbound. The pcap was retrieved from the network sensor and handed to you for analysis.

**Traffic Analysis Questions**

1\. What was the date and time for the first HTTP connection to the malicious IP?

We use the `http` query to filter the first HTTP connection.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-1.png" img_datasrc="../assets/img/analysis/carnage/answer-1.png" img_caption="Figure 1: Answer 1" img_alt="Answer 1" %}
Answer: **2021-09-24 16:44:38**

2\. What is the name of the zip file that was downloaded?

A wild search for `.zip` across IP packets led us to, 

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-2.png" img_datasrc="../assets/img/analysis/carnage/answer-2.png" img_caption="Figure 2: Answer 2" img_alt="Answer 2" %}
Answer: **documents.zip**

3\. What was the domain hosting the malicious zip file?

Packet information (From the 2nd answer) can reveal the server name.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-3.png" img_datasrc="../assets/img/analysis/carnage/answer-3.png" img_caption="Figure 3: Answer 3" img_alt="Answer 3" %}
Answer: **attirenepal[.]com**

4\. Without downloading the file, what is the name of the file in the zip file?

For this, we export the file from HTTP objects & view the data within the archive.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-4a.png" img_datasrc="../assets/img/analysis/carnage/answer-4a.png" img_caption="Figure 4: Answer 4a" img_alt="Answer 4a" %}
{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-4b.png" img_datasrc="../assets/img/analysis/carnage/answer-4b.png" img_caption="Figure 5: Answer 4b" img_alt="Answer 4b" %}
Answer: **chart-1530076591.xls**

5\. What is the name of the webserver of the malicious IP from which the zip file was downloaded?

Following the packet (From the 2nd answer) in the HTTP stream can provide server-side headers and responses.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-5.png" img_datasrc="../assets/img/analysis/carnage/answer-5.png" img_caption="Figure 6: Answer 5" img_alt="Answer 5" %}
Answer: **LiteSpeed**

6\. What is the version of the webserver from the previous question?

From the same HTTP stream, we get the version.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-6.png" img_datasrc="../assets/img/analysis/carnage/answer-6.png" img_caption="Figure 7: Answer 6" img_alt="Answer 6" %}
Answer: **PHP/7.2.34**

7\. Malicious files were downloaded to the victim host from multiple domains. What were the three domains involved with this activity?

We can filter the source IP as `10.9.23.102` and query the DNS requests.

The following domains were suspicious,

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-7a.png" img_datasrc="../assets/img/analysis/carnage/answer-7a.png" img_caption="Figure 8: Answer 7a" img_alt="Answer 7a" %}
{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-7b.png" img_datasrc="../assets/img/analysis/carnage/answer-7b.png" img_caption="Figure 9: Answer 7b" img_alt="Answer 7b" %}
{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-7c.png" img_datasrc="../assets/img/analysis/carnage/answer-7c.png" img_caption="Figure 10: Answer 7c" img_alt="Answer 7c" %}
Answer: **finejewels[.]com[.]au, thietbiagt[.]com, new[.]americold[.]com**

8\. Which certificate authority issued the SSL certificate to the first domain from the previous question?

Whois lookup can provide the registrar information.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-8.png" img_datasrc="../assets/img/analysis/carnage/answer-8.png" img_caption="Figure 11: Answer 8" img_alt="Answer 8" %}
Answer: **GoDaddy**

9\. What are the two IP addresses of the Cobalt Strike servers? Use VirusTotal (the Community tab) to confirm if IPs are identified as Cobalt Strike C2 servers. (answer format: enter the IP addresses in sequential order)

C2 servers use the following common ports i.e. 80,8080, 50050.

We filter using `tcp.port == 80 or tcp.port == 8080 or tcp.port == 50050`

The conversion statistics with the most packets can be checked for C2 servers.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-9a.png" img_datasrc="../assets/img/analysis/carnage/answer-9a.png" img_caption="Figure 12: Answer 9a" img_alt="Answer 9a" %}

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-9b.png" img_datasrc="../assets/img/analysis/carnage/answer-9b.png" img_caption="Figure 13: Answer 9b" img_alt="Answer 9b" %}
{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-9c.png" img_datasrc="../assets/img/analysis/carnage/answer-9c.png" img_caption="Figure 14: Answer 9c" img_alt="Answer 9c" %}
{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-9d.png" img_datasrc="../assets/img/analysis/carnage/answer-9d.png" img_caption="Figure 15: Answer 9d" img_alt="Answer 9d" %}
Answer: **185[.]106[.]96[.]158, 185[.]125[.]204[.]174**

10\. What is the Host header for the first Cobalt Strike IP address from the previous question?

We can get the host using the HTTP protocol,

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-10.png" img_datasrc="../assets/img/analysis/carnage/answer-10.png" img_caption="Figure 16: Answer 10" img_alt="Answer 10" %}
Answer: **ocsp.verisign.com**

11\. What is the domain name for the first IP address of the Cobalt Strike server? You may use VirusTotal to confirm if it's the Cobalt Strike server (check the Community tab).

We change the name resolution to resolve the network address.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-11.png" img_datasrc="../assets/img/analysis/carnage/answer-11.png" img_caption="Figure 17: Answer 11" img_alt="Answer 11" %}
Answer: **survmeter[.]live**

12\. What is the domain name of the second Cobalt Strike server IP?  You may use VirusTotal to confirm if it's the Cobalt Strike server (check the Community tab).

Similar as question 11.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-12.png" img_datasrc="../assets/img/analysis/carnage/answer-12.png" img_caption="Figure 18: Answer 12" img_alt="Answer 12" %}
Answer: **securitybusinpuff[.]com**

13\. What is the domain name of the post-infection traffic?

We inspect the HTTP POST Traffic using `http and http.request.method == "POST"`.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-13.png" img_datasrc="../assets/img/analysis/carnage/answer-13.png" img_caption="Figure 19: Answer 13" img_alt="Answer 13" %}
Answer: **maldivehost[.]net**

14\. What are the first eleven characters that the victim host sends out to the malicious domain involved in the post-infection traffic?

From the info section (From the 13th answer).

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-14.png" img_datasrc="../assets/img/analysis/carnage/answer-14.png" img_caption="Figure 20: Answer 14" img_alt="Answer 14" %}
Answer: **zLIisQRWZI9**


15\. What was the length for the first packet sent out to the C2 server?

From the length section (From the 13th answer).

Answer: **281**


16\. What was the Server header for the malicious domain from the previous question?

Following the packet (From the 13th answer) in HTTP stream,

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-16.png" img_datasrc="../assets/img/analysis/carnage/answer-16.png" img_caption="Figure 21: Answer 16" img_alt="Answer 16" %}
Answer: **Apache/2.4.49 (cPanel) OpenSSL/1.1.1l mod_bwlimited/1.4**


17\. The malware used an API to check for the IP address of the victim’s machine. What was the date and time when the DNS query for the IP check domain occurred?

We check DNS queries for such a service.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-17.png" img_datasrc="../assets/img/analysis/carnage/answer-17.png" img_caption="Figure 22: Answer 17" img_alt="Answer 17" %}
Answer: **2021-09-24 17:00:04**

18\. What was the domain in the DNS query from the previous question?

From the same packet (Refer answer 17).

Answer: **api[.]ipify[.]org**

19\. Looks like there was some malicious spam (malspam) activity going on. What was the first MAIL FROM address observed in the traffic?

We checked the SMTP request parameters.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-19.png" img_datasrc="../assets/img/analysis/carnage/answer-19.png" img_caption="Figure 23: Answer 19" img_alt="Answer 19" %}
Answer: **farshin[@]mailfa[.]com**

20\. How many packets were observed for the SMTP traffic?

Protocol hierarchy statistics for SMTP can provide the number of packets observed.

{% include lazyimg.html img_src="../assets/img/analysis/carnage/lowly/answer-20.png" img_datasrc="../assets/img/analysis/carnage/answer-20.png" img_caption="Figure 24: Answer 20" img_alt="Answer 20" %}
Answer: **1439**

We meet next time until then さようなら。.