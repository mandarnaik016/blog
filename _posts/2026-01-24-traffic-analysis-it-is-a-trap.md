---
layout: post
title: Traffic Analysis - It Is A Trap!
subtitle: PHP? Payload Helped Payload.
cover-img: /assets/img/analysis/analysis.jpeg
thumbnail-img: ""
tags: [analysis, security, network]
---

Hello, in this post, we will do network traffic analysis of an exercise [IT'S A TRAP](https://www.malware-traffic-analysis.net/2025/06/13/index.html).

**DETAILS OF LAN SEGMENT**
- LAN segment range:  10.6.13[.]0/24   (10.6.13[.]0 through 10.6.13[.]255)
- Domain:  massfriction[.]com
- Active Directory (AD) domain controller:  10.6.13[.]3 - WIN-DQL4WFWJXQ4
- AD environment name:  MASSFRICTION
- LAN segment gateway:  10.6.13[.]1
- LAN segment broadcast address:  10.6.13[.]255

We load the PCAP file in Snort to list the alerts it would have triggered,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/snort-alert-count.png" img_datasrc="../assets/img/analysis/trap/snort-alert-count.png" img_caption="Figure 1: Snort alert count" img_alt="Snort alert count" %}

The alert count is 138. Let’s view the type of alerts,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/alert-port-scanning.png" img_datasrc="../assets/img/analysis/trap/alert-port-scanning.png" img_caption="Figure 2: Alert port scanning" img_alt="Alert port scanning" %}

Multiple HTTP URI alerts were also observed. Typically, either to and fro from **10.6.13.133**.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/alert-http-uri.png" img_datasrc="../assets/img/analysis/trap/alert-http-uri.png" img_caption="Figure 3: Alert HTTP URI" img_alt="Alert HTTP URI" %}

After we analyze the DNS entries, we find some entries that might be suspicious.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/dns-queries-1.png" img_datasrc="../assets/img/analysis/trap/dns-queries-1.png" img_caption="Figure 4: DNS queries part 1" img_alt="DNS queries part 1" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/dns-queries-2.png" img_datasrc="../assets/img/analysis/trap/dns-queries-2.png" img_caption="Figure 5: DNS queries part 2" img_alt="DNS queries part 2" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/dns-queries-3.png" img_datasrc="../assets/img/analysis/trap/dns-queries-3.png" img_caption="Figure 6: DNS queries part 3" img_alt="DNS queries part 3" %}

The Virustotal results confirms we are on the right track.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-1.png" img_datasrc="../assets/img/analysis/trap/suspected-url-1.png" img_caption="Figure 7: Suspected URL 1" img_alt="Suspected URL 1" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-2.png" img_datasrc="../assets/img/analysis/trap/suspected-url-2.png" img_caption="Figure 8: Suspected URL 2" img_alt="Suspected URL 2" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-3.png" img_datasrc="../assets/img/analysis/trap/suspected-url-3.png" img_caption="Figure 9: Suspected URL 3" img_alt="Suspected URL 3" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-4.png" img_datasrc="../assets/img/analysis/trap/suspected-url-4.png" img_caption="Figure 10: Suspected URL 4" img_alt="Suspected URL 4" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-5.png" img_datasrc="../assets/img/analysis/trap/suspected-url-5.png" img_caption="Figure 11: Suspected URL 5" img_alt="Suspected URL 5" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-6.png" img_datasrc="../assets/img/analysis/trap/suspected-url-6.png" img_caption="Figure 12: Suspected URL 6" img_alt="Suspected URL 6" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-7.png" img_datasrc="../assets/img/analysis/trap/suspected-url-7.png" img_caption="Figure 13: Suspected URL 7" img_alt="Suspected URL 7" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-8.png" img_datasrc="../assets/img/analysis/trap/suspected-url-8.png" img_caption="Figure 14: Suspected URL 8" img_alt="Suspected URL 8" %}

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspected-url-9.png" img_datasrc="../assets/img/analysis/trap/suspected-url-9.png" img_caption="Figure 15: Suspected URL 9" img_alt="Suspected URL 9" %}

All these outbound connections were originating from **10.6.13.133** (The Snort log also had the same IP for HTTP URI alerts Ref. fig. 2).

We now analyze http requets from the same ip address,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/suspicious-outbound-request.png" img_datasrc="../assets/img/analysis/trap/suspicious-outbound-request.png" img_caption="Figure 16: Suspicious outbound request" img_alt="Suspicious outbound request" %}

