# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Intuition check: "Deep Intense Rock"

Profile: `{"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}`

Top result: **Storm Runner** by Voltline, Score 4.89
(`genre match +2.0`, `mood match +1.0`, `energy closeness +0.99`, `acoustic fit +0.90`)

This is the only rock/intense track whose energy (0.91) sits almost exactly on the 0.9 target, so it edges out
Iron Vein (energy 0.94, score 4.88) and Highway Static (energy 0.88, score 4.86) — the top three are separated by
only 0.03 points, all three of them Voltline tracks.

**Does it feel right?** Mostly, but not completely. My own intuition when I ask for "deep intense rock" is that I
want the *heaviest* track — the one with the highest energy and fastest tempo (Iron Vein: energy 0.94, 158 BPM) —
not necessarily the one closest to an arbitrary 0.9 energy number. The scoring rewards **proximity to a target**,
not **maximum intensity**, so a listener who typed `0.9` as a rough "pretty high" estimate rather than an exact
number would probably expect Iron Vein on top instead of Storm Runner. That's a real gap between how the algorithm
optimizes (minimize distance to a number) and how a person actually thinks about "intense" (a direction, not a
point).

I asked my AI coding assistant to explain the ranking directly from the current weights in `recommender.py`, and
its explanation matched the math above exactly: genre and mood are flat +2.0/+1.0 bonuses that only apply on an
exact string match, while `_energy_component` and `_acoustic_component` are continuous terms computed as
`1 - abs(value - target)`, so among songs that already share genre and mood, ranking is decided entirely by
whichever one happens to sit closest to the numeric targets.

### Repeated top result across profiles

**Sunrise City** (pop, happy, energy 0.82) ranked #1 for both the "High-Energy Pop" profile (4.74) and the
"Unknown Genre" adversarial profile (2.70), where genre stopped contributing entirely. That's the warning sign
the assignment calls out: when a song keeps winning across different profiles, it's usually not because the
genre weight is too strong (genre only helped in one of those two cases) — it's because the **catalog is only
30 songs**, and "happy" mood has just 5 entries in it (Sunrise City, Rooftop Lights, Golden Hour, Morning
Playlist, Bloom Parade). With so few happy-mood songs, any profile favoring mood over a specific genre collapses
onto nearly the same short list, and the single highest-energy one among them keeps winning. A larger, more
varied catalog per mood/genre combination would surface more distinct top-5 lists per profile.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
