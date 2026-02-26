from __future__ import annotations

from io import BytesIO

import pandas as pd

from app.utils.csv_ingestion import load_tolerant_csv

PLOT_NAMES = {
    "missing_heatmap",
    "target_distribution",
    "feature_importance",
    "numeric_distribution",
    "correlation_heatmap",
}


def _get_plt():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # noqa: WPS433

        return plt
    except Exception as exc:
        raise RuntimeError(f"matplotlib_unavailable: {exc}")


def _finalize_png(plt) -> bytes:
    buf = BytesIO()
    plt.tight_layout(pad=1.2)
    plt.savefig(buf, format="png", dpi=120, bbox_inches="tight", pad_inches=0.25)
    plt.close()
    buf.seek(0)
    return buf.read()


def _plot_missing_heatmap(df: pd.DataFrame) -> bytes:
    plt = _get_plt()
    top_missing = df.isna().mean().sort_values(ascending=False).head(15).index.tolist()
    if not top_missing:
        plt.figure(figsize=(8, 3))
        plt.text(0.5, 0.5, "No missing values detected", ha="center", va="center")
        plt.axis("off")
        return _finalize_png(plt)
    plt.figure(figsize=(10, 4))
    matrix = df[top_missing].isna().astype(int).head(500)
    plt.imshow(matrix.T, aspect="auto", interpolation="nearest")
    plt.yticks(range(len(top_missing)), top_missing)
    plt.xlabel("Row sample")
    plt.title("Missing Data Heatmap (Top Columns)")
    return _finalize_png(plt)


def _plot_target_distribution(df: pd.DataFrame, target_column: str | None) -> bytes:
    plt = _get_plt()
    plt.figure(figsize=(8, 4))
    if not target_column or target_column not in df.columns:
        plt.text(0.5, 0.5, "Target column unavailable", ha="center", va="center")
        plt.axis("off")
        return _finalize_png(plt)
    value_counts = df[target_column].astype("string").value_counts(dropna=False).head(20)
    value_counts.plot(kind="bar")
    plt.title(f"Target Distribution: {target_column}")
    plt.ylabel("Count")
    return _finalize_png(plt)


def _plot_feature_importance(report: dict) -> bytes:
    plt = _get_plt()
    plt.figure(figsize=(8, 4))
    importances = (
        report.get("target_diagnostics", {}).get("top_predictive_features", [])
        if isinstance(report.get("target_diagnostics", {}), dict)
        else []
    )
    if not importances:
        plt.text(0.5, 0.5, "Feature importance unavailable", ha="center", va="center")
        plt.axis("off")
        return _finalize_png(plt)

    labels = [item.get("feature", "") for item in importances[:10]]
    scores = [float(item.get("score", 0.0)) for item in importances[:10]]
    plt.barh(labels[::-1], scores[::-1])
    plt.title("Top Predictive Features")
    plt.xlabel("Signal Score")
    return _finalize_png(plt)


def _plot_numeric_distributions(df: pd.DataFrame) -> bytes:
    plt = _get_plt()
    numeric_cols = df.select_dtypes(include="number").columns.tolist()[:4]
    if not numeric_cols:
        plt.figure(figsize=(8, 3))
        plt.text(0.5, 0.5, "No numeric features", ha="center", va="center")
        plt.axis("off")
        return _finalize_png(plt)
    fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(8, 2.2 * len(numeric_cols)))
    if len(numeric_cols) == 1:
        axes = [axes]
    for idx, col in enumerate(numeric_cols):
        axes[idx].hist(df[col].dropna().values, bins=30)
        axes[idx].set_title(col)
    return _finalize_png(plt)


def _plot_correlation_heatmap(df: pd.DataFrame) -> bytes:
    plt = _get_plt()
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        plt.figure(figsize=(8, 3))
        plt.text(0.5, 0.5, "No numeric features", ha="center", va="center")
        plt.axis("off")
        return _finalize_png(plt)
    corr = numeric.corr(numeric_only=True).abs()
    subset = corr.mean().sort_values(ascending=False).head(20).index.tolist()
    matrix = corr.loc[subset, subset]
    plt.figure(figsize=(8, 6))
    plt.imshow(matrix.values, interpolation="nearest")
    plt.xticks(range(len(subset)), subset, rotation=90, fontsize=7)
    plt.yticks(range(len(subset)), subset, fontsize=7)
    plt.title("Correlation Heatmap (Top Numeric Features)")
    return _finalize_png(plt)


def generate_plot_bytes(
    file_path: str,
    report: dict,
    target_column: str | None,
    plot_name: str,
) -> bytes:
    generated = generate_all_plot_bytes(
        file_path=file_path,
        report=report,
        target_column=target_column,
        requested_plot_names={plot_name},
    )
    if plot_name not in generated:
        raise ValueError(f"Unsupported plot '{plot_name}'")
    return generated[plot_name]


def generate_all_plot_bytes(
    file_path: str,
    report: dict,
    target_column: str | None,
    requested_plot_names: set[str] | None = None,
) -> dict[str, bytes]:
    plot_names = requested_plot_names or PLOT_NAMES
    unsupported = [name for name in plot_names if name not in PLOT_NAMES]
    if unsupported:
        raise ValueError(f"Unsupported plot type(s): {unsupported}")

    df, _ = load_tolerant_csv(file_path, nrows=120_000)
    output: dict[str, bytes] = {}
    if "missing_heatmap" in plot_names:
        output["missing_heatmap"] = _plot_missing_heatmap(df)
    if "target_distribution" in plot_names:
        output["target_distribution"] = _plot_target_distribution(df, target_column)
    if "feature_importance" in plot_names:
        output["feature_importance"] = _plot_feature_importance(report)
    if "numeric_distribution" in plot_names:
        output["numeric_distribution"] = _plot_numeric_distributions(df)
    if "correlation_heatmap" in plot_names:
        output["correlation_heatmap"] = _plot_correlation_heatmap(df)
    return output
