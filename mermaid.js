// Music Recommender System Data Flow (Mermaid.js)

/*
Paste this diagram into a Mermaid.js live editor or compatible Markdown viewer to visualize the process.
*/

flowchart TD
    A[User Preferences (UserProfile)] --> B[Recommender]
    B --> C[Song Catalog (songs.csv → Song objects)]
    C --> D[Score Each Song]
    D --> E{Score ≥ 0.85?}
    E -- Yes --> F[Add to Recommendations]
    E -- No --> G[Discard]
    F --> H[Sort and Select Top K]
    H --> I[Show Recommendations to User]