BINGO!, The very first request made to one of the suspicious entries contains *PowerShell* as the user agent. We follow the request in HTTP stream,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/powershell-script-in-stream.png" img_datasrc="../assets/img/analysis/trap/powershell-script-in-stream.png" img_caption="Figure 17: Powershell script in stream" img_alt="Powershell script in stream" %}

The response contains a PowerShell script. Let's view the script,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/powershell-script-1.png" img_datasrc="../assets/img/analysis/trap/powershell-script-1.png" img_caption="Figure 18: Powershell script 1" img_alt="Powershell script 1" %}

Most of the lines are dead code.
example,
```
for ($i = 0; $i -lt 5; $i++) { $nextvar = $i }
try { $y = 0 } catch { $error }
if ($errorLevel -gt 7) { Write-Output ‘$result’ }
while ($binpath) { Start-Sleep -Seconds 0 }
```

We mark all of them similarly to the above pattern,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/dead-code-in-powershell-script-1.png" img_datasrc="../assets/img/analysis/trap/dead-code-in-powershell-script-1.png" img_caption="Figure 19: Dead code in powershell script 1" img_alt="Dead code in powershell script 1" %}

We removed redundant lines,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/cleaned-powershell-script-1.png" img_datasrc="../assets/img/analysis/trap/cleaned-powershell-script-1.png" img_caption="Figure 20: Cleaned powershell script 1" img_alt="Cleaned powershell script 1" %}

Insight (From fig. 20):
1. The first blob contains base64 encoded strings that are being concatenated later.
2. The second string contains powershell command to convert from  base64.
3. The third string executes the decoded base64 script.

We use the following recipe to extract base64, concatenate them, and decode them.

```
Regular_expression('User defined','\\s=\\s"(.*?)"',true,true,false,false,false,false,'List capture groups')
Find_/_Replace({'option':'Extended (\\n, \\t, \\x...)','string':'\\n'},'',true,false,true,false)
From_Base64('A-Za-z0-9+/=',true,false)

```

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/decoded-base64-of-powershell-script-1.png" img_datasrc="../assets/img/analysis/trap/decoded-base64-of-powershell-script-1.png" img_caption="Figure 21: Decoded base64 of powershell script 1" img_alt="Decoded base64 of powershell script 1" %}

The decoded base64 contains another PowerShell script. Let's view it.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/powershell-script-1.1.png" img_datasrc="../assets/img/analysis/trap/powershell-script-1.1.png" img_caption="Figure 22: Powershell script 1.1" img_alt="Powershell script 1.1" %}

After deobfuscation, the script we get,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/deobfuscated-powershell-script-1.1.png" img_datasrc="../assets/img/analysis/trap/deobfuscated-powershell-script-1.1.png" img_caption="Figure 23: Deobfuscated powershell script 1.1" img_alt="Deobfuscated powershell script 1.1" %}

The output of the command **systeminfo** is passed as a POST request to the URL "eventdata-microsoft[.]live/NV4RgNEu".

We could see an outbound request being made to this uncovered URL.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/outbound-request-made-by-powershell-script-1.1.png" img_datasrc="../assets/img/analysis/trap/outbound-request-made-by-powershell-script-1.1.png" img_caption="Figure 24: Outbound request made by powershell script 1.1" img_alt="Outbound request made by powershell script 1.1" %}

We could see the **systeminfo** output in the TCP stream,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/system-info-in-post-request.png" img_datasrc="../assets/img/analysis/trap/system-info-in-post-request.png" img_caption="Figure 25: System info in post request" img_alt="System info in post request" %}

Additionally, we could see another PowerShell script as a response from the server,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/powershell-script-2-in-stream.png" img_datasrc="../assets/img/analysis/trap/powershell-script-2-in-stream.png" img_caption="Figure 26: Powershell script 2 in stream" img_alt="Powershell script 2 in stream" %}

let's view this script

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/powershell-script-2.png" img_datasrc="../assets/img/analysis/trap/powershell-script-2.png" img_caption="Figure 27: Powershell script 2" img_alt="Powershell script 2" %}

This PowerShell script seems extremely obfuscated, spanning over 13K lines of code. Deobfuscating this lengthy script is near impossible until…

We use bankai!

{% include lazyimg.html img_src="../assets/img/analysis/lowly/bankai.jpg" img_datasrc="../assets/img/analysis/bankai.jpg" img_caption="Bankai!" img_alt="Bankai!" %}

