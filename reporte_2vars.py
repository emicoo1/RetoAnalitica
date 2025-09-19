#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- ELIGE AQUÍ TUS DOS VARIABLES ----------
VAR1 = "BMI"   # cambia si prefieres otras (no usar: Glucose, BloodPressure, Pregnancies, Insulin)
VAR2 = "Age"
# --------------------------------------------------

ROOT = Path.cwd()
CSV = (ROOT / ".." / "datos" / "TC1002S-Dataset" / "diabetes.csv").resolve()
OUT_MD = ROOT / "reporte_dos_variables.md"
OUT_HTML = ROOT / "reporte_dos_variables.html"
FIGDIR = ROOT / "figs_2vars"
FIGDIR.mkdir(exist_ok=True)

# --- leer datos ---
if not CSV.exists():
    raise FileNotFoundError(f"No se encontró el CSV en: {CSV}")
df = pd.read_csv(CSV)

use_cols = [VAR1, VAR2]
fisiologicas = {"Glucose","BloodPressure","SkinThickness","Insulin","BMI"}
dfc = df.copy()
for c in use_cols:
    if c in fisiologicas:
        dfc[c] = dfc[c].replace(0, np.nan)
        dfc[c] = dfc[c].fillna(dfc[c].median())

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (8,4)

# ---- helpers para explicación corta ----
def clas_sesgo(skew):
    a = abs(skew)
    if a < 0.15: return "casi simétrica"
    return "sesgada a la derecha" if skew > 0 else "sesgada a la izquierda"

def rango_text(s):
    return f"[{s.min():.2f}, {s.max():.2f}]"

def iqr_stats(series):
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
    outliers = ((series < lower) | (series > upper)).sum()
    return q1, q3, iqr, lower, upper, int(outliers)

def df_to_md(dfi, title):
    try:
        md = dfi.to_markdown(index=True)
    except Exception:
        md = "```\n" + dfi.to_string() + "\n```"
    return f"\n**{title}**\n\n{md}\n"

lines = []
lines.append(f"# Reporte — Dos variables: {VAR1} y {VAR2}\n")
lines.append("## Visualización y Análisis de Datos (2 variables)\n")

desc = pd.DataFrame({
    "min": dfc[use_cols].min(),
    "max": dfc[use_cols].max(),
    "mean": dfc[use_cols].mean(),
    "median": dfc[use_cols].median(),
    "std": dfc[use_cols].std(ddof=1),
    "skew": dfc[use_cols].skew()
}).round(3)

# ---------- por cada variable: barras, hist, box con explicación ----------
for var in use_cols:
    s = dfc[var].dropna()
    mean, median, std, skew = s.mean(), s.median(), s.std(ddof=1), s.skew()
    sesgo_txt = clas_sesgo(skew)
    q1, q3, iqr, lo, hi, n_out = iqr_stats(s)

    # Barras por bins
    bins = np.linspace(s.min(), s.max(), 11) if s.min() != s.max() else np.array([s.min()-0.5, s.max()+0.5])
    cat = pd.cut(s, bins=bins, include_lowest=True)
    vc = cat.value_counts().sort_index()
    ax = vc.plot(kind="bar")
    ax.set_title(f"Diagrama de barras por bins — {var}")
    ax.set_xlabel("Bin (min–max)"); ax.set_ylabel("Frecuencia")
    plt.tight_layout(); plt.savefig(FIGDIR / f"bar_{var}.png", dpi=150, bbox_inches="tight"); plt.close()
    # explicación barras
    top_bin = vc.idxmax()
    top_cnt = int(vc.max())
    top_pct = 100 * top_cnt / len(s)
    lines.append(f"\n**Diagrama de barras — {var}**\n\n![](figs_2vars/bar_{var}.png)\n")
    lines.append(f"_Explicación_: La mayor concentración está en el bin **{top_bin}** "
                 f"({top_cnt} obs, {top_pct:.1f}%). Rango total {rango_text(s)}, media {mean:.2f}, mediana {median:.2f}.\n")

    # Histograma
    sns.histplot(data=dfc, x=var, kde=True, bins=30)
    plt.title(f"Histograma — {var}"); plt.xlabel(var); plt.ylabel("Frecuencia")
    plt.tight_layout(); plt.savefig(FIGDIR / f"hist_{var}.png", dpi=150, bbox_inches="tight"); plt.close()
    lines.append(f"\n**Histograma — {var}**\n\n![](figs_2vars/hist_{var}.png)\n")
    lines.append(f"_Explicación_: Distribución {sesgo_txt} (skew={skew:.2f}); "
                 f"dispersión (std={std:.2f}). La media vs mediana sugiere {'cola derecha' if mean>median else 'cola izquierda' if mean<median else 'simetría'}.\n")

    # Caja y bigotes
    sns.boxplot(x=dfc[var], orient="h")
    plt.title(f"Caja y Bigotes — {var}"); plt.xlabel(var)
    plt.tight_layout(); plt.savefig(FIGDIR / f"box_{var}.png", dpi=150, bbox_inches="tight"); plt.close()
    lines.append(f"\n**Caja y Bigotes — {var}**\n\n![](figs_2vars/box_{var}.png)\n")
    lines.append(f"_Explicación_: Mediana {median:.2f}, Q1={q1:.2f}, Q3={q3:.2f} (IQR={iqr:.2f}). "
                 f"Posibles atípicos (regla IQR): **{n_out}**. Umbrales: [{lo:.2f}, {hi:.2f}].\n")

