from pathlib import Path

import joblib
import typer

from .model import train_model


app = typer.Typer()

@app.command()
def train(train_data_path: Path, model_output_path: Path):
    """Train the model on the given dataset."""

    # Train the model.
    model = train_model(train_data_path)

    # Save the trainged model.
    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_output_path)
