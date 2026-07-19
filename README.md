# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

* Mood, energy, and tempo_bpm seem to have a very strong coorelation to each other with higher BMP tending to be a more upbeat, happy, or intense song.
* I plan to have my system combine a few of the given data points into clusters to help fine tune the weighted score they receive.
* Genre, mood, energy, tempo, artist, and title

* The information that the user profile needs to store is likely their favorite genre, favorite mood, target energy, and if they like acoustics or not.

* It will compute the score using a weight based system. Grouping tempo and energy together for a flat 1 or 0, mood is a binary value as well as genre. We can then have an energy proximity fit versus acoustics.

* We will just rank the song by total score and then take the top one that hasnt been played already.

You can include a simple diagram or bullet list if helpful.

* Final algorithm will have a flat amount of points added if genre and mood are the same and then everything else can have a variance of points based off how close their values are to the value range of the users prefered genre.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 30
User profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

1. Sunrise City by Neon Echo - Score: 3.98
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.98)

2. Gym Hero by Max Pulse - Score: 2.87
     - genre match (+2.0)
     - energy closeness (+0.87)

3. Treadmill Anthem by Max Pulse - Score: 2.85
     - genre match (+2.0)
     - energy closeness (+0.85)

4. Sprint Interval by Max Pulse - Score: 2.84
     - genre match (+2.0)
     - energy closeness (+0.84)

5. Rooftop Lights by Indigo Parade - Score: 1.96
     - mood match (+1.0)
     - energy closeness (+0.96)
```

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

### Weight Shift: GENRE_WEIGHT 2.0→1.0, ENERGY_WEIGHT 1.0→2.0

Total max possible score stayed the same (2+1+1+1=5 vs. 1+1+2+1=5), so the change is a pure reallocation of
importance, not an overall inflation of scores. `pytest` still passed afterward, confirming the reallocation
didn't break the core ordering the tests depend on (pop/happy still on top for that profile).

**What actually changed:**

- **"Chill Lofi" #5 slot**: baseline had *Late Night Deadline* (lofi/focused — genre match, mood mismatch,
  score 3.69) in 5th place. With energy weight doubled, *Velvet Lounge* (jazz/chill — mood match, genre
  mismatch, score 3.90) took the spot instead. Halving genre's weight was enough for a mood-only match to beat
  a genre-only match, which never happened at the original weights.
- **"Deep Intense Rock" #2/#3 swap**: baseline order was Storm Runner (4.89) > Iron Vein (4.88) > Highway Static
  (4.86). After the shift, Highway Static and Iron Vein tied at 4.84, with Highway Static edging ahead on the
  tie-break. Iron Vein's advantage was a 0.04 acoustic-fit edge over Highway Static; Highway Static's advantage
  was a 0.02 energy-closeness edge. Doubling the energy weight turned that 0.02 into 0.04, exactly canceling
  Iron Vein's acoustic edge — a clean illustration of how weight ratios, not just absolute values, decide close
  rankings.
- **"Unknown Genre" #1 flip**: baseline top was Sunrise City (2.70); after the shift, Bloom Parade (3.59) passed
  it (3.58). Sunrise City's edge was a 0.15 acoustic-fit advantage; Bloom Parade's edge was a 0.08
  energy-closeness advantage. Doubling energy weight turned 0.08 into 0.16, just barely tipping past Sunrise
  City's 0.15 acoustic edge — the ranking flipped on a margin of 0.01.

**More accurate, or just different?** Just different, for this catalog. The shift didn't resolve the earlier
"Storm Runner vs. Iron Vein" intuition gap from the System Evaluation section — Iron Vein (the highest-energy,
most objectively "intense" rock track) still didn't reach #1, because the energy term rewards *proximity to
0.9*, not *maximum energy*, regardless of how heavily it's weighted. The experiment mainly showed that this
catalog has several songs sitting within a few hundredths of each other on the continuous terms, so small weight
changes are enough to flip rankings among near-ties without making any single result obviously "better" — it
just changes which near-tie wins. The change was reverted back to the original weights (GENRE_WEIGHT=2.0,
ENERGY_WEIGHT=1.0) for the delivered system.

---

## System Evaluation

Three standard taste profiles ("High-Energy Pop", "Chill Lofi", "Deep Intense Rock") plus four adversarial/edge-case
profiles are defined in `src/main.py` and run automatically by `python -m src.main`.

### Standard Profiles

```
Profile: High-Energy Pop
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False}

