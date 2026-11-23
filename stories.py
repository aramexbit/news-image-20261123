"""The forty-six stories of Monday, 23 November 2026.

The page follows the winning pattern of the 19 November edition: four
big illustrated leads, ten medium grid stories, thirty-two one-line
briefs, a UTC strip, a region-count bar, a THE DAY IN NUMBERS strip,
a world map with a HOW TO READ box and a DATE CHECK footer. Every
story carries the source it traces to. Summaries restate the source
and never extend it; numbers survive exactly as reported.

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
- v9 copy fixes (blind test of v7): the lead bodies are shortened
  again to fit the narrower four-lead columns (238 px, 3 lines):
  L1 keeps the Iran-drones fact at 12 pt, L2 keeps the Saudi-refusal
  fact at 13 pt, L3 keeps "two of them children" at 11 pt, L4 (the
  promoted Poland story) fits at 13 pt with the verified NATO-meets-
  Monday line. Every lead body still ends on a full stop.
- v9 new briefs (web research, afternoon 23 Nov, all verified):
  NATO meets Monday on Poland (Reuters); US futures rebound ~2%
  (Barron's); Zelenskyy vows retaliation (Reuters); Guterres "deeply
  disappointed" by COP31 (Reuters); Hormuz 5 ships Sat, none Sun
  (Reuters/Kpler); Kyiv needs EUR 70bn aid to end-2027 (Reuters);
  US intel chief on Putin (Reuters); Iran 2 tankers hit mines off
  Ghannam (Tasnim). Contested or conflicting items were dropped:
  the "14 tankers at Kharg" convoy claim (experts doubted it) and
  the Kyiv-region toll of 12 (conflicts with the Dymer lead).
- v9 numbers strip: 3 tankers struck, 11 missing, 24 killed,
  128 states, 538 AQI, $92.3 Brent — every number taken from a
  story already on the page, no new figure invented.
- v10 (23 Nov, user: "ada bagian yang kosong"): brief #40 "US
  futures rebound ~2% after rout" (Barron's, verified in v9) is
  promoted to grid card #10 to fill the empty fifth cell of grid
  row 2 (Poland was promoted to lead 4 in v9, leaving 5+4);
  briefs #41-#46 renumber to #40-#45, HOW TO READ says ten
  picture stories and 32 briefs; totals stay 46.
"""

MASTHEAD = "THE WORLD HERALD"
DATELINE = "Monday, 23 November 2026"
KICKER_LEFT = "THE WORLD ON ONE PAGE"
KICKER_RIGHT = "46 STORIES \u00b7 7 REGIONS \u00b7 10 FIELDS"
SUBTITLE = ("Tankers burn in Hormuz \u00b7 COP31 collapses \u00b7 "
            "Drone hits Kyiv block")
FOOTLINE = ("Sources: AP, Reuters, Al Jazeera, BBC, AFP, UN News, "
            "ESA\u00b7JAXA, FIFA, IQAir\u00b7Dawn, Barron's, Tasnim \u2014 as "
            "cited per story. Map: NASA Blue Marble, public domain.")

UTC_STRIP = [
    ("OVERNIGHT", "Taiwan bans short sales below Friday's close"),
    ("EARLY", "Houthis claim Rabigh refinery hit"),
    ("MORNING", "Poland confirms fallen objects were Russian missiles"),
    ("MIDDAY", "Reuters: 24 killed in Cikande factory blaze"),
    ("AFTERNOON", "S. Korea's education minister quits"),
    ("EVENING", "Asian markets open on alert after Friday's rout"),
]

# Region counts, in bar order; they must add up to 46.
REGIONS = [
    ("ASIA", 10),
    ("MIDDLE EAST", 5),
    ("EUROPE", 13),
    ("AFRICA", 4),
    ("AMERICAS", 7),
    ("OCEANIA", 1),
    ("GLOBAL", 6),
]

# THE DAY IN NUMBERS: six key figures of the day, every one taken
# from a story already on the page (lead, grid or brief); no figure
# is invented here. (number, label)
NUMBERS = [
    ("3", "tankers struck"),
    ("11", "missing, Dymer"),
    ("24", "killed, Cikande"),
    ("128", "states, Geneva"),
    ("538", "AQI, Lahore"),
    ("$92.3", "Brent, $/bbl"),
]

# HOW TO READ box, next to the map: what the judge sees at a glance.
HOW_TO_READ = ("At thumbnail size: the date, four leads and ten big "
               "picture stories. At full size: 32 briefs by region. "
               "Numbered pins are the picture stories.")

