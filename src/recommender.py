import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 1.0

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

def _genre_component(genre: str, favorite_genre: str) -> Tuple[float, Optional[str]]:
    if genre == favorite_genre:
        return GENRE_WEIGHT, f"genre match (+{GENRE_WEIGHT:.1f})"
    return 0.0, None

def _mood_component(mood: str, favorite_mood: str) -> Tuple[float, Optional[str]]:
    if mood == favorite_mood:
        return MOOD_WEIGHT, f"mood match (+{MOOD_WEIGHT:.1f})"
    return 0.0, None

def _energy_component(energy: float, target_energy: float) -> Tuple[float, str]:
    closeness = 1 - abs(energy - target_energy)
    points = ENERGY_WEIGHT * closeness
    return points, f"energy closeness (+{points:.2f})"

def _acoustic_component(acousticness: float, likes_acoustic: bool) -> Tuple[float, str]:
    fit = acousticness if likes_acoustic else (1 - acousticness)
    points = ACOUSTIC_WEIGHT * fit
    return points, f"acoustic fit (+{points:.2f})"

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        reasons: List[str] = []
        total = 0.0

        genre_points, genre_reason = _genre_component(song.genre, user.favorite_genre)
        total += genre_points
        if genre_reason:
            reasons.append(genre_reason)

        mood_points, mood_reason = _mood_component(song.mood, user.favorite_mood)
        total += mood_points
        if mood_reason:
            reasons.append(mood_reason)

        energy_points, energy_reason = _energy_component(song.energy, user.target_energy)
        total += energy_points
        reasons.append(energy_reason)

        acoustic_points, acoustic_reason = _acoustic_component(song.acousticness, user.likes_acoustic)
        total += acoustic_points
        reasons.append(acoustic_reason)

        return total, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(self._score(user, song)[0], song) for song in self.songs]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        total, reasons = self._score(user, song)
        return f"Score {total:.2f} - " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    user_prefs keys: genre, mood, energy, and optionally likes_acoustic (bool)
    """
    reasons: List[str] = []
    total = 0.0

    genre_points, genre_reason = _genre_component(song["genre"], user_prefs.get("genre"))
    total += genre_points
    if genre_reason:
        reasons.append(genre_reason)

    mood_points, mood_reason = _mood_component(song["mood"], user_prefs.get("mood"))
    total += mood_points
    if mood_reason:
        reasons.append(mood_reason)

    if "energy" in user_prefs:
        energy_points, energy_reason = _energy_component(song["energy"], user_prefs["energy"])
        total += energy_points
        reasons.append(energy_reason)

    if "likes_acoustic" in user_prefs:
        acoustic_points, acoustic_reason = _acoustic_component(song["acousticness"], user_prefs["likes_acoustic"])
        total += acoustic_points
        reasons.append(acoustic_reason)

    return total, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, total, "; ".join(reasons))
        for song, total, reasons in (
            (song, *score_song(user_prefs, song)) for song in songs
        )
    ]

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
