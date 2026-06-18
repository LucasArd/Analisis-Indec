from pathlib import Path
from zipfile import BadZipFile, ZipFile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph"
RAW_DIR = Path("data") / "infoCruda" / "eph"
START_YEAR = 2016
END_YEAR = 2025
QUARTERS = (1, 2, 3, 4)


def eph_filename(year: int, quarter: int) -> str:
    return f"EPH_usu_{quarter}_Trim_{year}_txt.zip"


def eph_filename_candidates(year: int, quarter: int) -> list[str]:
    candidates = [eph_filename(year, quarter)]

    if year == 2016:
        ordinal = {2: "2do", 3: "3er", 4: "4to"}.get(quarter)
        if ordinal:
            candidates.extend(
                [
                    f"EPH_usu_{ordinal}Trim_{year}_txt.zip",
                    f"EPH_usu_{ordinal}_Trim_{year}_txt.zip",
                    f"EPH_usu_{ordinal}_trim_{year}_txt.zip",
                    f"EPH_usu_{ordinal}Trim_{year}.zip",
                    f"EPH_usu_{ordinal}_Trim_{year}.zip",
                    f"EPH_usu_{ordinal}_trim_{year}.zip",
                ]
            )

    if year == 2017 and quarter == 1:
        candidates.extend(
            [
                "EPH_usu_1er_Trim_2017_txt.zip",
                "EPH_usu_1er_trim_2017_txt.zip",
                "EPH_usu_1_Trim_2017.zip",
                "EPH_usu_1er_Trim_2017.zip",
                "EPH_usu_1er_trim_2017.zip",
            ]
        )

    return candidates


def is_valid_zip(path: Path) -> bool:
    try:
        with ZipFile(path) as zip_file:
            return bool(zip_file.namelist())
    except BadZipFile:
        return False


def download_file(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    missing = []
    downloaded = []
    skipped = []

    for year in range(START_YEAR, END_YEAR + 1):
        for quarter in QUARTERS:
            if year == 2016 and quarter == 1:
                continue

            filename = eph_filename(year, quarter)
            destination = RAW_DIR / filename

            if destination.exists() and destination.stat().st_size > 0 and is_valid_zip(destination):
                skipped.append(filename)
                continue

            last_error = None
            for candidate in eph_filename_candidates(year, quarter):
                url = f"{BASE_URL}/{candidate}"

                try:
                    download_file(url, destination)
                    if is_valid_zip(destination):
                        downloaded.append(filename)
                        print(f"OK        {filename}")
                        break

                    last_error = "archivo descargado no es un zip válido"
                    destination.unlink()
                except (HTTPError, URLError, TimeoutError) as error:
                    last_error = str(error)
                    if destination.exists() and destination.stat().st_size == 0:
                        destination.unlink()
            else:
                missing.append((filename, last_error or "error desconocido"))
                print(f"FALLÓ     {filename} ({last_error})")

    print("\nResumen")
    print(f"Descargados: {len(downloaded)}")
    print(f"Ya estaban:  {len(skipped)}")
    print(f"Fallidos:    {len(missing)}")

    if missing:
        missing_path = RAW_DIR / "descargas_fallidas.txt"
        lines = [f"{filename}\t{error}" for filename, error in missing]
        missing_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Detalle de fallidos: {missing_path}")
    else:
        missing_path = RAW_DIR / "descargas_fallidas.txt"
        if missing_path.exists():
            missing_path.unlink()


if __name__ == "__main__":
    main()
