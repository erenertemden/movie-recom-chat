# embedding/textual_rep.py
import pandas as pd

def create_textual_rep(row):
    def safe_str(val):
        return str(val).strip() if pd.notna(val) and val != "" else "Not Provided"

    return (
        f"Type: {safe_str(row.get('type'))}\n"
        f"Title: {safe_str(row.get('title'))}\n"
        f"Director: {safe_str(row.get('director'))}\n"
        f"Cast: {safe_str(row.get('cast'))}\n"
        f"Released: {safe_str(row.get('release_year'))}\n"
        f"Genres: {safe_str(row.get('listed_in'))}\n"
        f"Description: {safe_str(row.get('description'))}\n"
    )
