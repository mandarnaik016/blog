---
layout: post
title: Traffic Analysis - Easy As 123
subtitle: Easy, Easier, & Easiest.
cover-img: /assets/img/analysis/analysis.jpeg
thumbnail-img: ""
tags: [analysis, security, network]
---

Hello, in this post, we will perform network traffic analysis for the [EASY AS 123](https://www.malware-traffic-analysis.net/2026/02/28/index.html) exercise.

**DETAILS OF LAN SEGMENT**
 - LAN segment range:  10.2.28[.]0/24   (10.2.28[.]0 through 10.2.28[.]255)
 - Domain:  easyas123[.]tech
 - AD environment name:  EASYAS123
 - Active Directory (AD) domain controller:  10.2.28[.]2 - EASYAS123-DC
 - LAN segment gateway:  10.2.28[.]1
 - LAN segment broadcast address:  10.2.28[.]255

**BACKGROUND**
 - Several signature hits for NetSupport Manager RAT from 45.131.214[.]85 over TCP port 443.
 - The activity started on 2026-02-28 at 19:55 UTC.

Let's begin

1. IP address of the infected system.

 * From the briefing, there is a connection to NetSupport Manager RAT IP address 45.131.214[.]85. We hunt for the packets containing this IP address.
 {% include lazyimg.html img_src="../assets/img/analysis/easy/lowly/ip_address_of_infected_system.png" img_datasrc="../assets/img/analysis/easy/ip_address_of_infected_system.png" img_caption="Figure 1: IP address" img_alt="IP address" %}
 * We could observe a connection initiated only from *10.2.28[.]88*.

2. MAC address of the infected system.

 * From any connection to and from 10.2.28[.]88, we can locate the MAC address.
 {% include lazyimg.html img_src="../assets/img/analysis/easy/lowly/mac_address_of_infected_system.png" img_datasrc="../assets/img/analysis/easy/mac_address_of_infected_system.png" img_caption="Figure 2: MAC address" img_alt="MAC address" %}
 * The corresponding MAC address is *00:19:d1:b2:4d:ad*.

3. Host name of the infected system.
 * One of the simplest ways to get a hostname is via DHCP.
 {% include lazyimg.html img_src="../assets/img/analysis/easy/lowly/dhcp_event.png" img_datasrc="../assets/img/analysis/easy/dhcp_event.png" img_caption="Figure 3: DHCP event" img_alt="DHCP event" %}
 * Unfortunately, DHCP does not include the “Host Name” field.
 * We resort to NetBIOS Name Service, 
 {% include lazyimg.html img_src="../assets/img/analysis/easy/lowly/hostname_of_infected_system.png" img_datasrc="../assets/img/analysis/easy/hostname_of_infected_system.png" img_caption="Figure 4: Hostname" img_alt="Hostname" %}
 * The hostname is *DESKTOP-TEYQ2NR*.

4. User account name from the infected system.
 * The CNameString from Kerberos would reflect the user account name. In this case, *brolf*.
 {% include lazyimg.html img_src="../assets/img/analysis/easy/lowly/account_name_of_infected_system.png" img_datasrc="../assets/img/analysis/easy/account_name_of_infected_system.pngort-alert-count.png" img_caption="Figure 5: Account name" img_alt="Account name" %}

5. Full name of user.
 * We utilize the SAMR (Security Account Manager Remote Protocol) to get this information,
 {% include lazyimg.html img_src="../assets/img/analysis/easy/lowly/full_name_of_user.png" img_datasrc="../assets/img/analysis/easy/full_name_of_user.png" img_caption="Figure 6: Full name" img_alt="Full name" %}
 * The full name of the user is *Becka Rolf*.

QUESTIONS? **ANSWERS**
 - What is the IP address of the infected Windows client? **10.2.28[.]88**
 - What is the MAC address of the infected Windows client? **00:19:d1:b2:4d:ad**
 - What is the host name of the infected Windows client? **DESKTOP-TEYQ2NR**
 - What is the user account name from the infected Windows client? **brolf**
 - What is the full name of the user from the user account? **Becka Rolf**

We meet next time dissecting another sample or comming up with an evasion technique until then Aloha.