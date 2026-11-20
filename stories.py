# stories.py — data berita Kamis 19 November 2026 untuk poster R3.
# Semua entri ditulis dengan kata-kata sendiri dari fakta spec.
# Struktur: list of dict, bukan tuple.

FEATURES = [
    {
        "kicker": "SHENZHEN · SUMMIT",
        "headline": "Trump, Xi and Putin hold first three-way summit",
        "body": "At APEC in Shenzhen, the three leaders issue a 'Declaration on Peace' on nuclear risk.",
        "source": "Reuters · AP · Xinhua",
        "place": "Shenzhen",
        "art": "summit",
        "accent": "#B03A2E",
    },
    {
        "kicker": "THE HAGUE · JUSTICE",
        "headline": "World Court: Myanmar committed genocide",
        "body": "The ICJ rules 9–6: Myanmar is guilty of genocide against the Rohingya; reparations ordered.",
        "source": "Al Jazeera · UN News",
        "place": "The Hague",
        "art": "court",
        "accent": "#1F4E79",
    },
    {
        "kicker": "ANTALYA · CLIMATE",
        "headline": "COP31 draft drops fossil fuels and $120bn aid goal",
        "body": "The slim draft text cuts the adaptation aid target; talks are due to end on Friday.",
        "source": "Reuters · AFP",
        "place": "Antalya",
        "art": "climate",
        "accent": "#1E7A4C",
    },
]

TILES = [
    {
        "kicker": "CRIMEA · WAR",
        "headline": "Ukraine hits Crimea bridge again",
        "body": "Third strike in a week halts trains.",
        "source": "Euronews",
        "place": "Crimea",
        "art": "bridge",
        "accent": "#7A3E1E",
    },
    {
        "kicker": "RIYADH · WAR",
        "headline": "Saudis shoot down Houthi missiles",
        "body": "Debris falls on the capital; none hurt.",
        "source": "Reuters",
        "place": "Riyadh",
        "art": "missile",
        "accent": "#8A2B2B",
    },
    {
        "kicker": "ODISHA · STORM",
        "headline": "Cyclone Akvan nears India's coast",
        "body": "100,000+ evacuated before landfall.",
        "source": "IMD",
        "place": "Odisha",
        "art": "cyclone",
        "accent": "#2E6E8E",
    },
    {
        "kicker": "SEOUL · JUSTICE",
        "headline": "Korea's top court clears ex-PM Han",
        "body": "Han Duck-soo's conviction overturned.",
        "source": "AP",
        "place": "Seoul",
        "art": "gavel",
        "accent": "#4A4A8A",
    },
    {
        "kicker": "GREENLAND · SECURITY",
        "headline": "Denmark backs Arctic pact with US",
        "body": "Parliament approves the deal 109–0.",
        "source": "AP",
        "place": "Greenland",
        "art": "glacier",
        "accent": "#2E7A8E",
    },
    {
        "kicker": "NEW YORK · MARKETS",
        "headline": "Anthropic starts trading on Nasdaq",
        "body": "Record $81bn sale was priced at $83.",
        "source": "AP",
        "place": "New York",
        "art": "chart",
        "accent": "#1E6B3A",
    },
    {
        "kicker": "WORLDWIDE · GAMES",
        "headline": "GTA VI goes on sale after 13 years",
        "body": "The midnight launch draws rave reviews.",
        "source": "ABC",
        "place": "Vice City",
        "art": "game",
        "accent": "#6A2E8E",
    },
    {
        "kicker": "BOGOTÁ · LABOUR",
        "headline": "Colombia's unions hold national strike",
        "body": "Marches in three cities against reforms.",
        "source": "Infobae",
        "place": "Bogotá",
        "art": "strike",
        "accent": "#8E6E1E",
    },
]

# Ubin ke-9 dan ke-10 dipakai sebagai cadangan bila grid diperluas; tidak
# dirender di layout R3 (grid 2x4 memakai 8 ubin pertama).
TILES_EXTRA = [
    {
        "kicker": "NAIROBI · SPORT",
        "headline": "Marathon champion banned for doping",
        "body": "Kenya's Peres Jepchirchir gets three years.",
        "source": "ABC",
        "place": "Nairobi",
        "art": "runner",
        "accent": "#8E2E5A",
    },
]

BRIEFS = [
    {"num": 12, "place": "Gaza", "text": "Israeli tanks cross the Yellow Line; Hamas calls it a truce breach.", "source": "AP"},
    {"num": 13, "place": "London", "text": "Van Gogh sells for record $190.4m amid Nazi-history row.", "source": "ABC"},
    {"num": 14, "place": "Mexico City", "text": "Banxico cuts rates to 6.25% on a 3–2 vote.", "source": "Banxico"},
    {"num": 15, "place": "Canberra", "text": "Three killed and four groups hit by fresh sanctions over West Bank settlers.", "source": "ABC"},
    {"num": 16, "place": "Mogadishu", "text": "Somalia accuses the UAE of secret military bases on its soil.", "source": "Mogadishu"},
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
    {"value": "3", "label": "presidents at one table", "color": "#1F4E79"},
    {"value": "9–6", "label": "World Court genocide vote", "color": "#1E7A4C"},
    {"value": "$120bn", "label": "aid goal cut at COP31", "color": "#B03A2E"},
    {"value": "$81bn", "label": "Anthropic's record IPO", "color": "#6A2E8E"},
    {"value": "109–0", "label": "Danish vote on Arctic pact", "color": "#C25E10"},
    {"value": "4.9%", "label": "Australian jobless rate", "color": "#0E7A7A"},
]

REGIONS = ["ASIA 3", "MIDDLE EAST 2", "EUROPE 6", "AFRICA 4", "AMERICAS 6", "OCEANIA 2", "GLOBAL 2"]

LEFT_OUT = [
    "18 NOV: EU's €45bn Ukraine loan plan",
    "18 NOV: Iran fires on Kuwait and Bahrain",
    "18 NOV: Nvidia results",
    "18 NOV: Jeffries named for US speaker",
    "18 NOV: Voyager 1 crosses one light-day",
    "20 NOV: COP31's scheduled close",
    "20 NOV: Cyclone Akvan's landfall",
]

ATTRIBUTION = (
    "Every story here happened, or was first reported, on Thursday 19 November 2026. "
    "Sources: Reuters, AP, AFP, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature."
)
