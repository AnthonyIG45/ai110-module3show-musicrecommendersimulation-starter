# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeCheck 1.0**

---

## 2. Intended Use  

VibeCheck picks songs from a small catalog that match what a user says they like.

You give it a genre, a mood, an energy level, and whether you like acoustic sound.
It hands back the top 5 songs that fit best, plus a plain-English reason for each one.

It assumes you can describe your taste in those four simple terms.
It does not know your listening history or who you are.

This is a classroom project, not a real product. It's built to teach how recommenders work, not to run a real
music app.

---

## 3. How the Model Works  

Think of it like a judge scoring every song in the catalog, one at a time.

The judge hands out points for four things:

- **Genre match** — is it the genre you said you like? Big flat bonus if yes, nothing if no.
- **Mood match** — is it the mood you said you like? Smaller flat bonus if yes, nothing if no.
- **Energy fit** — how close is the song's energy to the energy you asked for? The closer, the more points.
- **Acoustic fit** — does the song's acoustic sound match whether you said you like acoustic music or not? Again,
  closer fit means more points.

Add up all four, and that's the song's score. Sort every song by score, highest first, and hand back the top 5.

The starter code just returned the first 5 songs in the file with no scoring at all. My version is the first
version that actually scores and ranks anything.

---

## 4. Data  

The catalog is small: 30 songs total, in `data/songs.csv`.

Each song has: title, artist, genre, mood, energy, tempo, valence, danceability, and how acoustic it is.

Genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop (7 genres).
Moods: happy, chill, intense, relaxed, moody, focused (6 moods).

I didn't add or remove any songs — this is the dataset as given.

Some genres are barely represented (rock only has 3 songs, all by one artist), so certain tastes get way less
variety than others. There's also no genre like metal, EDM, or classical, and no way to search by lyrics or
language — so some real-world tastes just aren't in here at all.

---

## 5. Strengths  

It works best for users whose taste is a "clean" combination that's actually common in the catalog — like happy
pop, chill lofi, or intense rock. For those users, the #1 result really is the obviously right song: it matches
genre, mood, *and* energy all at once.

The reasons list is honest and easy to read. You can see exactly why a song scored the way it did, which makes
it easy to catch when the ranking looks weird.

It also handles a missing preference gracefully — if you only give it a genre, it still returns something
instead of crashing, though the results get less meaningful (see Section 7).

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Short version:** rock fans always get songs by the same one artist, because the catalog only has 3 rock songs
and they're all by Voltline. That's a filter bubble — not because the code is biased, but because the data is
unbalanced. Details below.

### Discovered weakness: genre/artist representation imbalance creates a filter bubble

Checking `data/songs.csv` directly, genre representation is uneven: lofi has 7 songs (the most of any genre)
while rock has only 3, and every single rock song is by the same artist, Voltline. Because `_genre_component`
gives a flat +2.0 bonus for an exact genre match with no artist-diversity penalty, a "rock" fan's top 5 will
always be dominated by Voltline whenever k approaches or exceeds 3, since there simply is no other rock artist
to recommend instead — the system can't avoid over-representing one artist for underrepresented genres, and a
lofi fan gets far more variety (LoRoom and Paper Lanterns both contribute) purely because the catalog happens to
contain more lofi tracks. A second, related bias sits in `UserProfile.target_energy`: it's a required field with
no way to express "I don't have an energy preference," so a user who is genuinely indifferent to energy is
forced to guess a number, and `_energy_component`'s symmetric `1 - abs(energy - target)` penalty will silently
punish that guess as if it were a real preference. Both issues would get worse, not better, as the catalog grows
unevenly (e.g., if more pop gets added but rock does not), since the scoring logic has no built-in mechanism to
correct for category size.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Short version:** I ran 7 different user profiles (3 normal, 4 designed to try to break it) and compared the
top 5 songs each time. Most results made sense. The biggest surprise was a high-energy "intense" pop song
sneaking into the top of a "happy" search — explained in plain language below.

### Profiles tested

Seven profiles in total, run via `python -m src.main` (`src/main.py`):

- **Standard:** High-Energy Pop, Chill Lofi, Deep Intense Rock
- **Adversarial:** Conflicting Energy vs Mood, Unknown Genre, Genre vs Acoustic Contradiction, Sparse Profile
  (Genre Only)

For each one I looked at: did the #1 song actually match genre+mood+energy the way I'd expect, did the top-5 stay
inside the requested genre/mood or drift outside it, and did the score magnitude itself seem to reflect how
"satisfiable" the request was.

**What surprised me most:** *Gym Hero* — a pop song whose actual mood is `intense`, not `happy` — lands at #2 in
the "High-Energy Pop" (`genre=pop, mood=happy, energy=0.9`) results, ahead of several genuinely happy songs. See
the plain-language explanation below.

### Pairwise comparisons

- **High-Energy Pop vs. Chill Lofi** — these two target opposite ends of the energy scale (0.9 vs. 0.3) and
  opposite acoustic preferences (non-acoustic vs. acoustic). The results split cleanly: Pop's top 5 are all loud,
  danceable, low-acousticness tracks (Sunrise City, Gym Hero, Treadmill Anthem...), while Lofi's top 5 are all
  soft, high-acousticness tracks (Rainy Window, Sunday Sketchbook...). This makes sense — energy and
  acousticness happen to move in opposite directions across this catalog, so asking for opposite values on both
  produces two non-overlapping playlists.

