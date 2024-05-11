import re

import uvicorn
from datasets import load_dataset
from fastapi import FastAPI

app = FastAPI()


# Define a utility function to extract section or article numbers
def extract_section_or_article(text):
    # Match articles in Grundgesetz
    art_match = re.search(r"^Art\s+(\d+)(\s+[a-z])?", text)
    if art_match:
        return [
            f"{art_match.group(1)}{art_match.group(2).strip() if art_match.group(2) else ''}"
        ]

    # Handle range of sections with optional suffix letters (for BGB/STGB)
    range_match = re.search(r"^§§\s*(\d+)([a-z]?)\s*bis\s*(\d+)([a-z]?)", text)
    if range_match:
        start, start_suffix, end, end_suffix = range_match.groups()
        return [
            f"{num}{start_suffix if num == int(start) else end_suffix}"
            for num in range(int(start), int(end) + 1)
        ]

    # Handle single section with optional suffix letter
    single_match = re.search(r"^§\s*(\d+)([a-z]?)", text)
    if single_match:
        return [f"{single_match.group(1)}{single_match.group(2)}"]

    return None


# Load datasets and preprocess
def load_and_prepare_data(dataset_name):
    dataset = load_dataset(dataset_name)
    df = dataset["train"].to_pandas()
    df["section"] = df["text"].apply(extract_section_or_article)
    return df


bgb = load_and_prepare_data("wndknd/german-law-bgb")
stgb = load_and_prepare_data("wndknd/german-law-stgb")
gg = load_and_prepare_data("wndknd/german-law-gg")  # Grundgesetz
sgb_1 = load_and_prepare_data("wndknd/german-law-sgb1")  # Sozialgesetzbuch I


# Define a function to get paragraph by section number or article
def get_paragraph(df, query):
    query = query.strip().replace(" ", "").replace("§", "").replace("Art", "")
    for index, row in df.iterrows():
        if row["section"] is not None and query in row["section"]:
            return row["text"]
    return "Section or article not found."


# Unified endpoint to get paragraph by section number or article
@app.get("/{dataset_name}/{section_or_article}")
def read_section_or_article(dataset_name: str, section_or_article: str):
    if dataset_name == "bgb":
        df = bgb
    elif dataset_name == "stgb":
        df = stgb
    elif dataset_name == "gg":
        df = gg
    elif dataset_name == "sgb1":
        df = sgb_1
    else:
        return {
            "section_or_article": section_or_article,
            "text": "Invalid dataset name",
        }

    text = get_paragraph(df, section_or_article)
    return {"section_or_article": section_or_article, "text": text}


# Run the application if executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
