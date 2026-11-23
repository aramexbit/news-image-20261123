"""The nine stories of Monday, 23 November 2026, as reported that morning.

Every story carries the source it traces to. Summaries restate the source
and never extend it; numbers survive exactly as reported.
"""

MASTHEAD = "THE WORLD HERALD"
DATELINE = "MONDAY, 23 NOVEMBER 2026  \u2014  THE WORLD IN ONE PAGE"
FOOTLINE = ("THE WORLD HERALD  \u00b7  Monday, 23 November 2026  \u00b7  "
            "Every story as reported on 23 November 2026")

LEAD = {
    "kicker": "STRAIT OF HORMUZ \u2014 GULF ESCALATION",
    "headline": "TANKERS BURN IN THE\nSTRAIT OF HORMUZ",
    "body": (
        "At least three tankers were struck in and near the Strait of Hormuz "
        "on Friday and Saturday, and two more caught fire on Sunday after "
        "hitting naval mines. Iran also sent drones at the US base of Ali Al "
        "Salem in Kuwait and at bases in Bahrain; both countries said their "
        "defences intercepted the drones, and two people were hurt in Bahrain."
    ),
    "source": "AP \u00b7 Reuters \u00b7 Al Jazeera",
    "image": "media-generation-hero-hormuz-0-cac3b021-4860-4e4b-a12b-bb39b02e4790.webp",
}

COLUMNS = [
    {
        "kicker": "CLIMATE \u2014 ANTALYA",
        "headline": "COP31 Ends With No Deal",
        "body": (
            "The UN climate talks in Antalya collapsed after record overtime, "
            "deadlocked over fossil fuels."
        ),
        "source": "Reuters",
        "image": "media-generation-col-cop31-0-6c002f0b-85b8-42ea-a2fe-c0f38e743c98.webp",
    },
    {
        "kicker": "UKRAINE \u2014 KYIV REGION",
        "headline": "Drone Hits Block; 11 Missing",
        "body": (
            "A Russian drone hit a five-storey block in Dymer, north of Kyiv, "
            "early on Sunday. Two were killed; eleven are missing, two of them "
            "children."
        ),
        "source": "Al Jazeera \u00b7 AP",
        "image": "media-generation-col-ukraine-0-0ac3371c-9a80-41de-967a-01a39226693f.webp",
    },
    {
        "kicker": "POLAND \u2014 NATO TO MEET",
        "headline": "Fallen Objects Were Russian Missiles",
        "body": (
            "Poland confirmed that three objects which fell in the south-east "
            "were Russian cruise missiles. NATO is to meet over the incident."
        ),
        "source": "Reuters \u00b7 Polish authorities",
        "image": "media-generation-col-poland-0-83efb8d3-c325-4874-b8ae-5932366fb585.webp",
    },
    {
        "kicker": "MARKETS \u2014 FRIDAY SLUMP",
        "headline": "Stocks Plunge; Asia on Alert",
        "body": (
            "US stocks fell sharply on Friday \u2014 the S&P 500 down 3.7% and "
            "the Nasdaq down 5.3%. Asian markets stayed on alert today."
        ),
        "source": "Market reports",
        "chart": True,
    },
]

FOOTER = [
    {
        "lead": "MERCURY",
        "text": "BepiColombo entered Mercury orbit \u2014 only the second mission ever.",
        "source": "ESA \u00b7 JAXA",
    },
    {
        "lead": "FOOTBALL",
        "text": "The UK is to host the 2035 Women\u2019s World Cup, the first in Britain since 1966.",
        "source": "FIFA",
    },
    {
        "lead": "POLLUTION",
        "text": "Lahore was the world\u2019s most polluted city on Sunday, its air quality index at 538.",
        "source": "IQAir \u00b7 Dawn",
    },
    {
        "lead": "INDONESIA",
        "text": "24 body bags recovered from the Cikande candy factory fire; dozens missing.",
        "source": "Local reports",
    },
]


def validate():
    """Every story on the page must name the source it traces to."""
    assert LEAD["source"] and LEAD["body"] and LEAD["headline"]
    assert len(COLUMNS) == 4, "the page carries exactly four column stories"
    assert len(FOOTER) == 4, "the footer carries exactly four briefs"
    for story in COLUMNS + FOOTER:
        assert story["source"], "a story without a source is refused"
        assert story["text" if "text" in story else "body"]
    return 1 + len(COLUMNS) + len(FOOTER)