Top recommendations:

1. Sunrise City by Neon Echo - Score: 4.74
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.92)
     - acoustic fit (+0.82)

2. Gym Hero by Max Pulse - Score: 3.92
     - genre match (+2.0)
     - energy closeness (+0.97)
     - acoustic fit (+0.95)

3. Treadmill Anthem by Max Pulse - Score: 3.91
     - genre match (+2.0)
     - energy closeness (+0.95)
     - acoustic fit (+0.96)

4. Sprint Interval by Max Pulse - Score: 3.91
     - genre match (+2.0)
     - energy closeness (+0.94)
     - acoustic fit (+0.97)

5. Rooftop Lights by Indigo Parade - Score: 2.51
     - mood match (+1.0)
     - energy closeness (+0.86)
     - acoustic fit (+0.65)


Profile: Chill Lofi
User profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'likes_acoustic': True}

Top recommendations:

1. Rainy Window by Paper Lanterns - Score: 4.89
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.99)
     - acoustic fit (+0.90)

2. Sunday Sketchbook by Paper Lanterns - Score: 4.87
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.99)
     - acoustic fit (+0.88)

3. Library Rain by Paper Lanterns - Score: 4.81
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.95)
     - acoustic fit (+0.86)

4. Midnight Coding by LoRoom - Score: 4.59
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.88)
     - acoustic fit (+0.71)

5. Late Night Deadline by LoRoom - Score: 3.69
     - genre match (+2.0)
     - energy closeness (+0.89)
     - acoustic fit (+0.80)


Profile: Deep Intense Rock
User profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}

Top recommendations:

1. Storm Runner by Voltline - Score: 4.89
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.99)
     - acoustic fit (+0.90)

2. Iron Vein by Voltline - Score: 4.88
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.96)
     - acoustic fit (+0.92)

3. Highway Static by Voltline - Score: 4.86
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.98)
     - acoustic fit (+0.88)

4. Gym Hero by Max Pulse - Score: 2.92
     - mood match (+1.0)
     - energy closeness (+0.97)
     - acoustic fit (+0.95)

5. Treadmill Anthem by Max Pulse - Score: 2.91
     - mood match (+1.0)
     - energy closeness (+0.95)
     - acoustic fit (+0.96)
```

All three standard profiles behave as expected: the song that matches genre, mood, *and* energy tops each list, with
genre-only or mood-only partial matches filling out the rest of the top 5.

### Adversarial / Edge Case Profiles

```
Profile: Conflicting Energy vs Mood
User profile: {'genre': 'rock', 'mood': 'chill', 'energy': 0.95, 'likes_acoustic': False}

Top recommendations:

1. Iron Vein by Voltline - Score: 3.91
     - genre match (+2.0)
     - energy closeness (+0.99)
     - acoustic fit (+0.92)

2. Storm Runner by Voltline - Score: 3.86
     - genre match (+2.0)
     - energy closeness (+0.96)
     - acoustic fit (+0.90)

3. Highway Static by Voltline - Score: 3.81
     - genre match (+2.0)
     - energy closeness (+0.93)
     - acoustic fit (+0.88)

4. Treadmill Anthem by Max Pulse - Score: 1.96
     - energy closeness (+1.00)
     - acoustic fit (+0.96)

5. Sprint Interval by Max Pulse - Score: 1.96
     - energy closeness (+0.99)
     - acoustic fit (+0.97)


