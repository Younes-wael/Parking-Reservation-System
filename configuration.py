# =========================
# Configuration
# =========================
from pathlib import Path

_HERE = Path(__file__).parent

HOTEL_NAME = "Mercure Hotel Frankfurt Airport Langen"
DB_PATH = _HERE / "parking_reservations.db"
JSON_PATH = _HERE / "data.json"

# Default capacity (sidebar can override at runtime)
DEFAULT_PARKING_SPOTS = 60
