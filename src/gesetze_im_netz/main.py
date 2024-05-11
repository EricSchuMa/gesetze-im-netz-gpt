import re

import uvicorn
from datasets import load_dataset
from fastapi import FastAPI

app = FastAPI()


# Utility functions (already defined)
def extract_section_number(text):
    # This regular expression targets section numbers that appear at the start of the text.
    # We use '^' to match the beginning of the text.
    range_match = re.search(r"^§§\s*(\d+)\s*bis\s*(\d+)", text)
    if range_match:
        start, end = int(range_match.group(1)), int(range_match.group(2))
        return list(range(start, end + 1))

    # Similarly, this searches for a single section number at the start of the text.
    single_match = re.search(r"^§\s*(\d+)", text)
    if single_match:
        return [int(single_match.group(1))]

    return None


dataset = load_dataset("wndknd/german-law-bgb")
df = dataset["train"].to_pandas()  # convert to pandas DataFrame
df["section"] = df["text"].apply(extract_section_number)


def get_paragraph(df, query):
    query = query.strip().replace(" ", "")
    query_number = int(re.search(r"§(\d+)", query).group(1))
    for index, row in df.iterrows():
        if row["section"] is not None and query_number in row["section"]:
            return row["text"]
    return "Section not found."


# Endpoint to get paragraph by section number
@app.get("/bgb/{section}")
def read_section(section: str):
    section_text = get_paragraph(df, section)
    return {"section": section, "text": section_text}


# Include this if you want to run using python script instead of command line
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
