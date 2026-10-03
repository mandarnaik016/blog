---
layout: post
title: Traffic Analysis - LUMMA IN THE ROOM-AH
subtitle: Not ME, The Browser Said!
cover-img: /assets/img/analysis/malware-analysis.png
thumbnail-img: ""
tags: [analysis, security, network]
---

* TOC
{:toc}

## BACKGROUND

As an analyst at a Security Operations Center (SOC), you check alerts for the past week and find a signature hit for ET MALWARE Lumma Stealer Victim Fingerprinting Activity that triggered on traffic from 153.92.1\[.\]49 over TCP port 80. The alert triggered on 2026-01-27 at 23:05 UTC.

Using the information, you retrieve a packet capture (pcap) of the traffic from the internal IP address that triggered the alert. Based on the pcap, you write up an incident report, so the incident responders can track down the computer and associated user.

The characteristics of your environment are:

- LAN segment range: 10.1.21\[.\]0/24 (10.1.21\[.\]0 through 10.1.21\[.\]255)
- Domain: win11office\[.\]com
- AD environment name: WIN11OFFICE
- Active Directory (AD) domain controller: 10.1.21\[.\]2 - WIN-LU4L24X3UB7
- LAN segment gateway: 10.1.21\[.\]1
- LAN segment broadcast address: 10.1.21\[.\]255

## METHODOLOGY

Based on the briefing, a signature hit was detected on traffic to `153.92.1[.]49` over TCP port `80`. We can identify the systems that initiated connections to this destination

{% include lazyimg.html img_src="../assets/img/nta/lumma/lowly/victim.png" img_datasrc="../assets/img/nta/lumma/victim.png" img_caption="Fig. 1: Victim" img_alt="Victim" %}

```sql
_path == "conn" | where id.resp_h == 153.92.1.49 and id.resp_p == 80 | cut id.orig_h | sort | uniq
```

Running the above query against the pcap in Brim lists all endpoints that initiated connections to **Lumma malware**.

The victim is `10.1.21[.]58`. We can use this IP address as the starting point for further investigation.

We analyze the DNS queries, filter out potential noise, and arrange the results chronologically by timestamp.

{% include lazyimg.html img_src="../assets/img/nta/lumma/lowly/suspicious-dns-queries.png" img_datasrc="../assets/img/nta/lumma/suspicious-dns-queries.png" img_caption="Fig. 2: DNS queries" img_alt="DNS queries" %}

```sql
_path == "dns" | where id.orig_h == 10.1.21.58 |  sort ts | cut query | where !grep(/(^wpad.*|^_ldap.*|.*.microsoft.com|.*.google.com|.*.googleapis.com|.*.gstatic.com|.*.local|.*.bing.com|.*.msn.com)/, query) and query != "desktop-es9f3ml"
```

We can filter the domains listed below as suspicious.

| No. | URL                                 | VirusTotal |
|-----|-------------------------------------|------------|
| 1   | hiyter[.]com                        | 0/91       |
| 2   | media[.]megafilehub4[.]lat          | 7/91       |
| 3   | arch[.]filemegahab4[.]sbs           | 1/91       |
| 4   | whooptm[.]cyou                      | 18/91      |
| 5   | whitepepper[.]su                    | 20/91      |
| 6   | holiday-forever[.]cc                | 16/91      |
| 7   | communicationfirewall-security[.]cc | 14/91      |

The corresponding resolved IPs

{% include lazyimg.html img_src="../assets/img/nta/lumma/lowly/resolved-dns.png" img_datasrc="../assets/img/nta/lumma/resolved-dns.png" img_caption="Fig. 3: DNS resolution" img_alt="DNS resolution" %}

```sql
_path == "dns" | cut query, answers | where query == "hiyter.com" or query == "media.megafilehub4.lat" or query == "arch.filemegahab4.sbs" or query == "whooptm.cyou" or query == "whitepepper.su" or query == "holiday-forever.cc" or query == "communicationfirewall-security.cc" | where answers != null | sort query | uniq
```

