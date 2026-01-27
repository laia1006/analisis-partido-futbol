import pandas as pd

# Cargar datos
df_raw = pd.read_csv("/Users/laiazamora/Desktop/carpeta/Hackathon_fcb/Sample_Game_2_RawEventsData.csv", sep=",")
df_raw.columns = df_raw.columns.str.strip()

print(df_raw.columns)

# Filtrar solo pases válidos
passes = df_raw[
    (df_raw["Type"] == "PASS") &
    (df_raw["From"].notna()) &
    (df_raw["To"].notna())
]

# Crear dataframe estándar para el modelo
df = passes[["From", "To", "Start Time [s]"]].copy()
df.columns = ["passer", "receiver", "minute"]

# Convertir segundos a minutos
df["minute"] = df["minute"] / 60

print(df.head())

df.to_csv("passes.csv", index=False)
