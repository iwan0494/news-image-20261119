# stories.py — data berita Kamis 19 November 2026 (ronde 4).
# Semua fakta ditulis dengan kata-kata builder dari spec; struktur data
# (list of dict) dipilih sendiri. Penomoran cerita 1-25 tanpa lompat:
# FEATURES 1-3, TILES 4-11, BRIEFS 12-25.

FEATURES = [
    {
        "num": 1,
        "place": "SHENZHEN",
        "kicker": "SUMMIT",
        "headline": "Trump, Xi and Putin hold first three-way summit",
        "body": "Leaders of the US, China and Russia meet at APEC Shenzhen; a "
                "'Declaration on Peace' covers nuclear risk and UN reform.",
        "source": "Reuters, AP, Xinhua",
        "art": "summit",
    },
    {
        "num": 2,
        "place": "THE HAGUE",
        "kicker": "JUSTICE",
        "headline": "World Court: Myanmar committed genocide",
        "body": "The ICJ rules 9-6 that Myanmar is guilty of genocide against "
                "the Rohingya and orders reparations.",
        "source": "Al Jazeera, UN News",
        "art": "court",
    },
    {
        "num": 3,
        "place": "ANTALYA",
        "kicker": "CLIMATE",
        "headline": "COP31 draft drops fossil fuels and $120bn aid goal",
        "body": "The COP31 draft cuts fossil fuels and slashes the $120 billion "
                "adaptation aid target; talks end Friday.",
        "source": "Reuters, AFP",
        "art": "climate",
    },
]

TILES = [
    {
        "num": 4,
        "place": "CRIMEA",
        "kicker": "WAR",
        "headline": "Ukraine hits Crimea bridge again",
        "body": "Third attack in a week halts rail to Russia.",
        "source": "Euronews",
        "art": "bridge",
    },
    {
        "num": 5,
        "place": "RIYADH",
        "kicker": "WAR",
        "headline": "Saudis shoot down Houthi missiles",
        "body": "Debris falls on the capital; no casualties.",
        "source": "Reuters",
        "art": "missile",
    },
    {
        "num": 6,
        "place": "ODISHA",
        "kicker": "STORM",
        "headline": "Cyclone Akvan nears India's coast",
        "body": "100,000 evacuated ahead of Friday landfall.",
        "source": "IMD",
        "art": "storm",
    },
    {
        "num": 7,
        "place": "SEOUL",
        "kicker": "JUSTICE",
        "headline": "Korea's top court clears ex-PM Han",
        "body": "Martial-law verdict on ex-PM Han void.",
        "source": "AP",
        "art": "court",
    },
    {
        "num": 8,
        "place": "GREENLAND",
        "kicker": "SECURITY",
        "headline": "Denmark backs Arctic pact with US",
        "body": "Parliament backs Greenland pact 109-0.",
        "source": "AP",
        "art": "ice",
    },
    {
        "num": 9,
        "place": "NEW YORK",
        "kicker": "MARKETS",
        "headline": "Anthropic starts trading on Nasdaq",
        "body": "Record $81bn IPO, priced at $83 a share.",
        "source": "AP",
        "art": "chart",
    },
    {
        "num": 10,
        "place": "WORLDWIDE",
        "kicker": "GAMES",
        "headline": "GTA VI goes on sale after 13 years",
        "body": "Midnight launch draws praise.",
        "source": "ABC",
        "art": "game",
    },
    {
        "num": 11,
        "place": "BOGOTA",
        "kicker": "LABOUR",
        "headline": "Colombia's unions hold national strike",
        "body": "Marches in three cities oppose reform.",
        "source": "Infobae",
        "art": "march",
    },
]

BRIEFS = [
    {"num": 12, "place": "Gaza", "text": "Israeli tanks cross the Yellow Line; Hamas calls it a truce breach.", "source": "AP"},
    {"num": 13, "place": "London", "text": "Van Gogh sells for a record $190.4m despite its Nazi history.", "source": "ABC"},
    {"num": 14, "place": "Mexico City", "text": "Banxico cuts rates to 6.25% on a 3-2 vote.", "source": "Banxico"},
    {"num": 15, "place": "Canberra", "text": "Three killed, four groups sanctioned over West Bank settlers.", "source": "ABC"},
    {"num": 16, "place": "Mogadishu", "text": "Somalia accuses UAE of secret bases on its soil.", "source": "Mogadishu"},
    {"num": 17, "place": "Frankfurt", "text": "Deutsche Bank handled $582m in Epstein-linked deals.", "source": "FT"},
    {"num": 18, "place": "Washington", "text": "Senators warn AI cyber threats to national defences.", "source": "Washington"},
    {"num": 19, "place": "Rome", "text": "Author Corrado Augias dies at 91.", "source": "Euronews"},
    {"num": 20, "place": "Sudan", "text": "Court sentences absent RSF chief to death.", "source": "AP"},
    {"num": 21, "place": "Pretoria", "text": "Central bank holds rate at 7.25%.", "source": "SABC"},
    {"num": 22, "place": "Canaries", "text": "Record 11,000 migrants in 15 days.", "source": "Africanews"},
    {"num": 23, "place": "Florida", "text": "Floods shut Broward; Miami schools again.", "source": "CBS"},
    {"num": 24, "place": "Wellington", "text": "Court: pay equity cuts broke rights law.", "source": "RNZ"},
    {"num": 25, "place": "Space", "text": "Red giant seen eating a Sun-sized star.", "source": "Nature"},
]

STATS = [
    {"value": "3", "label": "presidents at one table", "color": (31, 119, 180)},
    {"value": "9-6", "label": "World Court genocide vote", "color": (44, 160, 44)},
    {"value": "$120bn", "label": "aid goal cut at COP31", "color": (214, 39, 40)},
    {"value": "$81bn", "label": "Anthropic's record IPO", "color": (148, 103, 189)},
    {"value": "109-0", "label": "Danish vote on Arctic pact", "color": (255, 127, 14)},
    {"value": "4.9%", "label": "Australian jobless rate", "color": (23, 190, 207)},
]

REGIONS = [
    ("ASIA", 3),
    ("MIDDLE EAST", 2),
    ("EUROPE", 6),
    ("AFRICA", 4),
    ("AMERICAS", 6),
    ("OCEANIA", 2),
    ("GLOBAL", 2),
]

LEFT_OUT = [
    "18 NOV: EU's \u20ac45bn Ukraine loan plan",
    "18 NOV: Iran fires on Kuwait and Bahrain",
    "18 NOV: Nvidia results",
    "18 NOV: Jeffries named for US speaker (251-11)",
    "18 NOV: Voyager 1 crossing one light-day, 10:16 GMT",
    "20 NOV: COP31's scheduled close",
    "20 NOV: Cyclone Akvan's landfall",
]

SUBHEAD = (
    "Trump, Xi and Putin meet in Shenzhen - the World Court rules on Myanmar - "
    "COP31 drops fossil fuels"
)