We mark the redundant lines as similar to the previous one.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/dead-code-in-powershell-script-2.png" img_datasrc="../assets/img/analysis/trap/dead-code-in-powershell-script-2.png" img_caption="Figure 28: Dead code in powershell script 2" img_alt="Dead code in powershell script 2" %}

Removing them, we are left with.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/cleaned-powershell-script-2.png" img_datasrc="../assets/img/analysis/trap/cleaned-powershell-script-2.png" img_caption="Figure 29: Cleaned powershell script 2" img_alt="Cleaned powershell script 2" %}

We could observe same pattern of script containing base64 blobs being concatenated and invoked. We use the same CyberChef recipe as earlier.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/decoded-base64-of-powershell-script-2.png" img_datasrc="../assets/img/analysis/trap/decoded-base64-of-powershell-script-2.png" img_caption="Figure 30: Decoded base64 of powershell script 2" img_alt="Decoded base64 of powershell script 2" %}

We could observe another obfuscated PowerShell script as output,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/powershell-script-2.1.png" img_datasrc="../assets/img/analysis/trap/powershell-script-2.1.png" img_caption="Figure 31: Powershell script 2.1" img_alt="Powershell script 2.1" %}

When deobfuscated, we get a readable PowerShell script as,

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/deobfuscated-powershell-script-2.1-part1.png" img_datasrc="../assets/img/analysis/trap/deobfuscated-powershell-script-2.1-part1.png" img_caption="Figure 32: Deobfuscated powershell script 2.1 part1" img_alt="Deobfuscated powershell script 2.1 part1" %}

Insight (From fig. 32):
1. The php binaries for Windows are being downloaded from the URL of version 8.2.28 in %temp% locations as php.zip.
2. Then the downloaded zip is extracted to ApplicationData\php directory.
3. After extraction, the file is deleted from the %temp% location.
4. The config and php binary absolute paths are set to,
	- $mv = ApplicationData\php\config.cfg
	- $YupgDUknfb = ApplicationData\php\php.exe
5. We could see another base64 encoded string stored in a variable, $X9.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/decoded-base64-of-powershell-script-2.1.png" img_datasrc="../assets/img/analysis/trap/decoded-base64-of-powershell-script-2.1.png" img_caption="Figure 33: Decoded base64 of powershell script 2.1" img_alt="Decoded base64 of powershell script 2.1" %}

The decoded base64 contains obfuscated php script.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/deobfuscated-powershell-script-2.1-part2.png" img_datasrc="../assets/img/analysis/trap/deobfuscated-powershell-script-2.1-part2.png" img_caption="Figure 34: Deobfuscated powershell script 2.1 part2" img_alt="Deobfuscated powershell script 2.1 part2" %}

Insight (From fig. 34):
1. The first section decodes the base64 data (containing php script) and writes to a file ApplicationData\php\config.cfg pointed by the variable $mv.
2. The second section executes the obfuscated PHP script using the official PHP binary downloaded earlier and extracted in ApplicationData\php folder. The output of the executed php file is written in two files, pointed by *$UZ3eaxi6FRJQ0yaCX* and *$GhzCP*.
3. The content of those is stored in *$lMeQbHXUc* and *$2oRVdufAtTxwFJB*.
4. After the content is stored, the created files are deleted.
5. The third section sends the data as a POST request to the URL "comprehensive-cabin-spend-organic[.]trycloudflare[.]com/NV4RgNEu" after concatenation via a delimiter "-=-=-=-=-=-".

We can get the MAC address and hostname using DHCP protocol.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/dhcp-protocol.png" img_datasrc="../assets/img/analysis/trap/dhcp-protocol.png" img_caption="Figure 13: DHCP protocol" img_alt="DHCP protocol" %}

For the user account name, we use kerberos protocol.

{% include lazyimg.html img_src="../assets/img/analysis/trap/lowly/kerberos-protocol.png" img_datasrc="../assets/img/analysis/trap/kerberos-protocol.png" img_caption="Figure 17: Kerberos protocol" img_alt="Kerberos protocol" %}

QUESTIONS? **ANSWERS**
- What is the IP address of the infected Windows client? **10.6.13.133**
- What is the mac address of the infected Windows client? **24:77:03:AC:97:DF**
- What is the host name of the infected Windows client?  **DESKTOP-5AVE44C**
- What is the user account name from the infected Windows client? **rgaines**

We meet next time dissecting another sample or comming up with an evasion technique until then Nabad gelyo.