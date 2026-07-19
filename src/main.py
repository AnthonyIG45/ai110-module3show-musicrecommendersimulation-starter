"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Three distinct, realistic taste profiles.
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
}

# Adversarial / edge-case profiles designed to try to "trick" the scoring logic.
ADVERSARIAL_PROFILES = {
    # Genre (rock) and mood (chill) never co-occur in the catalog, and the
    # energy target contradicts "chill" outright.
    "Conflicting Energy vs Mood": {"genre": "rock", "mood": "chill", "energy": 0.95, "likes_acoustic": False},
    # Genre does not exist anywhere in the catalog.
    "Unknown Genre": {"genre": "metal", "mood": "happy", "energy": 0.7, "likes_acoustic": False},
    # Jazz tracks are always high-acousticness/low-energy; this profile wants
    # jazz but also wants near-zero energy AND non-acoustic sound.
    "Genre vs Acoustic Contradiction": {"genre": "jazz", "mood": "intense", "energy": 0.05, "likes_acoustic": False},
    # Minimal profile: only a genre, no mood/energy/likes_acoustic keys at all.
    "Sparse Profile (Genre Only)": {"genre": "synthwave"},
}


def run_profiles(label: str, profiles: dict, songs: list) -> None:
    print(f"\n{'=' * 60}\n{label}\n{'=' * 60}")
    for name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nProfile: {name}")
        print(f"User profile: {user_prefs}")
        print("\nTop recommendations:\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            reasons = explanation.split("; ") if explanation else ["(no matching criteria)"]
            for reason in reasons:
                print(f"     - {reason}")
            print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    run_profiles("Standard Profiles", PROFILES, songs)
    run_profiles("Adversarial / Edge Case Profiles", ADVERSARIAL_PROFILES, songs)


if __name__ == "__main__":
    main()
