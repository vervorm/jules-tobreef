import argparse
import os
import yaml
from ultralytics import YOLO

def parse_args():
    """Parses command-line arguments for YOLO training."""
    parser = argparse.ArgumentParser(description="Train a YOLO segmentation model for leaf segmentation.")
    parser.add_argument('--data_yaml', type=str, required=True,
                        help="Path to the dataset.yaml file (e.g., 'leaf_dataset_yolo/dataset.yaml').")
    parser.add_argument('--model_variant', type=str, default='yolo11n-seg.pt',
                        help="Which YOLO segmentation model to use (e.g., 'yolo11n-seg.pt', 'yolov8n-seg.pt'). Default: 'yolo11n-seg.pt'.")
    parser.add_argument('--epochs', type=int, default=100,
                        help="Number of training epochs. Default: 100.")
    parser.add_argument('--batch_size', type=int, default=16,
                        help="Batch size for training. Default: 16.")
    parser.add_argument('--img_size', type=int, default=640,
                        help="Image size (width and height) for training. Default: 640.")
    parser.add_argument('--device', type=str, default='cpu',
                        help="Device to train on ('cpu', '0', '0,1,2,3', etc.). Default: 'cpu'.")
    parser.add_argument('--output_dir', type=str, default='runs/train_leaf_seg',
                        help="Directory to save training runs. This will be used as the 'project' for Ultralytics. Default: 'runs/train_leaf_seg'.")
    parser.add_argument('--project_name', type=str, default='leaf_segmentation_project',
                        help="Project name. Note: In this script, 'output_dir' is used as the main project path for Ultralytics. This argument is available but not directly passed as 'project' to YOLO.train if output_dir is used. Default: 'leaf_segmentation_project'.")
    parser.add_argument('--run_name', type=str, default='exp',
                        help="Specific name for this training run, used as the experiment name ('name') by Ultralytics. Default: 'exp'.")
    parser.add_argument('--workers', type=int, default=8,
                        help="Number of data loading workers. Default: 8.")
    parser.add_argument('--patience', type=int, default=50,
                        help="Epochs for early stopping if no improvement is observed. Default: 50.")
    parser.add_argument('--learning_rate', type=float, default=None,
                        help="Initial learning rate (e.g., 0.01). Default: None (use Ultralytics default).")
    parser.add_argument('--optimizer', type=str, default=None,
                        help="Optimizer to use (e.g., 'SGD', 'Adam', 'AdamW'). Default: None (use Ultralytics default).")

    return parser.parse_args()

def main(args):
    """Main function to train the YOLO model."""
    try:
        model = YOLO(args.model_variant)
    except Exception as e:
        print(f"Error loading model variant {args.model_variant}: {e}")
        print(f"Please ensure the model variant '{args.model_variant}' is correct, accessible, and supported by your Ultralytics version.")
        print("If 'yolo11n-seg.pt' is a custom model, ensure it's properly defined or use a standard YOLOv8 variant like 'yolov8n-seg.pt'.")
        return

    # Ensure the output_dir (which will be the project dir for YOLO) exists
    os.makedirs(args.output_dir, exist_ok=True)

    training_kwargs = {
        'data': args.data_yaml,
        'epochs': args.epochs,
        'batch': args.batch_size,
        'imgsz': args.img_size,
        'device': args.device,
        'project': args.output_dir, # Use output_dir as the project for Ultralytics
        'name': args.run_name,       # Use run_name as the name for Ultralytics
        'workers': args.workers,
        'patience': args.patience,
    }

    if args.optimizer:
        training_kwargs['optimizer'] = args.optimizer
    if args.learning_rate is not None:
        training_kwargs['lr0'] = args.learning_rate

    print(f"Starting training with the following configuration:")
    for key, value in training_kwargs.items():
        print(f"  {key}: {value}")
    # The actual save directory will be project/name, i.e., args.output_dir / args.run_name
    actual_save_dir = os.path.join(args.output_dir, args.run_name)
    print(f"Note: Training results will be saved in '{actual_save_dir}'")


    try:
        results = model.train(**training_kwargs)
        
        # results.save_dir should be args.output_dir / args.run_name
        # Construct the expected path to the best model
        best_model_path = os.path.join(args.output_dir, args.run_name, 'weights', 'best.pt')
        
        if os.path.exists(best_model_path):
            print(f"\nTraining completed successfully!")
            final_model_path = os.path.abspath(best_model_path)
            print(f"The best model weights are saved at: {final_model_path}")
        # Check results.save_dir as a more robust way if Ultralytics changes behavior slightly
        elif results and hasattr(results, 'save_dir') and os.path.exists(os.path.join(results.save_dir, 'weights', 'best.pt')):
            print(f"\nTraining completed successfully!")
            final_model_path = os.path.abspath(os.path.join(results.save_dir, 'weights', 'best.pt'))
            print(f"The best model weights are saved at: {final_model_path}")
        else:
            print(f"\nTraining completed, but could not automatically locate 'best.pt' at the expected path.")
            print(f"Please check the output directory: {os.path.abspath(actual_save_dir)}")
            final_model_path = f"{actual_save_dir}/weights/best.pt" # Placeholder for instruction

        print("\nTo use the trained model for prediction, you can use the following command:")
        print(f"yolo predict model={final_model_path} source=/path/to/your/image.jpg")
        print("\nOr using Python:")
        print("from ultralytics import YOLO")
        print(f"model = YOLO('{final_model_path}')")
        print("results = model.predict(source='/path/to/your/image.jpg')")

    except Exception as e:
        print(f"\nAn error occurred during training: {e}")
        print("Please check your dataset, arguments, and environment. Ensure PyTorch and CUDA (if using GPU) are correctly installed.")

if __name__ == '__main__':
    args = parse_args()
    
    if not os.path.exists(args.data_yaml):
        print(f"Error: data_yaml file not found at '{args.data_yaml}'. Please provide a valid path.")
    else:
        try:
            with open(args.data_yaml, 'r') as f:
                data_config = yaml.safe_load(f)
            if not data_config: 
                print(f"Error: data_yaml file '{args.data_yaml}' is empty or malformed.")
            elif not all(k in data_config for k in ['train', 'val', 'names']):
                # Proceed with warning, as 'nc' might also be used by YOLO instead of 'names' in some contexts
                print(f"Warning: The data_yaml file '{args.data_yaml}' might be missing expected keys like 'train', 'val', or 'names'. Review its content if training fails.")
                main(args) 
            else:
                main(args) 
        except yaml.YAMLError as e:
            print(f"Error parsing data_yaml file '{args.data_yaml}': {e}")
        except Exception as e: 
            print(f"Error reading data_yaml file '{args.data_yaml}': {e}")
