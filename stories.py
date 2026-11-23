"""The thirty-eight stories of Monday, 23 November 2026.

The page follows the winning pattern of the 19 November edition: three
big illustrated leads, ten medium grid stories, twenty-five one-line
briefs, a UTC strip, a region-count bar, a world map and a DATE CHECK
footer. Every story carries the source it traces to. Summaries restate
the source and never extend it; numbers survive exactly as reported.

Verification notes, 23 Nov 2026 (web research, morning):
- Houthi Rabigh claim: no casualty figure was found anywhere, so the
  brief carries no casualty claim, only the claim itself.
- Trump on Iran: the "in no rush" quote is from 19-20 Nov interviews,
  so the brief uses the fresher 21-22 Nov report instead.
- Brent: $92.29 early Monday (Reuters); down about 20% in November
  (the 21.6% figure belongs to WTI, not Brent).
- Sanchez: the debate was Thu 19 Nov, so it is replaced by the Baltic
  cargo ship, verified in the Wall Street Journal.
- Nvidia: Jensen Huang resigned, accepted 11 Nov, announced 12 Nov
  (SEC Form 8-K) — so the DATE CHECK lists it as (12 Nov).
- v5 copy fixes (blind test of v4): the three lead bodies were cut
  mid-sentence by the 3-line box, so each is shortened to end on a
  full stop; #6 headline now says "hit" to match "it capsized";
  #13 keeps "AQI 538" inside the 2-line box.
"""

MASTHEAD = "THE WORLD HERALD"
DATELINE = "Monday, 23 November 2026"
KICKER_LEFT = "THE WORLD ON ONE PAGE"
KICKER_RIGHT = "38 STORIES \u00b7 7 REGIONS \u00b7 10 FIELDS"
SUBTITLE = ("Tankers burn in Hormuz \u00b7 COP31 collapses \u00b7 "
            "Drone hits Kyiv block")
FOOTLINE = ("Sources: AP, Reuters, Al Jazeera, BBC, AFP, UN News, "
            "ESA\u00b7JAXA, FIFA, IQAir\u00b7Dawn \u2014 as cited per story.")

UTC_STRIP = [
    ("OVERNIGHT", "Taiwan bans short sales below Friday's close"),
    ("EARLY", "Houthis claim Rabigh refinery hit"),
    ("MORNING", "Poland confirms fallen objects were Russian missiles"),
    ("MIDDAY", "Reuters: 24 killed in Cikande factory blaze"),
    ("AFTERNOON", "S. Korea's education minister quits"),
    ("EVENING", "Asian markets open on alert after Friday's rout"),
]

# Region counts, in bar order; they must add up to 38.
REGIONS = [
    ("ASIA", 10),
    ("MIDDLE EAST", 3),
    ("EUROPE", 10),
    ("AFRICA", 4),
    ("AMERICAS", 5),
    ("OCEANIA", 1),
    ("GLOBAL", 5),
]

LEADS = [
    {
        "num": 1,
        "kicker": "STRAIT OF HORMUZ \u2014 GULF ESCALATION",
        "headline": "TANKERS BURN IN THE STRAIT OF HORMUZ",
        "body": (
            "Three tankers were struck on Friday and Saturday; two more "
            "caught fire on Sunday after hitting mines. Iran sent drones "
            "at US bases in Kuwait and Bahrain."
        ),
        "source": "AP \u00b7 Reuters \u00b7 Al Jazeera",
        "art": "tanker",
    },
    {
        "num": 2,
        "kicker": "CLIMATE \u2014 ANTALYA",
        "headline": "COP31 COLLAPSES OVER FOSSIL FUELS",
        "body": (
            "The climate talks in Antalya collapsed after record overtime, "
            "deadlocked over fossil fuels. Saudi Arabia led the refusal of "
            "fossil-fuel language."
        ),
        "source": "Reuters \u00b7 AP",
        "art": "cop",
    },
    {
        "num": 3,
        "kicker": "UKRAINE \u2014 KYIV REGION",
        "headline": "DRONE HITS BLOCK, 11 MISSING",
        "body": (
            "A Russian drone hit a five-storey block in Dymer, north of Kyiv, "
            "early on Sunday. Two were killed and eleven are missing, two of "
            "them children."
        ),
        "source": "Al Jazeera \u00b7 AP",
        "art": "block",
    },
]

