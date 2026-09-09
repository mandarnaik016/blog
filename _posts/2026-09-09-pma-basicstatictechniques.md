---
layout: post
title: PMA - Basic Static Techniques
subtitle: Lab 1-1-1-2
cover-img: /assets/img/pma/pma.png
thumbnail-img: ""
tags: [pma, security, analysis]
---

## Lab 1-1

### Questions

1\. Upload the files to [http://www.VirusTotal.com](http://www.VirusTotal.com) and view the reports. Does either file match any existing antivirus signatures?

Answer: _Lab01-01.exe_ was detected by 53/69 engines, and _Lab01-01.dll_ was detected by 39/70 engines.

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-1-lab-1-1.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-1-lab-1-1.png" img_caption="Figure 1: Answer 1 Lab 1-1" img_alt="Answer 1 Lab 1-1" %}

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-1-lab-1-1-part-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-1-lab-1-1-part-2.png" img_caption="Figure 2: Answer 1 Lab 1-1 Part 2" img_alt="Answer 1 Lab 1-1 Part 2" %}

2\. When were these files compiled?

Answer: _Lab01-01.exe_ was compiled on _Sun Dec 19 16:16:19 2010 (UTC)_, and _Lab01-01.dll_ was compiled on _Sun Dec 19 16:16:38 2010 (UTC)_.

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-2-lab-1-1.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-2-lab-1-1.png" img_caption="Figure 3: Answer 2 Lab 1-1" img_alt="Answer 2 Lab 1-1" %}  

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-2-lab-1-1-part-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-2-lab-1-1-part-2.png" img_caption="Figure 4: Answer 2 Lab 1-1 Part 2" img_alt="Answer 2 Lab 1-1 Part 2" %}

3\. Are there any indications that either of these files is packed or obfuscated? If so, what are these indicators?

Answer: None of the files are packed or obfuscated.

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-3-lab-1-1.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-3-lab-1-1.png" img_caption="Figure 5: Answer 3 Lab 1-1" img_alt="Answer 3 Lab 1-1" %}

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-3-lab-1-1-part-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-3-lab-1-1-part-2.png" img_caption="Figure 6: Answer 3 Lab 1-1 Part 2" img_alt="Answer 3 Lab 1-1 Part 2" %}

4\. Do any imports hint at what this malware does? If so, which imports are they?

Answer: We could picture the following,

KERNEL32.dll for _Lab01-01.exe_,

|     |     |
| --- | --- |
| Name | Finding |
| CreateFileA | Creates or Opens a file. |
| CopyFileA | Copies a file. |
| FindNextFileA & FindFirstFileA | Searches a file. |
| FindClose | Closes searching |

<br>

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-4-lab-1-1.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-4-lab-1-1.png" img_caption="Figure 7: Answer 4 Lab 1-1" img_alt="Answer 4 Lab 1-1" %}

KERNEL32.dll and MSVCRT.dll for _Lab01-01.dll_,

|     |     |
| --- | --- |
| Name | Finding |
| CreateProcessA | Creates process. |
| malloc | Allocates memory. |
| free | Frees the allocated memory. |

<br>

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-4-lab-1-1-part-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-4-lab-1-1-part-2.png" img_caption="Figure 8: Answer 4 Lab 1-1 Part 2" img_alt="Answer 4 Lab 1-1 Part 2" %}

5\. Are there any other files or host-based indicators that you could look for on infected systems?

Answer: From strings, the file _Lab01-01.exe_ contains references to _Lab01-01.dll_ and _C:\\windows\\system32\\kerne132.dll_. The binary might be cloning to the system directory or loading a previously dumped DLL.

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-5-lab-1-1.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-5-lab-1-1.png" img_caption="Figure 9: Answer 5 Lab 1-1" img_alt="Answer 5 Lab 1-1" %}

6\. What network-based indicators could be used to find this malware on infected machines?

Answer: From strings, The file _Lab01-01.dll_ contains an IP address being 127\[.\]26\[.\]152\[.\]13.

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-6-lab-1-1.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-6-lab-1-1.png" img_caption="Figure 10: Answer 6 Lab 1-1" img_alt="Answer 6 Lab 1-1" %}

7\. What would you guess is the purpose of these files?

Answer: The PE file seems to be loading the DLL, and then the DLL provides a reverse connection to the aforementioned IP address (from answers 5 & 6).

## Lab 1-2

### Questions

1\. Upload the Lab01-02.exe file to http://www.VirusTotal.com/. Does it match any existing antivirus definitions?

Answer: The file _Lab01-02.exe_ was detected by 56/69 engines.

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-1-lab-1-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-1-lab-1-2.png" img_caption="Figure 11: Answer 1 Lab 1-2" img_alt="Answer 1 Lab 1-2" %}

2\. Are there any indications that this file is packed or obfuscated? If so, what are these indicators? If the file is packed, unpack it if possible.

Answer: The binary is packed using UPX. We can unpack it using,
```
upx -d "Lab01-02.exe" -o "Lab01-02_unpacked.exe"
```

<br>

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-2-lab-1-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-2-lab-1-2.png" img_caption="Figure 12: Answer 2 Lab 1-2" img_alt="Answer 2 Lab 1-2" %}

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-2-lab-1-2-part-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-2-lab-1-2-part-2.png" img_caption="Figure 13: Answer 2 Lab 1-2 Part 2" img_alt="Answer 2 Lab 1-2 Part 2" %}

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-2-lab-1-2-part-3.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-2-lab-1-2-part-3.png" img_caption="Figure 14: Answer 2 Lab 1-2 Part 3" img_alt="Answer 2 Lab 1-2 Part 3" %}

3\. Do any imports hint at this program’s functionality? If so, which imports are they and what do they tell you?

Answer: The binary creates and starts a service (functionality from _ADVAPI32.dll_), Additionally it connects to the internet for a resource (functionality from _WININET.dll_).

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-3-lab-1-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-3-lab-1-2.png" img_caption="Figure 15: Answer 3 Lab 1-2" img_alt="Answer 3 Lab 1-2" %}

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-3-lab-1-2-part-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-3-lab-1-2-part-2.png" img_caption="Figure 16: Answer 3 Lab 1 3 Part 2" img_alt="Answer 3 Lab 1-2 Part 2" %}

4\. What host- or network-based indicators could be used to identify this malware on infected machines?

Answer: The binary connects to hxxp[://]www[.]malwareanalysisbook[.]com (network-based indicators) and creates a service _Malservice_ (host-based indicators).

{% include lazyimg.html img_src="../assets/img/pma/basicstatictechniques/lowly/answer-4-lab-1-2.png" img_datasrc="../assets/img/pma/basicstatictechniques/answer-4-lab-1-2.png" img_caption="Figure 17: Answer 4 Lab 1-2" img_alt="Answer 4 Lab 1-2" %}
