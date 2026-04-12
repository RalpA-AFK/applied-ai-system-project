# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
PrecisionTune Recommender 1.0  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 
It recommends top songs from a small fixed catalog for simulated users in a class exercise.  

Prompts:  

- What kind of recommendations does it generate  
	Content-based top-k song recommendations using genre, mood, and audio-feature similarity.  
- What assumptions does it make about the user  
	It assumes the user has one preferred genre and mood plus numeric targets for energy, tempo, danceability, and acousticness.  
- Is this for real users or classroom exploration  
	Classroom exploration only.  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  
Each song gets points for matching user preferences; closer numeric values get more points, and the highest total scores are recommended.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
	Genre, mood, energy, tempo (BPM), danceability, acousticness, and optional exact title/artist matches.  
- What user preferences are considered  
	Favorite genre, favorite mood, target energy, target tempo, target danceability, and target acousticness (plus optional favorite title/artist).  
- How does the model turn those into a score  
	It uses weighted sums: exact matches add full weight; numeric features add partial weight based on closeness within set thresholds; only songs with score >= 0.85 are kept and sorted.  
- What changes did you make from the starter logic  
	Added weighted linear closeness for tempo/energy/danceability/acousticness, added optional low-weight title/artist matches, and enforced a recommendation cutoff at 0.85.  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  
The model uses a local CSV catalog with hand-curated song metadata and audio-like attributes.  

Prompts:  

- How many songs are in the catalog  
	20 songs.  
- What genres or moods are represented  
	Genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, world, classical, chiptune, bluegrass, folk, hip hop, metal, new age, reggae, and space; moods include happy, chill, intense, relaxed, moody, focused, spiritual, calm, playful, joyful, nostalgic, confident, aggressive, peaceful, laid-back, and epic.  
- Did you add or remove data  
	Yes, the dataset includes additions beyond the smallest starter set (current catalog totals 20 songs).  
- Are there parts of musical taste missing in the dataset  
	Yes, it lacks lyrics/language context, regional diversity, long-tail subgenres, and enough examples per style for robust personalization.  

---

## 5. Strengths  

Where does your system seem to work well  
It works best when users have clear, specific preferences that align with the catalog labels.  

Prompts:  

- User types for which it gives reasonable results  
	Users with strong single-genre/single-mood preferences and realistic numeric targets (for example pop-happy or lofi-chill profiles).  
- Any patterns you think your scoring captures correctly  
	It captures combined mood plus tempo/energy fit well, so songs that feel behaviorally similar rank near the top.  
- Cases where the recommendations matched your intuition  
	Metal-aggressive users receive high-energy fast-tempo tracks, and lofi-chill users consistently get low-energy slower-tempo tracks.  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 
It is limited by a small catalog and rigid preference assumptions, which can produce narrow recommendations.  

Prompts:  

- Features it does not consider  
	It does not use lyrics, language, era, popularity, listening context, novelty preference, or collaborative behavior from other users.  
- Genres or moods that are underrepresented  
	Most genres/moods have only one or a few songs, so coverage is thin and uneven across styles.  
- Cases where the system overfits to one preference  
	Strong mood/tempo/energy weighting can over-prioritize those dimensions and reduce stylistic diversity in top results.  
- Ways the scoring might unintentionally favor some users  
	Users whose tastes match well-labeled high-density parts of the catalog are favored, while mixed or niche tastes are underserved.  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 
I evaluated using predefined contrasting and similar user profiles plus unit tests for ranking and explanation behavior.  

Prompts:  

- Which user profiles you tested  
	Contrasting profiles (pop, metal, classical, reggae, chiptune) and similar lofi-chill profiles.  
- What you looked for in the recommendations  
	I checked whether top results matched each profile's genre/mood and feature targets, and whether similar users had overlapping results.  
- What surprised you  
	Small threshold/weight choices strongly changed which songs cleared the 0.85 cutoff.  
- Any simple tests or comparisons you ran  
	Ran pytest checks to confirm history overlap for contrasting users, overlap for similar users, sorted recommendation order, and non-empty explanations.  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  
Expand data coverage and add smarter ranking objectives beyond single-profile similarity.  

Prompts:  

- Additional features or preferences  
	Add language, release year, popularity, lyrical theme, skip behavior, and time-of-day/context preferences.  
- Better ways to explain recommendations  
	Show per-feature contribution breakdown and short plain-language reasons for why each song ranked where it did.  
- Improving diversity among the top results  
	Add a diversity penalty so near-duplicate songs do not occupy multiple top slots.  
- Handling more complex user tastes  
	Support multi-genre preference vectors and session-aware preference shifts instead of one fixed profile.  

---

## 9. Personal Reflection  

A few sentences about your experience.  
I learned that recommender quality depends heavily on feature design and weighting, not just code structure. I also saw how quickly a simple scoring rule can become biased when data coverage is uneven. This changed my view of music apps by making it clear that recommendation outputs are shaped by modeling choices and dataset limits as much as by user taste.  

Prompts:  

- What you learned about recommender systems  
	They are structured ranking systems where feature selection, weight tuning, and thresholds directly control user experience.  
- Something unexpected or interesting you discovered  
	Very small parameter changes can create large shifts in which songs are recommended.  
- How this changed the way you think about music recommendation apps  
	I now see recommendations as constrained approximations of taste, not neutral predictions, because they reflect both data and design tradeoffs.  
