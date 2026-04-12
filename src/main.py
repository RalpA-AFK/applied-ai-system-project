"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.test_recommender import contrasting_users, similar_users


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_sets = [
        ("Contrasting Users", contrasting_users),
        ("Similar Users", similar_users)
    ]

    for set_name, user_list in user_sets:
        stat_keys = ["genre", "mood", "energy", "tempo", "danceability", "acousticness"]
        stat_labels = ["Genre", "Mood", "Energy", "Tempo", "Danceability", "Acousticness"]
        song_count = 3
        col_labels = ["User"] + stat_labels + [f"Top Song {i+1}" for i in range(song_count)]
        col_widths = [8] + [14]*len(stat_labels) + [38]*song_count

        # Gather all data for each user
        user_rows = []
        for idx, user in enumerate(user_list):
            row = [f"User {idx+1}"]
            for key in stat_keys:
                row.append(str(user["prefs"].get(key, "-")))
            recs = recommend_songs(user["prefs"], songs, k=song_count)
            for i in range(song_count):
                if i < len(recs):
                    song, score, explanation = recs[i]
                    song_str = f"{song.title} ({score:.2f})"
                    expl_str = explanation.replace(", ", "; ")
                    cell = f"{song_str}\n{expl_str}"
                    row.append(cell)
                else:
                    row.append("-")
            user_rows.append(row)

        # Print table
        table_width = sum(col_widths) + len(col_widths)*3 + 1
        print("\n" + "="*table_width)
        print(set_name.center(table_width))
        print("="*table_width)
        # Header
        print("|", end="")
        for label, width in zip(col_labels, col_widths):
            print(f" {{:^{width}}} |".format(label), end="")
        print()
        print("|" + "|".join(["-"*w for w in col_widths]) + "|")
        # Rows
        for row in user_rows:
            print("|", end="")
            for cell, width in zip(row, col_widths):
                # For multi-line cells (song explanations), align each line
                lines = cell.split("\n")
                if len(lines) == 1:
                    print(f" {{:<{width}}} |".format(lines[0]), end="")
                else:
                    # Print first line, then pad subsequent lines
                    print(f" {{:<{width}}} |".format(lines[0]), end="")
            print()
        print("-"*table_width)


if __name__ == "__main__":
    main()
