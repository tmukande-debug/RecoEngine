from flask import Flask, render_template, request
import pandas as pd

# Sample data (Replace this with your actual data)
data1 = {
    "User ID": [25626, 26121, 26210, 26216, 26216, 26218, 26219, 26220, 26221],
    "Quality Score": [1, 3, 7, 7, 7, 7, 7, 6, 7],
    "AWC Per Hour": [612, 72, 720, 1620, 1872, 1548, 1080, 828, 5148],
    "Cost Per Word": [0.1012, "#N/A", 0.0975, 0.0911, 0.0911, 0.0948, 0.0958, 0.0867, 0.1034],
    "sourceCode": ["it-IT", "fr-FR", "es-ES", "cs-CZ", "cs-CZ", "de-DE", "de-DE", "de-DE", "el-GR"],
    "targetCode": ["en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US"],
}

data2 = {
    "sourceCode": ["en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US", "en-US"],
    "targetCode": ["id-ID", "id-ID", "id-ID", "id-ID", "id-ID", "id-ID", "id-ID", "id-ID", "hi-IN", "hi-IN", "hi-IN", "hi-IN", "id-ID", "id-ID", "id-ID", "id-ID"],
    "SubTenant": ["MinecraftMarketplaceAll", "MinecraftMarketplaceAll", "MinecraftMarketplaceAll", "MinecraftMarketplaceAll", "MinecraftMarketplaceAll", "MinecraftMarketplaceAll", "MinecraftBackendWorlds3", "MinecraftMarketplaceAll", "CardinalUI", "CardinalUI", "GamesBoston", "GamesBoston", "MinecraftMarketplaceAll", "MinecraftMarketplaceAll", "MinecraftMarketplaceAll", "Minecraft"],
    "User ID": [26253, 26253, 26253, 26255, 26255, 26255, 26255, 26255, 26252, 26252, 26252, 26252, 26253, 26253, 26253, 26253],
    "User Completed Tasks": [80, 8, 2, 21, 35, 31, 1, 39, 6, 2, 2, 3, 15, 8, 18, 1],
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Merge the two dataframes
merged_df = df1.merge(df2, on=["sourceCode", "targetCode", "User ID"], how="inner")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    sourceCode_options = df2["sourceCode"].unique().tolist()
    targetCode_options = df2["targetCode"].unique().tolist()
    SubTenant_options = df2["SubTenant"].unique().tolist()

    if request.method == "POST":
        selected_sourceCode = request.form["sourceCode"]
        selected_targetCode = request.form["targetCode"]
        selected_SubTenant = request.form["SubTenant"]

        filtered_df = merged_df[
            (merged_df["sourceCode"] == selected_sourceCode)
            & (merged_df["targetCode"] == selected_targetCode)
            & (merged_df["SubTenant"] == selected_SubTenant)
        ]
    else:
        filtered_df = merged_df

    ranked_candidates = filtered_df.sort_values(
        by=["Quality Score", "AWC Per Hour", "Cost Per Word", "User Completed Tasks"],
        ascending=[False, False, True, False],
    ).reset_index(drop=True)

    return render_template(
        "index.html",
        sourceCode_options=sourceCode_options,
        targetCode_options=targetCode_options,
        SubTenant_options=SubTenant_options,
        ranked_candidates=ranked_candidates.to_dict(orient="records"),
    )

if __name__ == "__main__":
    app.run(debug=True)
