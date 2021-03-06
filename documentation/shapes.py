import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import palettable

def configure(context):
    context.stage("data.income.municipality")
    context.stage("data.spatial.zones")
    context.stage("data.bpe.cleaned")

def execute(context):
    df_zones = context.stage("data.spatial.zones")
    df_communes = df_zones[df_zones["zone_level"] == "commune"][["commune_id", "geometry"]]

    # Spatial income distribution
    df_income = context.stage("data.income.municipality")
    df_income = pd.merge(df_communes, df_income, how = "inner", on = "commune_id")
    df_income["is_imputed"] = df_income["is_imputed"].astype(np.int)
    df_income.to_file("%s/income.geojson" % context.cache_path, driver = "GeoJSON")

    # Enterprises
    df_bpe = context.stage("data.bpe.cleaned")[["enterprise_id", "geometry", "imputed_location", "commune_id"]].copy()
    df_bpe["imputed_location"] = df_bpe["imputed_location"].astype(np.int)
    df_bpe = df_bpe.iloc[np.random.choice(len(df_bpe), size = 10000, replace = False)]
    df_bpe.to_file("%s/bpe.shp" % context.cache_path)

    return context.cache_path
