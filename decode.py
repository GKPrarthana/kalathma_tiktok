import pandas as pd
import html

# Load your dataset
df = pd.read_csv("tiktok_comments.csv")

# Decode messed up text (emoji encoding issues)
df["Comment"] = df["Comment"].apply(lambda x: html.unescape(str(x).encode('latin1').decode('utf-8', errors='ignore')))
df["Reply"] = df["Reply"].apply(lambda x: html.unescape(str(x).encode('latin1').decode('utf-8', errors='ignore')))

# Save cleaned file
df.to_csv("decoded_comments.csv", index=False)
print("✅ Cleaned and saved as 'cleaned_tiktok_data.csv'")