GRID = [
    {
        "num": 4,
        "kicker": "POLAND \u2014 NATO TO MEET",
        "headline": "Fallen objects were Russian missiles",
        "body": (
            "Three objects that fell in the south-east were Russian missiles."
        ),
        "source": "Reuters",
        "art": "missile",
    },
    {
        "num": 5,
        "kicker": "MARKETS \u2014 FRIDAY SLUMP",
        "headline": "Stocks plunge, Asia on alert",
        "body": (
            "S&P \u22123.7%, Nasdaq \u22125.3% on Friday; Taiwan \u221217.5% "
            "in a week."
        ),
        "source": "Market reports",
        "art": "chart",
    },
    {
        "num": 6,
        "kicker": "LIBYA \u2014 BENGHAZI",
        "headline": "Sea drones hit Russian warship",
        "body": (
            "Sea drones hit the corvette Merkury at Benghazi; it capsized."
        ),
        "source": "AP \u00b7 Reuters",
        "art": "ship",
    },
    {
        "num": 7,
        "kicker": "MEXICO \u2014 SINALOA",
        "headline": "Cartel boss Chapo Isidro captured",
        "body": (
            "FBI most-wanted Fausto Isidro Meza-Flores seized in Guasave."
        ),
        "source": "AP \u00b7 Reuters",
        "art": "badge",
    },
    {
        "num": 8,
        "kicker": "INDONESIA \u2014 CIKANDE",
        "headline": "24 killed in factory blaze",
        "body": (
            "Fire at a candy factory in Cikande killed 24 on Monday; 30 missing."
        ),
        "source": "Reuters",
        "art": "factory",
    },
    {
        "num": 9,
        "kicker": "SOUTH KOREA \u2014 EXAM CHAOS",
        "headline": "Education minister quits",
        "body": (
            "Choi Kyo-jin resigned on Sunday over chaos from AI exam rules."
        ),
        "source": "Reuters",
        "art": "school",
    },
    {
        "num": 10,
        "kicker": "GENEVA \u2014 128 STATES",
        "headline": "128 states back killer-robot rules",
        "body": (
            "128 states agreed in Geneva to draft killer-robot rules by 2028."
        ),
        "source": "UN News \u00b7 Reuters",
        "art": "globe",
    },
    {
        "num": 11,
        "kicker": "FOOTBALL \u2014 2035",
        "headline": "UK to host 2035 Women's World Cup",
        "body": (
            "FIFA confirms the UK will host the 2035 Women's World Cup."
        ),
        "source": "FIFA",
        "art": "trophy",
    },
    {
        "num": 12,
        "kicker": "SPACE \u2014 MERCURY",
        "headline": "BepiColombo enters Mercury orbit",
        "body": (
            "The European-Japanese probe entered Mercury orbit on 21 Nov."
        ),
        "source": "ESA \u00b7 JAXA",
        "art": "mercury",
    },
    {
        "num": 13,
        "kicker": "POLLUTION \u2014 LAHORE",
        "headline": "Lahore world's most polluted",
        "body": (
            "Lahore was the world's most polluted city on Sunday: AQI 538."
        ),
        "source": "IQAir \u00b7 Dawn",
        "art": "smog",
    },
]

BRIEFS = [
    ("14", "Manipur: 11 dead, 180+ in hospital",
     "Reuters"),
    ("15", "Nigeria: funeral boat capsizes, 24+ dead",
     "AP"),
    ("16", "Sudan: drones hit Khartoum, 4 killed",
     "Al Jazeera"),
    ("17", "West Bank: settlers burn 12 vehicles",
     "Reuters"),
    ("18", "Houthis claim Rabigh refinery hit",
     "Reuters"),
    ("19", "US\u2013Canada: Hegseth memo curbs defence ties",
     "WaPo"),
    ("20", "Malaysia: Selangor floods displace 1,884",
     "Reports"),
    ("21", "Slovakia: Fico refuses new \u20ac45bn EU loan",
     "Reports"),
    ("22", "UN: Nusseibeh's bid 'blocked' by 3 powers",
     "Guardian"),
    ("23", "Japan: Shuri Castle's rebuilt hall opens",
     "Reports"),
    ("24", "MotoGP: Marquez seals 8th title in Portugal",
     "Reuters"),
    ("25", "Tennis: Alcaraz beats Zverev for first ATP title",
     "ATP"),
    ("26", "Football: Liverpool thrash 10-man Man Utd 4-0",
     "Reuters"),
    ("27", "Golf: Thitikul wins third straight LPGA finale",
     "AP"),
    ("28", "India: foreign investors buy record $13bn",
     "Reuters"),
    ("29", "S. Korea: finance chief sees solid growth",
     "Reuters"),
    # v8: #30 rewritten ("weighs margin-ratio cut" -> "eyes margin
    # cut") so the whole line fits at 11 pt in the 317 px column
    # (measured 286.1 px vs 297.9 px available) with no ellipsis;
    # the source stays in the data for validate(), as with the
    # other briefs (fit_brief renders briefs without the tag).
    ("30", "Taiwan: FSC eyes margin cut to 120%",
     "Bloomberg"),
    ("31", "US: Democrats reach 258 House seats",
     "AP"),
    ("32", "US: Trump said to favour squeezing Iran's oil",
     "Reports"),
    ("33", "Cricket: India close in on win in Wellington",
     "AFP"),
    ("34", "Chess: Sindarov to open with White vs Gukesh",
     "Chess.com"),
    ("35", "Nikkei \u22125.1%, gold \u22124.6%, silver \u22127.3% Fri",
     "Market data"),
    ("36", "Oil: Brent $92.3, down about 20% in November",
     "Reuters"),
    ("37", "Baltic: Russian cargo ship hit by drones",
     "WSJ"),
    ("38", "Nigeria: central bank opens final rate meeting",
     "Reports"),
]

DATE_CHECK_LEFT_OUT = (
    "Nvidia chief steps down (12 Nov) \u00b7 Trump\u2013Xi\u2013Putin summit, "
    "Shenzhen (19 Nov) \u00b7 ICJ Myanmar genocide ruling (19 Nov) \u00b7 "
    "GTA VI launch (19 Nov) \u00b7 Anthropic Nasdaq debut (19 Nov)"
)
DATE_CHECK_NOT_YET = "COP31 follow-up talks \u00b7 Akvan landfall aftermath"


def validate():
    """Every story on the page must name the source it traces to."""
    assert len(LEADS) == 3, "the page carries exactly three leads"
    assert len(GRID) == 10, "the page carries exactly ten grid stories"
    assert len(BRIEFS) == 25, "the page carries exactly twenty-five briefs"
    total = len(LEADS) + len(GRID) + len(BRIEFS)
    assert total == 38, "the page carries exactly thirty-eight stories"
    assert sum(count for _, count in REGIONS) == 38, (
        "the region bar must add up to 38")
    assert len(UTC_STRIP) == 6, "the UTC strip carries six slots"
    for story in LEADS + GRID:
        assert story["source"], "a story without a source is refused"
        assert story["headline"] and story["body"]
    for _, text, source in BRIEFS:
        assert text and source, "a brief without text or source is refused"
    return total