- **High-Energy Pop vs. Deep Intense Rock** — both ask for the *same* energy target (0.9) and the *same*
  non-acoustic preference, differing only in genre (pop vs. rock) and mood (happy vs. intense). Despite wanting a
  very similar "vibe" (fast, loud, danceable), the two top-5 lists share zero songs. That makes sense given how
  the scoring works: genre is a hard categorical filter (+2.0, all-or-nothing), so even though a rock fan and a
  pop fan asked for the same intensity, the genre bonus keeps them in entirely separate lanes of the catalog.

- **Genre vs. Acoustic Contradiction vs. Chill Lofi** — both target low energy and low-acoustic-leaning genres
  (jazz vs. lofi), but the jazz profile explicitly asks for `likes_acoustic: False` even though jazz songs in this
  catalog are all highly acoustic (0.87–0.91). The result: Chill Lofi's top score is 4.89, while the jazz
  profile's top score tops out at 2.85 — nearly two full points lower. That gap makes sense and is actually
  useful: a low ceiling on the *best possible* score is itself a signal that the profile is asking for something
  the catalog can't cleanly deliver, i.e. an internally-contradictory profile "shows up" in the numbers, not just
  in the song choices.

- **Unknown Genre vs. High-Energy Pop** — same mood (`happy`) and similar energy targets (0.7 vs. 0.9), but one
  profile's genre (`metal`) doesn't exist in the catalog at all. Top scores drop from ~4.7 (Pop, genre matches)
  to ~2.7 (Unknown Genre, genre never matches) — roughly the size of the genre bonus itself. That confirms genre
  is the single biggest lever in the whole scoring system: losing it costs more than mood, energy, and acoustic
  fit combined typically add up to.

- **Sparse Profile (Genre Only) vs. Deep Intense Rock** — Deep Intense Rock supplies all four preferences and
  produces a smoothly decreasing, clearly differentiated set of scores (4.89 down to 2.91). Sparse Profile
  supplies only a genre and produces four songs tied at an identical 2.00, followed by a non-matching song at
  0.00. Without mood/energy/acoustic data to break ties, the system literally cannot tell same-genre songs apart
  — it needs at least one continuous feature filled in to produce a meaningfully ranked list.

### Plain language: why does "Gym Hero" keep showing up for people who just want "Happy Pop"?

Imagine the recommender as a judge handing out points for four separate things: is it the right genre (big
prize), is it the right mood (smaller prize), is the energy level close to what you asked for (medium prize that
scales with how close it is), and does it fit your like/dislike of acoustic sound (another scaling prize). Gym
Hero is a pop song, so it wins the big "right genre" prize. Its energy (0.93) is almost exactly what a
high-energy fan asked for (0.9), so it wins most of that prize too. And it's about as far from "acoustic" as a
song can get, so if the fan said they don't like acoustic sound, Gym Hero wins that prize as well. The only
thing it *doesn't* win is the mood prize, because Gym Hero's actual mood is "intense" (a gym-hype anthem), not
"happy." But three big prizes plus zero for mood still adds up to more total points than a song that only wins
the (smaller) mood and energy prizes. In other words: the judge is really scoring "is this the right *kind* of
song, played at the right *intensity*" much more heavily than "does this song feel *happy*" — so a driving,
adrenaline-pumping pop song can out-score a genuinely cheerful one, even when the person asked for "happy."

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

If I kept working on this, here's what I'd change first:

1. **Let users say "no preference."** Right now energy is a required number, so someone with no real opinion has
   to guess one and gets scored against that guess anyway. I'd make it optional.
2. **Add an artist-diversity rule.** Right now the top 5 can be one artist over and over if their genre is
   small (like rock/Voltline). I'd cap how many songs from the same artist can appear in one list.
3. **Use tempo, valence, and danceability as tiebreakers.** They're already in the data but unused. They'd help
   break near-ties (like Storm Runner vs. Iron Vein) in a way that matches how a person actually judges
   "intensity," instead of leaving it to whichever song sits closest to one number.

---

## 9. Personal Reflection  

Building this made it obvious that a recommender isn't "smart" — it's just addition. Every song gets a few
points added up from simple rules, and whichever song has the most points wins. There's no understanding of
music happening anywhere, just arithmetic on labels someone typed into a spreadsheet.

The most interesting thing I found was that genre acts almost like a locked door; if you don't match it, you
lose a big chunk of points and basically can't win, no matter how well everything else fits. That's a strong
design choice, and it's also where bias sneaks in: whichever genres happen to have more songs in the data end
up giving their fans more variety, for no reason related to their actual taste.

That changed how I think about real recommendation apps. If a tiny 4-rule system I built by hand can already
have a filter bubble and can already prefer "loud and general-genre-correct" over "actually matches how you
feel," a real app with millions of songs and hidden rules almost certainly has similar blind spots, just much
harder to spot.
