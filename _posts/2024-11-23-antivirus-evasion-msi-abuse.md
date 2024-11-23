---
layout: post
title: Antivirus Evasion - MSI Abuse
subtitle: Malware Security Interface?
cover-img: /assets/img/evasion/xor/evasion-thumb.png
thumbnail-img: ""
tags: [evasion, security]
---

Yeah, this is yet another effort by us trying to bypass antivirus! We are using **MSI abuse** for this evasion technique.

The most common format for installing any application designed for Windows is either "EXE" or "MSI." The concepts of stub and packer can be applied to both of them. For EXE files, writing a stub and its extractor is not a tea of anyone's cup. MSI, that might not be the case.

I discovered this technique while I was doing the malware analysis and reverse engineering of [Rozena](/2024-10-19-malware-analysis-rozena/).

We are using WiX for this purpose. Below is the execution workflow.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/evasion-workflow.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/evasion-workflow.png" img_alt="evasion workflow" %}

Firstly, the user will execute the MSI file for the installation of the app. The MSI file has 4 embedded objects within it, i.e., the script that does the operations, a carrier file (in this case, we are using PicoCrypt as an example), 7zip, and at last the encrypted archive.

We are using **LockBit ransomware** as our payload. The below directory contains the entire output generated using lockbit builder.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/lockbit-malicious-files.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/lockbit-malicious-files.png" img_alt="lockbit malicious files" %}

Let us check the number of detections it has on Virustotal.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/lockbit-vt.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/lockbit-vt.png" img_alt="lockbit vt" %}

Below is the source code created to build our MSI using WiX,

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/msi-builder-setup.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/msi-builder-setup.png" img_alt="msi builder setup" %}

We place the infected.exe in the *mal* folder, (this is the actual LockBit Ransomware).

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/infected-file-in-mal-folder.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/infected-file-in-mal-folder.png" img_alt="infected file in mal folder" %}

The *product.wxs* is the WiX script that defines the name and information of the MSI file. It also contains references to all the objects that will be embedded. At last, a custom action is defined to run the bat script immediately after the installation of the content in MSI is done.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/product.wxs-script.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/product.wxs-script.png" img_alt="product.wxs script" %}

The *script.bat* contains commands to extract the infected file from the archive and execute it along with executing the embedded carrier file.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/script-exec.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/script-exec.png" img_alt="script exec" %}

The *archive.bat* just creates the encrypted archive.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/archive.bat-script.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/archive.bat-script.png" img_alt="archive.bat script" %}

When we run the *archive.bat* file, we see an *infected.7z* being created.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/infected.7z-created.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/infected.7z-created.png" img_alt="infected.7z created" %}

The *build.bat* generates the final MSI file.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/msi-builder.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/msi-builder.png" img_alt="msi builder" %}

After the script execution, we can see the *product.msi* is created using WiX.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/msi-malicious-created.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/msi-malicious-created.png" img_alt="msi malicious created" %}

Let us check the detection of this newly created MSI file.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/msi-malicious-vt.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/msi-malicious-vt.png" img_alt="msi malicious vt" %}

Pretty interesting to see that it was detected by **22 engines** as malicious. But none of the detection rules includes a LockBit signature.

Let Rock n roll

After execution of the MSI file, it loads the carrier file i.e. PicoCrypt.

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/fake-file-exec.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/fake-file-exec.png" img_alt="fake file exec" %}

{% include lazyimg.html img_src="../assets/img/evasion/msi-abuse/lowly/lockbit-exec-at-backend.jpeg" img_datasrc="../assets/img/evasion/msi-abuse/lockbit-exec-at-backend.png" img_alt="lockbit exec at backend" %}

We finally see the LockBit logo on files on the Desktop.

We meet next time dissecting another sample or coming up with an evasion technique until then Ciao ciao.
