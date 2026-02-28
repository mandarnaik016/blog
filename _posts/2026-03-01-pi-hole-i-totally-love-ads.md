---
layout: post
title: Pi-hole - I Totally Love Ads
subtitle: Reclaiming The Internet.
cover-img: /assets/img/misc/poster-wall.jpg
thumbnail-img: ""
tags: [privacy, security]
---
Once upon a time, when I was a king, there was no internet, no websites — just a simple world. Over the years, information technology has evolved, connecting people across the globe. The internet began to rule the digital age, and then, eventually, Ads took over.

Until Ad-blockers arrived!.

In this post, we will set up [Pi-hole](https://pi-hole.net/), a DNS-level ad-blocker that blocks domains that serve ads and trackers, thereby enhancing network security.

## Ingredient

To cook we need the following,

- Raspberry Pi Zero 2 W
	+ Cost ~1800 INR
- Raspberry Pi Case
  + Cost ~300 INR
- DietPi
- microSDXC
  + Took from sibling.

## Installation

We flash our SD card with DietPi OS, then set up [Wi-Fi](https://kenilt.wordpress.com/2025/07/31/how-to-install-dietpi-on-a-raspberry-pi-step-by-step-guide/). 

{: .box-note}
**Note**: Set a static IP to Raspberry Pi to maintain consistency in the network.

Use `dietpi-software`, to install Pi-hole seamlessly.

{%  include lazyimg.html
    img_src="../assets/img/misc/pihole/lowly/dietpi-software-pihole.png"
    img_datasrc="../assets/img/misc/pihole/dietpi-software-pihole.png"
    img_caption="Figure 1: DietPi software - Pi-hole"
    img_alt="DietPi software - Pi-hole"
%}

Let's check the Pi-hole version to confirm installation.

{%  include lazyimg.html
    img_src="../assets/img/misc/pihole/lowly/pihole-version.png"
    img_datasrc="../assets/img/misc/pihole/pihole-version.png"
    img_caption="Figure 2: DietPi version"
    img_alt="DietPi version"
%}

We also install [Unbound](https://nlnetlabs.nl/projects/unbound/about/) for validating and caching DNS entries.

{%  include lazyimg.html
    img_src="../assets/img/misc/pihole/lowly/dietpi-software-unbound.png"
    img_datasrc="../assets/img/misc/pihole/dietpi-software-unbound.png"
    img_caption="Figure 3: DietPi software - Unbound"
    img_alt="DietPi software - Unbound"
%}

Another version check to confirm Unbound installation.

{%  include lazyimg.html
    img_src="../assets/img/misc/pihole/lowly/unbound-version.png"
    img_datasrc="../assets/img/misc/pihole/unbound-version.png"
    img_caption="Figure 4: Unbound version"
    img_alt="Unbound version"
%}

## Customization

We add Unbound as **Custom DNS servers** and uncheck any Upstream DNS Servers.

{%  include lazyimg.html
    img_src="../assets/img/misc/pihole/lowly/unbound-as-dns-server.png"
    img_datasrc="../assets/img/misc/pihole/unbound-as-dns-server.png"
    img_caption="Figure 5: Unbound as DNS server"
    img_alt="Unbound as DNS server"
%}

The default list is [StevenBlack](https://github.com/StevenBlack/hosts), I personally use the following list for more extensive coverage.

```
https://someonewhocares.org/hosts/zero/
https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts;showintro=0
https://hosts.anudeep.me/mirror/adservers.txt
https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt
https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt
```

At last, add a whitelist just to be on a safer side.

```
https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt
```

Since the list contains only static domains, it becomes insufficient for newly generated domains. Using regex enables us to dynamically address this limitation.

I use the below Regex deny,
```
^ad([sxv]?[0-9]*|system)[_.-]([^.[:space:]]+\.){1,}|[_.-]ad([sxv]?[0-9]*|system)[_.-]
^(.+[_.-])?adse?rv(er?|ice)?s?[0-9]*[_.-]
^(.+[_.-])?telemetry[_.-]
^adim(age|g)s?[0-9]*[_.-]
^adtrack(er|ing)?[0-9]*[_.-]
^advert(s|is(ing|ements?))?[0-9]*[_.-]
^aff(iliat(es?|ion))?[_.-]
^analytics?[_.-]
^banners?[_.-]
^beacons?[0-9]*[_.-]
^count(ers?)?[0-9]*[_.-]
^mads\.
^pixels?[-.]
^stat(s|istics)?[0-9]*[_.-]
(.*\.|^)((think)?with)?google($|((adservices|apis|mail|static|syndication|tagmanager|tagservices|usercontent|zip|-analytics)($|\..+)))
(.*\.|^)g(gpht|mail|static|v(t[12])?)($|\..+)
(.*\.|^)chrom(e(experiments)?|ium)($|\..+)
(.*\.|^)ampproject($|\..+)
(.*\.|^)doubleclick($|\..+)
(.*\.|^)firebaseio($|\..+)
(.*\.|^)googlevideo($|\..+)
(.*\.|^)waze($|\..+)
(.*\.|^)y(outube|timg)($|\..+)
```

## Configuration

For convenience, the router’s DNS server can be changed to the Pi-hole IP address so that every device connected to the router uses Pi-hole by default.

{%  include lazyimg.html
    img_src="../assets/img/misc/pihole/lowly/router-dns.png"
    img_datasrc="../assets/img/misc/pihole/router-dns.png"
    img_caption="Figure 6: Router DNS"
    img_alt="Router DNS"
%}

If the router's DNS address cannot be changed, manually configure the DNS servers on each device.

## Result

The statistics for Pi-hole in the home network with the same set of lists and regex deny rules.

{%  include lazyimg.html
    img_src="../assets/img/misc/pihole/lowly/pihole-stats.png"
    img_datasrc="../assets/img/misc/pihole/pihole-stats.png"
    img_caption="Figure 7: Pi-hole stats"
    img_alt="Pi-hole stats"
%}

On average, nearly 5K out of 17K queries are **blocked**!.

Additionally, Unbound’s DNS caching significantly improves response time and overall DNS performance.

{%  include lazyimg.html
    img_src="../assets/img/misc/pihole/lowly/unbound-stats.png"
    img_datasrc="../assets/img/misc/pihole/unbound-stats.png"
    img_caption="Figure 8: Unbound stats"
    img_alt="Unbound stats"
%}

Thank you. We meet next time to make security better. Until then, وداعا وداعا!.
