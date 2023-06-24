---
layout: post
title: Ultimate Guide To Block Ads
subtitle: More Than You Can Ever Imagine!
cover-img: /assets/img/adblock/thumb.png
thumbnail-img: ""
tags: [security]
---

## Why Ad-blockers?

Have at look at below image (p.s: The numbers could have been more than you can ever imagine!).

![Blocked Ads](/assets/img/adblock/blocked-ads-mobile.png){: .mx-auto.d-block :}

I am used to change my OS and browsers as the result the numbers of ads blocked is quite less.

I agree with you that some of the sites on the internet survive on the money earned through ads but now a days most of the time ads are present to **track** us down.

> Arguing that you don't care about the right to privacy because you have nothing to hide is no different than saying you don't care about free speech because you have nothing to say. - Edward Snowden 

## How Ad-blockers Work?

They exactly work like depicted below

![Cat Blocker](/assets/img/adblock/cat-blocker.png){: .mx-auto.d-block :}

Nothing rocket science over here they contains the rules to block and filter the webpage you are viewing. 

## How to Block Ads?

### Host Level

{: .box-note}
**Note:** Make sure to use notepad in administration mode.  

To block ads at **Host Level**, I use Dan Pollock [filter list](http://someonewhocares.org/hosts/).

- Copy the host entries from the website.
- Paste the entries in the host file located at 
	- For Windows 9x and ME place this file at `C:\Windows\hosts`
	- For NT, Win2K and XP use `C:\windows\system32\drivers\etc\hosts` or `C:\winnt\system32\drivers\etc\hosts`
	- For Windows 7 and Vista use `C:\windows\system32\drivers\etc\hosts` or `%systemroot%\system32\drivers\etc\hosts`
	- For Windows 8 and Windows 10 use `C:\Windows\System32\drivers\etc\hosts`
- Final host file should look similar to below one.

![Host](/assets/img/adblock/host.png){: .mx-auto.d-block :}  

### OS Level 

To block ads at **OS level**, I use [NextDNS](https://nextdns.io/).

- Create a account and configure the filter list in the privacy tab.
- Then Download their installer.
- After installing, right-click on NextDNS icon in the Systray then open the Settings. Set your Configuration ID.
- Right-click on NextDNS icon in the Systray, then click on Enable.

![NextDNS Dashboard](/assets/img/adblock/nextdns-dashboard.png){: .mx-auto.d-block :}  

### Browser Level 

To block ads at **Browser level**, I use [uBlock Origin](https://ublockorigin.com/).

- Add the extension to your browser.
- Enable all the filter list present in uBlock Origin.

![uBlock Dashboard](/assets/img/adblock/ublock-dashboard.png){: .mx-auto.d-block :}

Live a happy online life!