Profile: Unknown Genre
User profile: {'genre': 'metal', 'mood': 'happy', 'energy': 0.7, 'likes_acoustic': False}

Top recommendations:

1. Sunrise City by Neon Echo - Score: 2.70
     - mood match (+1.0)
     - energy closeness (+0.88)
     - acoustic fit (+0.82)

2. Bloom Parade by Indigo Parade - Score: 2.63
     - mood match (+1.0)
     - energy closeness (+0.96)
     - acoustic fit (+0.67)

3. Rooftop Lights by Indigo Parade - Score: 2.59
     - mood match (+1.0)
     - energy closeness (+0.94)
     - acoustic fit (+0.65)

4. Golden Hour by Indigo Parade - Score: 2.59
     - mood match (+1.0)
     - energy closeness (+0.99)
     - acoustic fit (+0.60)

5. Morning Playlist by Indigo Parade - Score: 2.56
     - mood match (+1.0)
     - energy closeness (+0.98)
     - acoustic fit (+0.58)


Profile: Genre vs Acoustic Contradiction
User profile: {'genre': 'jazz', 'mood': 'intense', 'energy': 0.05, 'likes_acoustic': False}

Top recommendations:

1. Velvet Lounge by Slow Stereo - Score: 2.85
     - genre match (+2.0)
     - energy closeness (+0.75)
     - acoustic fit (+0.10)

2. Firelight Waltz by Slow Stereo - Score: 2.82
     - genre match (+2.0)
     - energy closeness (+0.69)
     - acoustic fit (+0.13)

3. Paper Boats by Slow Stereo - Score: 2.81
     - genre match (+2.0)
     - energy closeness (+0.72)
     - acoustic fit (+0.09)

4. Coffee Shop Stories by Slow Stereo - Score: 2.79
     - genre match (+2.0)
     - energy closeness (+0.68)
     - acoustic fit (+0.11)

5. Gym Hero by Max Pulse - Score: 2.07
     - mood match (+1.0)
     - energy closeness (+0.12)
     - acoustic fit (+0.95)


Profile: Sparse Profile (Genre Only)
User profile: {'genre': 'synthwave'}

Top recommendations:

1. Night Drive Loop by Neon Echo - Score: 2.00
     - genre match (+2.0)

2. Neon Alley by Neon Echo - Score: 2.00
     - genre match (+2.0)

3. Skyline Pulse by Neon Echo - Score: 2.00
     - genre match (+2.0)

4. Static Heartbeat by Neon Echo - Score: 2.00
     - genre match (+2.0)

5. Sunrise City by Neon Echo - Score: 0.00
     - (no matching criteria)
```

**What this revealed:**

- **Conflicting Energy vs Mood** — since `rock` and `chill` never co-occur in the catalog, the mood term never
  fires. The flat +2.0 genre bonus still wins over songs that fit the (contradictory) energy target better,
  showing that a single strong categorical match can outweigh a fully-satisfied continuous term.
- **Unknown Genre** — an unrecognized genre string (`metal`) silently contributes 0 points rather than erroring,
  so the recommender degrades gracefully to ranking on mood + energy + acoustic alone. This is safe, but it also
  means a typo in the profile is indistinguishable from a genuine "no genre preference."
- **Genre vs Acoustic Contradiction** — asking for `jazz` (always highly acoustic in this catalog) while also
  setting `likes_acoustic: False` shows the genre bonus (+2.0) still dominating a near-zero acoustic fit score,
  so jazz tracks are recommended despite actively fighting the user's stated acoustic preference.
- **Sparse Profile (Genre Only)** — a profile with *only* a `genre` key exposed a real bug: once every
  genre-matching song was exhausted, `k=5` padded the list with a non-matching, effectively random song whose
  explanation string was empty, printing a blank, unexplained bullet. Fixed in `src/main.py` by falling back to
  an explicit `"(no matching criteria)"` label when the explanation list is empty. This is a good example of how
  padding a fixed-`k` recommendation list can surface junk results once genuine matches run out.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



