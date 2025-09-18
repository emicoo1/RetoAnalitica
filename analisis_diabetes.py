#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent
csv_path = (ROOT / ".." / "datos" / "TC1002S-Dataset" / "diabetes.csv").resolve()

df = pd.read_csv(csv_path)

lines = []
lines.append("# Análisis de diabetes.csv\n")
lines.append(f"Ruta del CSV: `{csv_path}`\n")
lines.append(f"- Filas: {df.shape[0]}\n- Columnas: {df.shape[1]}\n")

lines.append("## Variables y tipos\n")
for col, dtype in df.dtypes.items():
    lines.append(f"- **{col}**: {dtype}\n")

lines.append("\n## Valores faltantes por columna\n")
na = df.isna().sum()
for col, n in na.items():
    lines.append(f"- {col}: {n}\n")

num_df = df.select_dtypes(include=[np.number]).copy()
cat_cols = [c for c in df.columns if c not in num_df.columns]

lines.append("\n## Rango (mín–máx) de variables numéricas\n")
lines.append("| Variable | Mín | Máx |\n|---|---:|---:|\n")
mins = num_df.min()
maxs = num_df.max()
for c in num_df.columns:
    lines.append(f"| {c} | {mins[c]:.3f} | {maxs[c]:.3f} |\n")

lines.append("\n## Estadísticos descriptivos (media, mediana, desviación estándar)\n")
lines.append("| Variable | Media | Mediana | Desv.Std |\n|---|---:|---:|---:|\n")
means = num_df.mean()
medians = num_df.median()
stds = num_df.std(ddof=1)
for c in num_df.columns:
    lines.append(f"| {c} | {means[c]:.3f} | {medians[c]:.3f} | {stds[c]:.3f} |\n")

# Forma / atípicos
skews = num_df.skew(numeric_only=True)
iqr = num_df.quantile(0.75) - num_df.quantile(0.25)
lower = num_df.quantile(0.25) - 1.5 * iqr
upper = num_df.quantile(0.75) + 1.5 * iqr
outliers = ((num_df.lt(lower, axis=1) | num_df.gt(upper, axis=1))).sum()

lines.append("\n## Asimetría y posibles valores atípicos (regla IQR)\n")
lines.append("| Variable | Skew | Posibles atípicos |\n|---|---:|---:|\n")
for c in num_df.columns:
    lines.append(f"| {c} | {skews[c]:.3f} | {outliers[c]} |\n")

# (Opcional) correlación con Outcome si existe
if "Outcome" in df.columns and pd.api.types.is_numeric_dtype(df["Outcome"]):
    corr = num_df.corr(numeric_only=True)["Outcome"].drop(labels=["Outcome"], errors="ignore").sort_values(ascending=False)
    lines.append("\n## Correlación con Outcome (opcional)\n")
    lines.append(corr.to_frame("corr").to_markdown() + "\n")

# Conclusiones automáticas
lines.append("\n## Conclusiones\n")
lines.append(
    "- Media, mediana y desviación estándar permiten ver tendencia central y dispersión por variable.\n"
    "- Si la **media > mediana** suele haber **asimetría positiva** (cola a la derecha); si **media < mediana**, asimetría negativa.\n"
    "- Variables con **desviación estándar alta** muestran mayor variabilidad y posibles valores extremos.\n"
    "- El conteo de **posibles atípicos (IQR)** sugiere columnas a depurar o revisar por errores de captura.\n"
)
top_std = stds.sort_values(ascending=False).head(3)
lines.append("\nVariables con mayor dispersión (top 3 por desviación estándar):\n")
for c, v in top_std.items():
    lines.append(f"- {c}: {v:.3f}\n")
top_skew = skews.abs().sort_values(ascending=False).head(3)
lines.append("\nVariables con mayor asimetría (top 3 por |skew|):\n")
for c, v in top_skew.items():
    lines.append(f"- {c}: {v:.3f}\n")

out_path = ROOT / "reporte_diabetes.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Listo. Reporte guardado en {out_path}")

