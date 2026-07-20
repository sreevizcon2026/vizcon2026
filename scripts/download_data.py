#!/usr/bin/env python3
"""
Download all datasets for VizCon 2026: 24 Hours on Planet Earth
Run once to populate data/raw/
"""

import os
import requests

RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(RAW_DIR, exist_ok=True)


DATASETS = {
    # Our World in Data (GitHub - correct URLs)
    "owid_time_use.csv": "https://raw.githubusercontent.com/owid/etl/master/etl/steps/data/garden/oecd/2024-04-16/time_use.csv",
    "owid_life_expectancy.csv": "https://raw.githubusercontent.com/owid/owid-datasets/refs/heads/master/datasets/Life%20expectancy%20-%20OWID%20based%20on%20Riley%2C%20Clio-Infra%20%26%20UN/Life%20expectancy%20-%20OWID%20based%20on%20Riley%2C%20Clio-Infra%20%26%20UN.csv",
    "owid_internet.csv": "https://raw.githubusercontent.com/owid/owid-datasets/refs/heads/master/datasets/Number%20of%20internet%20users%20by%20country%20-%20OWID%20based%20on%20WB%20%26%20UN/Number%20of%20internet%20users%20by%20country%20-%20OWID%20based%20on%20WB%20%26%20UN.csv",
    "owid_happiness.csv": "https://raw.githubusercontent.com/owid/owid-datasets/refs/heads/master/datasets/Happiness%20and%20Life%20Satisfaction%20-%20World%20Happiness%20Report%20(2017)/Happiness%20and%20Life%20Satisfaction%20-%20World%20Happiness%20Report%20(2017).csv",
    "owid_food_supply.csv": "https://raw.githubusercontent.com/owid/owid-datasets/refs/heads/master/datasets/Daily%20caloric%20supply%20per%20capita%20-%20FAO%20(2017)%20%26%20Various%20historical%20sources/Daily%20caloric%20supply%20per%20capita%20-%20FAO%20(2017)%20%26%20Various%20historical%20sources.csv",
    "owid_electricity.csv": "https://raw.githubusercontent.com/owid/owid-datasets/refs/heads/master/datasets/Share%20of%20the%20population%20with%20access%20to%20electricity%20-%20World%20Bank%20(WDI)/Share%20of%20the%20population%20with%20access%20to%20electricity%20-%20World%20Bank%20(WDI).csv",
    "owid_mobile.csv": "https://raw.githubusercontent.com/owid/owid-datasets/refs/heads/master/datasets/Mobile%20cellular%20subscriptions%20-%20World%20Bank%20(WDI)%20(2017)/Mobile%20cellular%20subscriptions%20-%20World%20Bank%20(WDI)%20(2017).csv",
    "owid_child_mortality.csv": "https://raw.githubusercontent.com/owid/owid-datasets/refs/heads/master/datasets/Child%20mortality%20rate%20-%20IHME/Child%20mortality%20rate%20-%20IHME.csv",
    "owid_water_access.csv": "https://raw.githubusercontent.com/owid/owid-datasets/refs/heads/master/datasets/Access%20to%20safe%20drinking%20water%20-%20WHO-UNICEF%20(2017)/Access%20to%20safe%20drinking%20water%20-%20WHO-UNICEF%20(2017).csv",

    # World Bank
    "worldbank_gdp_per_capita.csv": "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv",

    # OpenFlights
    "openflights_routes.csv": "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat",
    "openflights_airports.csv": "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat",

    # OECD Working Hours (direct CSV)
    "oecd_working_hours.csv": "https://stats.oecd.org/sdmx-json/data/ANHRS/AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA/.HRWKD./all?startTime=2015&endTime=2023&dimensionAtObservation=allDimensions&format=csv",
}


def download_file(url, filename):
    filepath = os.path.join(RAW_DIR, filename)
    if os.path.exists(filepath):
        print(f"  ✓ Already exists: {filename}")
        return True

    print(f"  ↓ Downloading: {filename}...")
    try:
        resp = requests.get(url, timeout=60, allow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 100:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            print(f"  ✓ Saved: {filename} ({len(resp.content) / 1024:.0f} KB)")
            return True
        else:
            print(f"  ✗ Failed ({resp.status_code}): {filename}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {filename} - {e}")
        return False


def main():
    print("=" * 60)
    print("24 Hours on Planet Earth - Dataset Downloader")
    print("=" * 60)
    print()

    success = 0
    failed = 0
    for filename, url in DATASETS.items():
        if download_file(url, filename):
            success += 1
        else:
            failed += 1

    print()
    print(f"Results: {success} downloaded, {failed} failed")
    print()
    print("=" * 60)
    print("MANUAL DOWNLOADS (if any above failed):")
    print()
    print("  1. Our World in Data (all-in-one):")
    print("     → https://github.com/owid/owid-datasets/tree/master/datasets")
    print("     → Search for: time use, life expectancy, internet, food supply")
    print()
    print("  2. OECD Time Use:")
    print("     → https://data-explorer.oecd.org")
    print("     → Search: 'time use'")
    print("     → Save as: data/raw/oecd_time_use.csv")
    print()
    print("  3. World Happiness Report:")
    print("     → https://worldhappiness.report/data/")
    print("     → Save as: data/raw/world_happiness.csv")
    print()
    print("  4. FAOSTAT Food Balance:")
    print("     → https://www.fao.org/faostat/en/#data/FBS")
    print("     → Save as: data/raw/fao_food_balance.csv")
    print("=" * 60)


if __name__ == "__main__":
    main()
