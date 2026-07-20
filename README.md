# 24 Hours on Planet Earth
## VizCon 2026 Entry

**Theme:** How the World Lives, Thrives & Connects  
**Tagline:** Every hour reveals a different story about humanity.  
**Tool:** Streamlit + Plotly + Mapbox  
**Deadline:** August 10, 2026

---

## Story Arc (6 Chapters)

| Chapter | Time | Question | Key Insight |
|---------|------|----------|-------------|
| 1 | 06:00 | How does the world wake up? | Longest sleepers aren't the happiest |
| 2 | 08:00 | Does working more = richer? | Some countries work less but produce more per hour |
| 3 | 12:00 | What does the world eat? | Healthiest diets aren't the most expensive |
| 4 | 15:00 | How connected is humanity? | Some regions leapfrogged to mobile, skipping landlines |
| 5 | 18:00 | Do richer families spend more time together? | Income ≠ family time |
| 6 | 22:00 | How does the world rest? | Life expectancy and sleep don't always correlate |

---

## Data Sources

| Dataset | Source | URL |
|---------|--------|-----|
| OECD Time Use | OECD | https://data-explorer.oecd.org |
| World Happiness Report | Kaggle | https://www.kaggle.com/datasets/unsdsn/world-happiness |
| World Bank Indicators | World Bank | https://data.worldbank.org |
| Our World in Data | GitHub | https://github.com/owid/owid-datasets |
| FAOSTAT | FAO | https://www.fao.org/faostat |
| OpenFlights | OpenFlights | https://openflights.org/data |
| WHO Health | WHO | https://www.who.int/data/gho |

---

## Tech Stack

- **App:** Streamlit
- **Charts:** Plotly Express + Plotly Graph Objects
- **Maps:** Plotly Choropleth / Mapbox
- **Data:** Pandas, DuckDB
- **Animations:** Streamlit transitions, custom CSS
- **Deployment:** Streamlit Cloud (free)
- **AI:** Claude/ChatGPT for data discovery, code gen, insight validation

---

## Project Structure

```
vizcon2026/
├── data/
│   ├── raw/          # Downloaded CSVs
│   ├── curated/      # Cleaned per-source
│   └── master/       # Final merged dataset
├── notebooks/        # Exploration & analysis
├── scripts/          # ETL & data processing
├── app/              # Streamlit app
├── assets/           # Images, fonts, CSS
├── docs/             # Documentation
└── README.md
```

---

## Timeline

| Week | Focus |
|------|-------|
| Week 1 (Jul 19-25) | Data collection, cleaning, master dataset, first prototype |
| Week 2 (Jul 26-Aug 1) | Build all 6 chapters, add interactions |
| Week 3 (Aug 2-8) | Polish visuals, validate insights, accessibility, deploy |
| Aug 10 | Submit |

---

## Killer Feature: "Guess First"

Each chapter starts with a question. User guesses the answer.  
Then the data reveals the truth.  
Creates engagement + surprise = exactly what judges want.
