import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
import urllib3


# Silenciar advertencias SSL (el sitio no tiene cert válido)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


BASE_URL = (
    "https://lotoven.com/animalito/guacharoactivo/historial/{inicio}/{fin}/"
)


def read_existing(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except Exception:
        return set()


def last_date_for_year(path: str, year: int) -> datetime | None:
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in reversed(f.readlines()):
                parts = [p.strip() for p in line.strip().split(",")]
                if len(parts) >= 1:
                    try:
                        d = datetime.strptime(parts[0], "%Y-%m-%d")
                        if d.year == year:
                            return d
                    except Exception:
                        continue
    except Exception:
        return None
    return None


def fetch_week(start_date: datetime, end_date: datetime) -> list[str]:
    url = BASE_URL.format(
        inicio=start_date.strftime("%Y-%m-%d"),
        fin=end_date.strftime("%Y-%m-%d"),
    )
    resp = requests.get(url, verify=False, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")
    table = soup.find("table", class_="table")
    if not table:
        return []

    headers = [th.get_text(strip=True) for th in table.thead.find_all("th")][1:]

    # Collect all (date, time, value) then sort by date -> time
    unsorted_rows: list[tuple[str, datetime, str]] = []
    for tr in table.tbody.find_all("tr"):
        tds = tr.find_all("td")
        hour_str = tds[0].get_text(strip=True)
        try:
            hour_dt = datetime.strptime(hour_str, "%I:%M %p")
        except Exception:
            # Fallback: place unparsed times at the end by using a fixed time
            hour_dt = datetime.strptime("11:59 PM", "%I:%M %p")
        for i, td in enumerate(tds[1:]):
            number = td.get_text(strip=True)
            date_str = headers[i]
            unsorted_rows.append((date_str, hour_dt, number))

    unsorted_rows.sort(key=lambda r: (r[0], r[1].time()))
    return [f"{date_str}, {dt.strftime('%I:%M %p')}, {val}" for date_str, dt, val in unsorted_rows]


def week_iter(year: int) -> tuple[datetime, datetime]:
    today = datetime.now().date()
    start = datetime(year, 1, 1)
    start -= timedelta(days=start.weekday())  # mover al lunes de esa semana
    limit = datetime(year, 12, 31).date() if year < today.year else today
    while start.date() <= limit:
        end = start + timedelta(days=6)
        yield start, datetime.combine(min(end.date(), limit), datetime.min.time())
        start += timedelta(weeks=1)


def run(years: list[int]) -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "resultados_guacharoactivo_completo2.txt")

    print(f"Años a procesar: {years}")
    print(f"Archivo de salida: {out_path}\n")

    existing = read_existing(out_path)
    print(f"Registros existentes: {len(existing)}\n")

    for year in years:
        if year > datetime.now().year:
            print(f"- Omitiendo {year} (futuro)")
            continue

        print(f"== Año {year} ==")
        resume_from = last_date_for_year(out_path, year)
        if resume_from is not None:
            print(f"Reanudando desde: {resume_from.strftime('%Y-%m-%d')}\n")

        new_lines_count = 0
        for start, end in week_iter(year):
            if resume_from and start.date() <= resume_from.date():
                continue
            try:
                week_results = fetch_week(start, end)
            except Exception as e:
                print(f"  Semana {start:%Y-%m-%d}..{end:%Y-%m-%d}: error {e}")
                continue

            to_append = [r for r in week_results if r not in existing]
            if not to_append:
                continue

            with open(out_path, "a", encoding="utf-8") as f:
                for line in to_append:
                    f.write(line + "\n")
            existing.update(to_append)
            new_lines_count += len(to_append)
            print(
                f"  Semana {start:%Y-%m-%d}..{end:%Y-%m-%d}: +{len(to_append)} nuevos"
            )

        print(f"Año {year} completo. Nuevos agregados: {new_lines_count}\n")


if __name__ == "__main__":
    run([2023, 2024, 2025])


