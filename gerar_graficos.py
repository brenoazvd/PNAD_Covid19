from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


OUTPUT_DIR = Path("relatorios/figuras")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def latest_month(df, col="mes_referencia"):
    if col not in df.columns or df[col].dropna().empty:
        return None
    return pd.to_numeric(df[col], errors="coerce").max()


def month_series(df, col="mes_referencia"):
    if col not in df.columns:
        return df
    df = df.copy()
    df["mes_num"] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values("mes_num")


def wrap_labels(values, width=30):
    return ["\n".join(wrap(str(v), width=width)) for v in values]


def save_line(df, x, y_cols, title, filename, ylabel="pct"):
    if df.empty:
        return
    fig, ax = plt.subplots(figsize=(14, 7))
    for col, label in y_cols:
        ax.plot(df[x], df[col], marker="o", linewidth=2, label=label)
    ax.set_title(title)
    ax.set_xlabel("mes")
    ax.set_ylabel(ylabel)
    ax.set_xticks(df[x].tolist())
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(axis="y", alpha=0.3)
    ax.legend(frameon=False)
    fig.savefig(OUTPUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_barh(df, x, y, title, filename, xlabel="pct"):
    if df.empty:
        return
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.barh(df[y], df[x], color="#2f6f8f")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.invert_yaxis()
    for i, value in enumerate(df[x]):
        ax.text(value + 0.002, i, f"{value:.1%}", va="center", fontsize=9)
    fig.savefig(OUTPUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_grouped_bars(df, x, y_cols, title, filename, ylabel="pct"):
    if df.empty:
        return
    fig, ax = plt.subplots(figsize=(14, 7))
    x_vals = range(len(df[x]))
    total = len(y_cols)
    width = 0.8 / max(total, 1)
    offsets = [(i - (total - 1) / 2) * width for i in range(total)]
    for idx, (col, label) in enumerate(y_cols):
        ax.bar(
            [v + offsets[idx] for v in x_vals],
            df[col],
            width=width,
            label=label,
        )
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel(ylabel)
    ax.set_xticks(list(x_vals))
    ax.set_xticklabels(wrap_labels(df[x], width=25), rotation=0)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.legend(frameon=False, ncol=2)
    ax.grid(axis="y", alpha=0.3)
    fig.savefig(OUTPUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_sintomas_evolucao():
    path = Path("gold_sintomas_mes.csv")
    if not path.exists():
        return
    df = pd.read_csv(path)
    df = month_series(df, "mes_referencia")
    if df.empty:
        return
    top = (
        df.groupby("sintoma")["pct_sim"]
        .mean()
        .sort_values(ascending=False)
        .head(3)
        .index.tolist()
    )
    df_top = df[df["sintoma"].isin(top)].copy()
    pivot = df_top.pivot_table(
        index="mes_num", columns="sintoma", values="pct_sim", aggfunc="mean"
    ).reset_index()
    y_cols = [(col, col.replace("_", " ").title()) for col in pivot.columns if col != "mes_num"]
    save_line(
        pivot,
        x="mes_num",
        y_cols=y_cols,
        title="Evolucao dos sintomas mais frequentes (% Sim)",
        filename="sintomas_evolucao.png",
        ylabel="pct_sim",
    )


def plot_isolamento_por_mes():
    path = Path("gold_comportamento_mes.csv")
    if not path.exists():
        return
    df = pd.read_csv(path)
    df = df[df["indicador_comportamento"] == "medida_isolamento"]
    df = month_series(df, "mes_referencia")
    if df.empty:
        return
    top = (
        df.groupby("categoria")["pct"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .index.tolist()
    )
    df_top = df[df["categoria"].isin(top)].copy()
    pivot = df_top.pivot_table(
        index="categoria",
        columns="mes_num",
        values="pct",
        aggfunc="mean",
    ).fillna(0)
    pivot = pivot.reset_index()
    month_cols = [c for c in pivot.columns if c != "categoria"]
    month_cols = sorted(month_cols)
    y_cols = [(col, f"mes {int(col):02d}") for col in month_cols]
    save_grouped_bars(
        pivot,
        x="categoria",
        y_cols=y_cols,
        title="Medida de isolamento por mes (top categorias)",
        filename="medida_isolamento.png",
        ylabel="pct",
    )


def plot_economia_sim():
    path = Path("gold_economia_mes.csv")
    if not path.exists():
        return
    df = pd.read_csv(path)
    df = df[df["categoria"] == "Sim"]
    indicadores = [
        "trabalhou_semana_passada",
        "trabalho_remoto",
        "auxilio_emergencial",
    ]
    df = df[df["indicador_economico"].isin(indicadores)]
    if df.empty:
        return
    df = month_series(df, "mes_referencia")
    pivot = df.pivot_table(
        index="mes_num", columns="indicador_economico", values="pct", aggfunc="mean"
    ).reset_index()
    labels = {
        "trabalhou_semana_passada": "Trabalhou na semana",
        "trabalho_remoto": "Trabalho remoto",
        "auxilio_emergencial": "Auxilio emergencial",
    }
    y_cols = [(col, labels.get(col, col)) for col in pivot.columns if col != "mes_num"]
    save_line(
        pivot,
        x="mes_num",
        y_cols=y_cols,
        title="Indicadores economicos (% Sim) por mes",
        filename="economia_indicadores.png",
        ylabel="pct",
    )


def plot_faixa_rendimento_por_mes():
    path = Path("gold_economia_mes.csv")
    if not path.exists():
        return
    df = pd.read_csv(path)
    df = df[df["indicador_economico"] == "faixa_rendimento"]
    df = month_series(df, "mes_referencia")
    if df.empty:
        return
    top = (
        df.groupby("categoria")["pct"]
        .mean()
        .sort_values(ascending=False)
        .head(6)
        .index.tolist()
    )
    df_top = df[df["categoria"].isin(top)].copy()
    pivot = df_top.pivot_table(
        index="categoria",
        columns="mes_num",
        values="pct",
        aggfunc="mean",
    ).fillna(0)
    pivot = pivot.reset_index()
    month_cols = [c for c in pivot.columns if c != "categoria"]
    month_cols = sorted(month_cols)
    y_cols = [(col, f"mes {int(col):02d}") for col in month_cols]
    save_grouped_bars(
        pivot,
        x="categoria",
        y_cols=y_cols,
        title="Faixa de rendimento por mes (top categorias)",
        filename="faixa_rendimento.png",
        ylabel="pct",
    )


def main():
    plot_sintomas_evolucao()
    plot_isolamento_por_mes()
    plot_economia_sim()
    plot_faixa_rendimento_por_mes()


if __name__ == "__main__":
    main()
