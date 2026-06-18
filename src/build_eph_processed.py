from pathlib import Path
from zipfile import ZipFile

import pandas as pd


RAW_DIR = Path("data") / "infoCruda" / "eph"
PROCESSED_DIR = Path("data") / "infoProcesada" / "eph"

INDIVIDUAL_OUTPUT = PROCESSED_DIR / "eph_individual_2016T2_2025T4.csv.gz"
HOGAR_OUTPUT = PROCESSED_DIR / "eph_hogar_2016T2_2025T4.csv.gz"
SUMMARY_OUTPUT = PROCESSED_DIR / "resumen_archivos_eph.csv"


def find_txt(zip_file: ZipFile, kind: str) -> str:
    kind_aliases = {
        "individual": ("individual", "personas"),
        "hogar": ("hogar",),
    }
    aliases = kind_aliases[kind]
    matches = [
        name
        for name in zip_file.namelist()
        if name.lower().endswith(".txt")
        and any(alias in Path(name).name.lower() for alias in aliases)
    ]
    if len(matches) != 1:
        raise ValueError(f"No se encontró un único archivo {kind}: {matches}")
    return matches[0]


def read_txt_from_zip(zip_path: Path, kind: str) -> pd.DataFrame:
    with ZipFile(zip_path) as zip_file:
        txt_name = find_txt(zip_file, kind)
        with zip_file.open(txt_name) as file:
            df = pd.read_csv(
                file,
                sep=";",
                encoding="latin1",
                low_memory=False,
            )

    df.columns = df.columns.str.upper()
    df["ARCHIVO_ORIGEN"] = zip_path.name
    return df


def build_dataset(kind: str) -> tuple[pd.DataFrame, list[dict]]:
    frames = []
    summary = []

    for zip_path in sorted(RAW_DIR.glob("EPH_usu_*_txt.zip")):
        df = read_txt_from_zip(zip_path, kind)
        frames.append(df)
        summary.append(
            {
                "archivo": zip_path.name,
                "tipo": kind,
                "filas": len(df),
                "columnas": len(df.columns),
                "anio_min": df["ANO4"].min() if "ANO4" in df.columns else None,
                "anio_max": df["ANO4"].max() if "ANO4" in df.columns else None,
                "trimestre_min": df["TRIMESTRE"].min()
                if "TRIMESTRE" in df.columns
                else None,
                "trimestre_max": df["TRIMESTRE"].max()
                if "TRIMESTRE" in df.columns
                else None,
            }
        )
        print(f"OK {kind:10} {zip_path.name}: {len(df):>7} filas")

    return pd.concat(frames, ignore_index=True, sort=False), summary


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    individual, individual_summary = build_dataset("individual")
    hogar, hogar_summary = build_dataset("hogar")

    individual.to_csv(INDIVIDUAL_OUTPUT, index=False, compression="gzip")
    hogar.to_csv(HOGAR_OUTPUT, index=False, compression="gzip")

    summary = pd.DataFrame(individual_summary + hogar_summary)
    summary.to_csv(SUMMARY_OUTPUT, index=False)

    print("\nResumen")
    print(f"Individual: {len(individual):,} filas, {len(individual.columns)} columnas")
    print(f"Hogar:      {len(hogar):,} filas, {len(hogar.columns)} columnas")
    print(f"Salida individual: {INDIVIDUAL_OUTPUT}")
    print(f"Salida hogar:      {HOGAR_OUTPUT}")
    print(f"Resumen archivos:  {SUMMARY_OUTPUT}")


if __name__ == "__main__":
    main()