# ---------- Heatmap (2 variables) + explicación ----------
corr = dfc[use_cols].corr(numeric_only=True)
plt.figure(figsize=(4.5,3.8))
sns.heatmap(corr, annot=True, fmt=".3f", cmap="coolwarm", center=0, square=True)
plt.title("Mapa de calor (2 variables)")
plt.tight_layout(); plt.savefig(FIGDIR / "heatmap_2vars.png", dpi=150, bbox_inches="tight"); plt.close()
r = corr.loc[use_cols[0], use_cols[1]]
fza = ("alta" if abs(r)>=0.7 else "moderada" if abs(r)>=0.4 else "baja")
signo = "positiva" if r >= 0 else "negativa"
lines.append("\n**Mapa de calor (correlación entre las dos variables)**\n\n![](figs_2vars/heatmap_2vars.png)\n")
lines.append(f"_Explicación_: Corr({use_cols[0]}, {use_cols[1]}) = **{r:.3f}** → correlación **{fza} {signo}**.\n")

# ---------- Tablas y respuestas resumidas ----------
lines.append(df_to_md(desc, "Rangos y estadísticos (solo 2 variables)"))

# Outliers por IQR (resumen)
outlier_counts = {}
for var in use_cols:
    _, _, _, lo, hi, n_out = iqr_stats(dfc[var].dropna())
    outlier_counts[var] = n_out
out_df = pd.DataFrame.from_dict(outlier_counts, orient="index", columns=["posibles_atipicos_IQR"])
lines.append(df_to_md(out_df, "Atípicos por IQR (conteo)"))

rangos_txt = "\n".join([f"- **{c}**: min={desc.loc[c,'min']}, max={desc.loc[c,'max']}" for c in use_cols])
atip_txt = "\n".join([f"- **{c}**: {outlier_counts[c]}" for c in use_cols])

respuestas = f"""
### Respuestas — Visualización y Análisis (solo {use_cols[0]} y {use_cols[1]})

**1) ¿Hay alguna variable que no aporta información?**  
Ninguna muestra varianza ~0; ambas aportan variabilidad.

**2) Si tuvieras que eliminar variables, ¿cuáles y por qué?**  
Eliminación solo si hubiera varianza casi nula o correlación ~1 con otra variable; con estas dos no aplica.

**3) Rangos (min–max):**  
{rangos_txt}

**4) ¿Existen datos atípicos?**  
(Criterio IQR)\n{atip_txt}

**5) ¿Existe correlación alta?**  
Corr({use_cols[0]}, {use_cols[1]}) = {r:.3f} → {fza} {signo}.
"""
lines.append(respuestas + "\n")

# --- escribir MD y HTML ---
OUT_MD.write_text("".join(lines), encoding="utf-8")
print(f"OK -> {OUT_MD}")

try:
    import markdown
    html_body = markdown.markdown(OUT_MD.read_text(encoding='utf-8'), extensions=["tables"])
    OUT_HTML.write_text("<meta charset='utf-8'>"+html_body, encoding="utf-8")
    print(f"OK -> {OUT_HTML}")
except Exception as e:
    print("HTML no generado (instala 'markdown'): ", e)