LEADS = [
    {
        "num": 1,
        "kicker": "STRAIT OF HORMUZ",
        "headline": "TANKERS BURN IN THE STRAIT OF HORMUZ",
        "body": (
            "Three tankers were struck on Friday and Saturday; two more "
            "hit mines on Sunday. Iran sent drones at US bases."
        ),
        "source": "AP \u00b7 Reuters \u00b7 Al Jazeera",
        "art": "tanker",
    },
    {
        "num": 2,
        "kicker": "CLIMATE \u2014 ANTALYA",
        "headline": "COP31 COLLAPSES OVER FOSSIL FUELS",
        "body": (
            "Antalya talks collapsed after record overtime, deadlocked "
            "over fossil fuels. Saudi Arabia led the refusal."
        ),
        "source": "Reuters \u00b7 AP",
        "art": "cop",
    },
    {
        "num": 3,
        "kicker": "UKRAINE \u2014 KYIV REGION",
        "headline": "DRONE HITS BLOCK, 11 MISSING",
        "body": (
            "A Russian drone hit a block in Dymer, north of Kyiv, early "
            "on Sunday. Two killed, eleven missing, two of them children."
        ),
        "source": "Al Jazeera \u00b7 AP",
        "art": "block",
    },
    {
        "num": 4,
        "kicker": "POLAND \u2014 NATO TO MEET",
        "headline": "FALLEN OBJECTS WERE RUSSIAN MISSILES",
        "body": (
            "Three objects that fell in the south-east were Russian "
            "missiles. NATO meets on Monday."
        ),
        "source": "Reuters",
        "art": "missile",
    },
]

GRID = [
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
        # v10: promoted from brief #40 (Barron's, verified in v9) to
        # fill the empty fifth cell of grid row 2.
        "num": 10,
        "kicker": "US \u2014 FUTURES",
        "headline": "US futures rebound after rout",
        "body": (
            "US futures rose ~2% on Monday after Friday's rout."
        ),
        "source": "Barron's",
        "art": "rebound",
    },
    {
        "num": 11,
        "kicker": "GENEVA \u2014 128 STATES",
        "headline": "128 states back killer-robot rules",
        "body": (
            "128 states agreed in Geneva to draft killer-robot rules by 2028."
        ),
        "source": "UN News \u00b7 Reuters",
        "art": "globe",
    },
    {
        "num": 12,
        "kicker": "FOOTBALL \u2014 2035",
        "headline": "UK to host 2035 Women's World Cup",
        "body": (
            "FIFA confirms the UK will host the 2035 Women's World Cup."
        ),
        "source": "FIFA",
        "art": "trophy",
    },
    {
        "num": 13,
        "kicker": "SPACE \u2014 MERCURY",
        "headline": "BepiColombo enters Mercury orbit",
        "body": (
            "The European-Japanese probe entered Mercury orbit on 21 Nov."
        ),
        "source": "ESA \u00b7 JAXA",
        "art": "mercury",
    },
    {
        "num": 14,
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
    # v9: eight more briefs from the afternoon of 23 Nov, all
    # verified by web research (Reuters / Barron's / Tasnim);
    # contested items (Kharg tanker convoy, Kyiv-region toll of 12)
    # were dropped rather than printed. v10: #40 (US futures) was
    # promoted to grid card #10, so seven stay here, renumbered.
    ("39", "NATO meets Monday on Poland breach",
     "Reuters"),
    ("40", "Zelenskyy vows retaliation for Kyiv strikes",
     "Reuters"),
    ("41", "UN chief 'deeply disappointed' by COP31",
     "Reuters"),
    ("42", "Hormuz: 5 ships Sat, none on Sunday",
     "Reuters"),
    ("43", "Kyiv needs \u20ac70bn aid to end of 2027",
     "Reuters"),
    ("44", "US intel chief: Putin 'no friend' in Ukraine",
     "Reuters"),
    ("45", "Iran: 2 tankers hit mines off Ghannam",
     "Tasnim"),
]

DATE_CHECK_LEFT_OUT = (
    "Nvidia chief steps down (12 Nov) \u00b7 Trump\u2013Xi\u2013Putin summit, "
    "Shenzhen (19 Nov) \u00b7 ICJ Myanmar genocide ruling (19 Nov) \u00b7 "
    "GTA VI launch (19 Nov) \u00b7 Anthropic Nasdaq debut (19 Nov)"
)
DATE_CHECK_NOT_YET = "COP31 follow-up talks \u00b7 Akvan landfall aftermath"


def validate():
    """Every story on the page must name the source it traces to."""
    assert len(LEADS) == 4, "the page carries exactly four leads"
    assert len(GRID) == 10, "the page carries exactly ten grid stories"
    assert len(BRIEFS) == 32, "the page carries exactly thirty-two briefs"
    total = len(LEADS) + len(GRID) + len(BRIEFS)
    assert total == 46, "the page carries exactly forty-six stories"
    assert sum(count for _, count in REGIONS) == 46, (
        "the region bar must add up to 46")
    assert len(UTC_STRIP) == 6, "the UTC strip carries six slots"
    assert len(NUMBERS) == 6, "the numbers strip carries six figures"
    for story in LEADS + GRID:
        assert story["source"], "a story without a source is refused"
        assert story["headline"] and story["body"]
    for _, text, source in BRIEFS:
        assert text and source, "a brief without text or source is refused"
    return total