The IP 153.92.1\[.\]49 was resolved by the query `whitepepper[.]su `. We inspect the HTTP traffic of the same to gather further information.

We can see a series of requests exchanged, which are used for fingerprinting.

{% include lazyimg.html img_src="../assets/img/nta/lumma/lowly/suspicious-http.png" img_datasrc="../assets/img/nta/lumma/suspicious-http.png" img_caption="Fig. 4: HTTP traffic" img_alt="HTTP traffic" %}

We follow the conversation in the HTTP stream to establish a chronology.

The victim i.e., `10.1.21[.]58` initiates an HTTP GET request to the malicious server as follows:

```
GET /api/set_agent?id=3BF67EC05320C5729578BE4C0ADF174C&token=842e2802df0f0a06b4ed51f12f4387e761523b&description=&agent=Chrome HTTP/1.1
Host: whitepepper.su
```

The ID and token appear to be used to temporarily distinguish each client. The server responds with HTML containing JavaScript to collect data.

The JavaScript collects the following information from the endpoint and stores it in the corresponding variables:

1. **timestamp** — Current timestamp.
2. **system** — Platform, supported languages, device memory, and other system information.
3. **webgl** — WebGL vendor, renderer, supported extensions, and related information.
4. **canvas** — Canvas fingerprint generated from browser-based rendering.
5. **network** — Network connection type and estimated connection speed.
6. **screen** — Screen height, width, resolution, and orientation.
7. **hardware** — Device memory and available CPU cores.
8. **language** — Browser or system language.
9. **fonts** — Fonts available on the endpoint.
10. **webrtc** — WebRTC-related information, potentially including local network information.
11. **audio** — Audio context properties such as sample rate.
12. **misc** — Miscellaneous browser capabilities, including plugin information, cookie support, and Java support.

The aforementioned data is sent as an HTTP POST request with `Content-Type: application/x-www-form-urlencoded`, along with the previous ID and token. After the request is completed, the page is redirected to `about:blank`.

The POST request content is stored on server in a ZIP archive named using the identifier from the request in the format `IP-ID.zip`.

From the DHCP log, we can get the mac and hostname,

{% include lazyimg.html img_src="../assets/img/nta/lumma/lowly/endpoint-info.png" img_datasrc="../assets/img/nta/lumma/endpoint-info.png" img_caption="Fig. 5: Endpoint info" img_alt="Endpoint info" %}

```sql
_path == "dhcp" |  where client_addr == 10.1.21.58 | cut client_addr, mac, host_name
```

<br>

| Infected | MAC | Hostname |
|-|-|-|
| 10.1.21.58 | 00:21:5d:c8:0e:f2 | DESKTOP\-ES9F3ML |

The user account name can be extracted from the Kerberos logs.

{% include lazyimg.html img_src="../assets/img/nta/lumma/lowly/account-name.png" img_datasrc="../assets/img/nta/lumma/account-name.png" img_caption="Fig. 6: Account name" img_alt="Account name" %}

| User name |
| - |
| gwyatt |

The full name of the user can be extracted from SAMR protocol log,

{% include lazyimg.html img_src="../assets/img/nta/lumma/lowly/user-full-name.png" img_datasrc="../assets/img/nta/lumma/user-full-name.png" img_caption="Fig. 7: Full name" img_alt="Full name" %}

| Full name |
| - |
| Gabriel Wyatt |

## QUESTION & ANSWER

1. What is the IP address of the infected Windows client? **10.1.21[.]58**
2. What is the MAC address of the infected Windows client? **00:21:5d:c8:0e:f2**
3. What is the host name of the infected Windows client? **DESKTOP\-ES9F3ML**
4. What is the user account name from the infected Windows client? **gwyatt**
5. What is the full name of the user from the user account? **Gabriel Wyatt**
6. What is the domain from 153.92.1[.]49 that triggered the alert for Lumma Stealer? **whitepepper[.]su**