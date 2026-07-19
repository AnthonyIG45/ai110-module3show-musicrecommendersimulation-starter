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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



