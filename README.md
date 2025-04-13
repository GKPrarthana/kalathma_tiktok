# 🕵️kalathma_tiktok

This project scrapes, cleans, and analyzes TikTok comments on viral videos about weird celebrity encounters in Sri Lanka. Using NLP, network analysis, and data visualization, it uncovers who’s being talked about, what kind of drama is unfolding, and how people are reacting in real-time. ☕️

🚀 Features
🧠 Named Entity Recognition (NER): Extracts celebrity names from user comments

📈 Network Graphs: Visualizes co-occurrences of names to detect gossip clusters and influencers

❤️ Sentiment Analysis: Detects tone and emotion in both comments and replies

🔥 Top Mentions: Ranks the most-discussed celebrities

💡 Topic Clustering: Groups similar gossip threads using unsupervised ML

🌐 Interactive Dashboard (optional): Displays insights using Streamlit / Dash

📂 Project Structure
```bash
kalathma-tiktok-gossip/
│
├── data/
│   └── tiktok_comments.csv        # Raw/cleaned data
│
├── notebooks/
│   └── eda_and_nlp_analysis.ipynb # Jupyter notebook for exploration
│
├── src/
│   ├── scraper.py                 # TikTok scraper using asyncio + TikTokApi
│   ├── text_cleaner.py            # Emoji remover, lowercasing, etc.
│   ├── nlp_pipeline.py            # NER, sentiment, clustering
│   ├── network_graph.py           # Builds & visualizes name co-mention graphs
│   └── dashboard.py               # (Optional) Streamlit dashboard
│
├── kalathma.py                    # Main async script to scrape data
├── requirements.txt               # Python dependencies
└── README.md                      # You're reading it :)
```
🧪 How to Run
Install dependencies


pip install -r requirements.txt
Install Playwright (if scraping)


playwright install
Run the scraper

python kalathma.py
Explore the data Run the Jupyter notebook in notebooks/.

(Optional) Launch dashboard

streamlit run src/dashboard.py
📊 Example Insights
Top 3 most-mentioned celebs: Kavihari Haputantri, Avishka Deshan, Miona de Silva

Most shocked comment style: “DIVORCED???”

Identified clusters: Cheating drama, Photographer saga, Clout chasing stories

📌 Dependencies
TikTokApi

Playwright

Pandas

Spacy / nltk

NetworkX, Matplotlib, Plotly

Scikit-learn

Streamlit (optional)