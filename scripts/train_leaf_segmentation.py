import argparse
from ultralytics import YOLO

def train_model(data_yaml_path, base_model, epochs, batch_size, img_size, project_name, run_name, patience):
    # Load a pre-trained YOLOv8 segmentation model
    # Examples: 'yolov8n-seg.pt', 'yolov8s-seg.pt', 'yolov8m-seg.pt'
    print(f"Loading base model: {base_model}")
    model = YOLO(base_model)

    print(f"Starting training with the following parameters:")
    print(f"  Data YAML: {data_yaml_path}")
    print(f"  Epochs: {epochs}")
    print(f"  Batch Size: {batch_size}")
    print(f"  Image Size: {img_size}")
    print(f"  Patience for early stopping: {patience}")
    print(f"  Project Name: {project_name}")
    print(f"  Run Name: {run_name}")
    print("Training on CPU. This might take a very long time. Consider using a GPU if available.")

    # Train the model
    results = model.train(
        data=data_yaml_path,
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        patience=patience,    # Epochs to wait for no observable improvement before stopping training
        project=project_name, # Directory to save results: project_name/run_name
        name=run_name,        # Subdirectory for this specific run
        verbose=True          # Print training progress
    )

    print("Training completed.")
    print(f"Trained model and results saved in: {results.save_dir}")
    print(f"Best model weights saved at: {model.trainer.best}") # Path to best.pt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train a YOLOv8 segmentation model for leaf detection.")
    parser.add_argument('--data_yaml', type=str, default='datasets/leaf_segmentation/leaf_dataset.yaml', help='Path to the dataset YAML file.')
    parser.add_argument('--base_model', type=str, default='yolov8n-seg.pt', help='Base model to start training from (e.g., yolov8n-seg.pt, yolov8s-seg.pt).')
    parser.add_argument('--epochs', type=int, default=100, help='Number of training epochs.')
    parser.add_argument('--batch_size', type=int, default=8, help='Batch size for training. Reduce if facing memory issues (e.g., 2 or 4 for CPU).')
    parser.add_argument('--img_size', type=int, default=640, help='Image size for training (e.g., 640).')
    parser.add_argument('--patience', type=int, default=20, help='Epochs to wait for no improvement before early stopping. 0 to disable.')
    parser.add_argument('--project_name', type=str, default='leaf_training_runs', help='Directory name to save training runs.')
    parser.add_argument('--run_name', type=str, default='exp', help='Specific name for this training run (creates a subdirectory under project_name).')

    args = parser.parse_args()

    train_model(
        data_yaml_path=args.data_yaml,
        base_model=args.base_model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        img_size=args.img_size,
        project_name=args.project_name,
        run_name=args.run_name,
        patience=args.patience
    )
```
