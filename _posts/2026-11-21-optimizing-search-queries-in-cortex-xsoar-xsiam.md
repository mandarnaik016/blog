---
layout: post
title: Optimizing Search Queries in Cortex XSOAR/XSIAM
subtitle: Automating * Except Bad Search Queries.
cover-img: /assets/img/analysis/analysis.webp
thumbnail-img: ""
tags: [security, cortex, xsoar, xsiam]
---

* TOC
{:toc}

## INTRODUCTION

In this article, we'll walk through optimizing search queries in Cortex XSOAR/XSIAM.

In an enterprise environment, a significant portion of operations relies on searching incidents and indicators to perform various tasks.

Whether it's searching for similar incidents based on specific queries and retrieving their IDs to link them to the current incident, or filtering indicators that have already been blocked, these use cases often involve working with large volumes of data.

For example, consider receiving a large set of indicators as part of a Security Advisory or Red Team exercise. Searching through these indicators one by one to check for a particular tag is an exhaustive approach and can take an unreasonable amount of time.

## METHODOLOGY

We collect the input data, which consists of a list of indicators (usually populated through `!extractIndicators`) and the tag we want to search for. In my case, I've tagged a few random indicators with the tag `blocked`.

```python
args: dict = demisto.args()
value: list = argToList(args["value"])
tag: str = args["tag"]
```

Since XSOAR allows us to group multiple clauses within a single field, for example, `value:("1.1.1.1" "8.8.8.8")`, we can search for all the IOCs in a single query, as shown below.

![Single search](../assets/img/cortex/single-search.png)

However, this approach works well when the number of indicators ranges from 0 to 100. Once the volume exceeds that range, it is no longer an efficient or practical approach. 

We'll stick to a reasonable batch size of 50. The `create_chunk()` function splits a large list into smaller batches, each containing up to 50 indicators.

```python
BATCH_SIZE: int = 50

def create_chunk(items: list) -> Iterator[list[str]]:
    """Create chunks of indicators

    Args:
        items (list): List of indicators

    Yields:
        Iterator[list[str]]: Chunked indicators list.
    """
    for i in range(0, len(items), BATCH_SIZE):
        yield items[i : i + BATCH_SIZE]
```

This is a classic example of *batch-based processing*.

Next, we define a function called `find_untagged()`, which takes two inputs: a list of indicators and the tag to search for. It returns a list of indicators that do not have the specified tag (in this case, `blocked`).

```python
def find_untagged(value: list, tag: str) -> list:
    """Return indicators to be blocked.

    Args:
        value (list): List of indicators
        tag (str): Indicator tag

    Returns:
        list: List of indicators
    """
    to_block: list = []
    for chunk in create_chunk(value):
        search_term = " ".join(f'"{ioc}"' for ioc in chunk)
        query = f'value:({search_term}) and -tags:"{tag}"'
        res: dict = demisto.searchIndicators(
            query=query, size=len(chunk), populateFields="value"
        )
        if not res["iocs"]:
            continue
        untagged: list = demisto.dt(res, "iocs.value")
        to_block.extend(untagged)
    return to_block
```

In case you haven't noticed, we retrieved only the `value`  column while performing the search. This is another important concept: *data minimization*.

The concept is quite simple: less data means less computation and processing, resulting in faster execution and quicker results. 

The response contains the output length of **50035** when the `populateFields` argument in `searchIndicators()` is not set.

![Default retrival](../assets/img/cortex/default-retrival.png)

The response is almost halved when we selectively retrieve only the `value` field. This reduces the output length to **23035**, eliminating unnecessary data.

![Selective retrival](../assets/img/cortex/selective-retrival.png)

In addition to selective field retrieval, we also limit the size in `searchIndicators()` to the length of the current chunk.

<details markdown="1">
<summary>NOTE:</summary>
If you're considering pagination here, keep in mind that it may increase execution time and computational overhead. Pagination is more effective when scraping data rather than filtering indicators based on specific criteria.
</details>

## PROFILING

For a sample ~3000 indicators, around 100 of which are already tagged.

| Function         | Call | Time (s) |
| ---------------- | ---- | -------- |
| find_untagged    | 1    | 3.65     |
| create_chunk     | 61   | 0.00035  |
| searchIndicators | 60   | 7.9      |
| dt               | 60   | 0.74     |

## RESULT

As expected, the script populated the output with only unblocked indicators, excluding those that were already tagged as `blocked`. The complete script can be found at [FindUntagged](https://gist.github.com/mandarnaik016/ac365583d1e9a8f42ce56332fdc914c6#file-finduntagged-py)

![Result](../assets/img/cortex/result-warroom.png)

Thank you for making it this far! See you next time. Until then, sayonara!