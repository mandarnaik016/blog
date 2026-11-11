---
layout: post
title: Traffic Analysis - KONGTUKE REBUKE
subtitle: Quite A Circus Backstage.
cover-img: /assets/img/analysis/malware-analysis.png
thumbnail-img: ""
tags: [analysis, security, network]
---

* TOC
{:toc}

## BACKGROUND

I investigated recent Kongtuke ClickFix activity using a domain-joined host in an Active Directory environment.

The characteristics of this environment are:
- LAN segment range: 10.9.11\[.\]0/24 (10.9.11\[.\]0 through 10.9.11\[.\]255)
- Domain: overhands\[.\]org
- AD environment name: OVERHANDS
- Active Directory (AD) domain controller: 10.9.11\[.\]2 - WIN-GTWXC9UYSE4
- LAN segment gateway: 10.9.11\[.\]1
- LAN segment broadcast address: 10.9.11\[.\]255

## METHODOLOGY

The infection method is **ClickFix**, which uses a CAPTCHA-solving webpage to trick users into running a series of commands under the guise of completing CAPTCHA verification.

I have conducted an in-depth malware analysis of these techniques in the following articles.
1. [Malware Analysis - Lumma Stealer][lumma-ma]
2. [Traffic Analysis - LUMMA IN THE ROOM-AH][lumma-na]

In the initial triage, we note the top endpoints involved in conversions by number of packets and bytes transferred. In this technique, a large number of back-and-forth connections would be made from an endpoint to multiple URLs/IPs.

![Top conversation][top-conversation]

We hypothetically assume the system with IP 10.9.11\[.\]135 is infected. To confirm the hypothesis, leverage DNS packets to extract and filter the domains for subsequent reputation analysis.

| Domain                    | Reputation | Community |
| ------------------------- | ---------- | --------- |
| aatthews[.]cfd            | 19/92      | -60       |
| hyko[.]fif-lost[.]com     | 1/92       | 0         |
| logincrypt8338[.]com      | 18/92      | -60       |
| opscast3707[.]net         | 1/92       | 0         |
| quadcinema[.]com          | 0/92       | 0         |
| stream[.]fif-lost[.]com   | 1/92       | 0         |
| winrun2915[.]com          | 6/92       | -11       |

We correlate DNS queries to identify potentially malicious connections. We then proceed to build a profile of the infected system.

To identify the MAC address of the infected system, we leverage the ARP protocol.

![MAC address][mac-address]

Subsequently, the hostname and username can be retrieved from Kerberos traffic.

![Host and User name][host-user-name]

Finally, we retrieve the user's full name using the SAMR protocol.

![Full name][full-name]

## QUESTION & ANSWER

1. What is the IP address of the infected Windows client? **10.9.11.135**
2. What is the MAC address of the infected Windows client? **08:d4:0c:7a:29:1e**
3. What is the host name of the infected Windows client? **DESKTOP\-6T17ZFM**
4. What is the user account name from the infected Windows client? **gmcdowell**
5. What is the full name of the user from the user account? **Gabriel McDowell**

[lumma-ma]: /blog/2024-10-05-malware-analysis-lumma-stealer/
[lumma-na]: /blog/2026-10-04-traffic-analysis-lumma-in-the-room-ah
[top-conversation]: ../assets/img/nta/kongtuke/top-conversation.png
[mac-address]: ../assets/img/nta/kongtuke/infected_system_mac.png
[host-user-name]: ../assets/img/nta/kongtuke/infected_system_host_user_name.png
[full-name]: ../assets/img/nta/kongtuke/infected_system_full_name.png