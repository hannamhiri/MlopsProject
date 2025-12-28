import mlflow
from mlflow.tracking import MlflowClient

# 🔹 MLflow DagsHub
MLFLOW_TRACKING_URI = "https://dagshub.com/hannamhiri/MlopsProject.mlflow"
DEFAULT_EXPERIMENT_ID = "0"  # DagsHub = Default

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()

# 🔹 Récupérer tous les runs FINISHED
runs = client.search_runs(
    experiment_ids=[DEFAULT_EXPERIMENT_ID],
    filter_string="attributes.status = 'FINISHED'"
)

if not runs:
    raise ValueError("❌ Aucun run terminé trouvé")


runs_with_auc = [
    r for r in runs if "roc_auc" in r.data.metrics
]

if not runs_with_auc:
    raise ValueError("❌ Aucun run avec la métrique roc_auc")


best_run = sorted(
    runs_with_auc,
    key=lambda r: r.data.metrics["roc_auc"],
    reverse=True
)[0]

best_model_uri = f"runs:/{best_run.info.run_id}/model"


with open("best_model_uri.txt", "w") as f:
    f.write(best_model_uri)

print("✅ Best model selected")
print("Run ID :", best_run.info.run_id)
print("ROC AUC :", best_run.data.metrics["roc_auc"])
print("Model URI :", best_model_uri)
