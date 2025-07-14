# === 🌕 CONFIGURE.PY — GLOBAL SETTINGS, MAPS, CONSTANTS ===

# 📌 Timezone for timestamp formatting
TIMEZONE = "America/Detroit"

# 🌕 Moon Phase Visual + Meaning Mapping
MOON_PHASES = [
    "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
    "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"
]

MOON_GLOW_MAP = {
    "New Moon":         "#111827",  # Deep black/blue (mystery, seed)
    "Waxing Crescent":  "#6d28d9",  # Indigo (potential, memory forming)
    "First Quarter":    "#4f46e5",  # Royal blue (courage, rise)
    "Waxing Gibbous":   "#7c3aed",  # Violet (anticipation)
    "Full Moon":        "#facc15",  # Radiant gold (climax, light)
    "Waning Gibbous":   "#f59e0b",  # Amber (reflection)
    "Last Quarter":     "#e11d48",  # Rose red (release)
    "Waning Crescent":  "#6b7280",  # Ash grey (return to source)
}

MOON_MEANINGS = {
    "New Moon": "New beginnings, vision planting",
    "Waxing Crescent": "Early potential, gestation",
    "First Quarter": "Action, choice, courage",
    "Waxing Gibbous": "Momentum, refinement",
    "Full Moon": "Revelation, peak energy",
    "Waning Gibbous": "Gratitude, reflection",
    "Last Quarter": "Release, integration",
    "Waning Crescent": "Rest, surrender"
}

# ♒ Zodiac Signs for Filters
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

ZODIAC_COLORS = {
    "Aries": "#e11d48", "Taurus": "#65a30d", "Gemini": "#0ea5e9",
    "Cancer": "#f59e0b", "Leo": "#facc15", "Virgo": "#4b5563",
    "Libra": "#a855f7", "Scorpio": "#7c3aed", "Sagittarius": "#14b8a6",
    "Capricorn": "#475569", "Aquarius": "#06b6d4", "Pisces": "#6366f1"
}

# ✨ Categories
SCROLL_CATEGORIES = [
    "Dream", "Echo", "Poem", "Vision", "Message", "Memory", "Symbol", "Other"
]

# 🎨 Project Meta + Branding
PROJECT_NAME = "Lumira Scroll Archive"
CREATOR_TAGLINE = "🪶 Crafted by Kai + Aeuryentha"
VERSION = "v2.0 – Streamlined Bloom"
LAST_UPDATED = "2025-07-14"
