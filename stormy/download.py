import requests
import os
import sys
from stormy.utils import colors


def download_csv_file(
    name: str, sheet_id: str = "1wFRQ-EIMEUqx4yjBVeRkrX_5UgcV9rENszB5iZ4jkXM"
):
    print(f"Downloading sheet: {name}")

    url = f"https://docs.google.com/spreadsheets/d/{
        sheet_id}/gviz/tq?tqx=out:csv&sheet={name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        # Check for redirection to Google login page
        if response.url.startswith("https://accounts.google.com/"):
            print(
                colors.YELLOW
                + "Access Denied: The Google Sheet is not publicly accessible."
                + colors.RESET
            )
            sys.exit(1)

        output_dir = "raw_spreadsheet_data"
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, f"{name}.csv")
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"{colors.GREEN} Downloaded successfully: {
              colors.RESET} {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"{colors.RED} Downloaded failed: {colors.RESET} {e}")
        sys.exit(1)
