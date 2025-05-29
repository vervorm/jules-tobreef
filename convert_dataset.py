import os
import shutil
import argparse
import cv2
import numpy as np
import glob
from sklearn.model_selection import train_test_split
import yaml

def parse_args():
    parser = argparse.ArgumentParser(description="Convert dataset to YOLO segmentation format.")
    parser.add_argument('--input_dir', type=str, required=True,
                        help="Path to the root DATA directory (containing IMAGES and MASKS).")
    parser.add_argument('--output_dir', type=str, required=True,
                        help="Path where the YOLO formatted dataset will be created (e.g., 'leaf_dataset_yolo').")
    parser.add_argument('--train_split', type=float, default=0.8,
                        help="Proportion of data for the training set (e.g., 0.8 for 80%% train). Validation set gets the rest. Default 0.8.")
    parser.add_argument('--seed', type=int, default=42,
                        help="Random seed for train/val split for reproducibility. Default 42.")
    return parser.parse_args()

def create_yolo_dataset(args):
    images_base_path = os.path.join(args.input_dir, 'IMAGES')
    masks_base_path = os.path.join(args.input_dir, 'MASKS')

    if not os.path.isdir(images_base_path):
        print(f"Error: IMAGES directory not found at {images_base_path}")
        return
    if not os.path.isdir(masks_base_path):
        print(f"Error: MASKS directory not found at {masks_base_path}")
        return

    # Create output directories
    output_images_train = os.path.join(args.output_dir, 'images', 'train')
    output_images_val = os.path.join(args.output_dir, 'images', 'val')
    output_labels_train = os.path.join(args.output_dir, 'labels', 'train')
    output_labels_val = os.path.join(args.output_dir, 'labels', 'val')

    for path in [output_images_train, output_images_val, output_labels_train, output_labels_val]:
        os.makedirs(path, exist_ok=True)

    image_mask_pairs = []
    
    # Using glob to find all image files, supporting various extensions
    # Search recursively in all subdirectories of IMAGES
    image_files = glob.glob(os.path.join(images_base_path, '**', '*.*'), recursive=True)
    # Filter out directories if glob includes them, ensure it's a file
    image_files = [f for f in image_files if os.path.isfile(f)]


    print(f"Found {len(image_files)} images in {images_base_path}")

    for img_path in image_files:
        try:
            # Construct relative path from IMAGES base to keep subdirectory structure
            relative_img_path = os.path.relpath(img_path, images_base_path)
            img_dirname = os.path.dirname(relative_img_path)
            img_basename, img_ext = os.path.splitext(os.path.basename(img_path))

            # Mask filename convention: segmented_{original_basename_without_extension}.jpg
            mask_filename = f"segmented_{img_basename}.jpg"
            # Mask path mirrors image path structure under MASKS directory
            mask_path = os.path.join(masks_base_path, img_dirname, mask_filename)
            
            # Fallback: if mask is not in a subfolder but directly in MASKS with the same name as image
            if not os.path.exists(mask_path):
                # This was the original simpler assumption, try it if the above fails
                # For example, if image is DATA/IMAGES/img1.jpg, mask is DATA/MASKS/segmented_img1.jpg
                # Or if image is DATA/IMAGES/folder/img1.jpg, mask is DATA/MASKS/segmented_img1.jpg (less likely with new rule)
                # The prompt implies mask subfolder structure mirrors image subfolder structure.
                # Let's try a direct segmented name in the root of MASKS if the subfolder version isn't found
                mask_path_alt = os.path.join(masks_base_path, mask_filename)
                if os.path.exists(mask_path_alt):
                    mask_path = mask_path_alt
                # else: # if specific naming like image1.jpg -> image1.jpg (mask name = image name)
                #    mask_path_alt2 = os.path.join(masks_base_path, img_dirname, f"{img_basename}{img_ext}") # mask has same name as image
                #    if os.path.exists(mask_path_alt2):
                #        mask_path = mask_path_alt2


            if os.path.exists(img_path) and os.path.exists(mask_path):
                image_mask_pairs.append((img_path, mask_path, relative_img_path))
            else:
                print(f"Warning: Image or Mask not found. Image: {img_path}, Tried Mask: {mask_path}. Skipping.")
        except Exception as e:
            print(f"Error processing path {img_path}: {e}. Skipping.")


    if not image_mask_pairs:
        print("No image-mask pairs found. Please check your input directories and naming conventions.")
        return

    train_pairs, val_pairs = [], []
    if args.train_split == 1.0:
        train_pairs = image_mask_pairs
    elif args.train_split == 0.0:
        val_pairs = image_mask_pairs
    elif 0.0 < args.train_split < 1.0:
        train_pairs, val_pairs = train_test_split(image_mask_pairs, train_size=args.train_split, random_state=args.seed)
    else:
        print(f"Error: train_split must be between 0.0 and 1.0. Got {args.train_split}")
        return

    print(f"Total pairs: {len(image_mask_pairs)}, Training pairs: {len(train_pairs)}, Validation pairs: {len(val_pairs)}")

    for split_type, pairs, output_img_dir, output_label_dir in [
        ('train', train_pairs, output_images_train, output_labels_train),
        ('val', val_pairs, output_images_val, output_labels_val)
    ]:
        if not pairs: # Skip if a split is empty (e.g. train_split=1.0 means val_pairs is empty)
            continue
        
        print(f"Processing {split_type} set...")
        for img_path, mask_path, relative_img_path in pairs:
            try:
                # Determine output image filename (preserve original extension, or convert to .jpg)
                # YOLO usually works well with .jpg. Let's keep original name for simplicity for now.
                img_filename = os.path.basename(relative_img_path) # This includes original extension
                # If subdirectories were part of relative_img_path, they are flattened here.
                # To preserve:
                # target_img_path = os.path.join(output_img_dir, relative_img_path)
                # os.makedirs(os.path.dirname(target_img_path), exist_ok=True)
                # For YOLO, flat structure in train/val is common.
                target_img_path = os.path.join(output_img_dir, img_filename)
                shutil.copy(img_path, target_img_path)

                # Process mask
                original_image_for_dims = cv2.imread(img_path)
                if original_image_for_dims is None:
                    print(f"Warning: Could not read original image {img_path} to get dimensions. Skipping.")
                    continue
                img_height, img_width = original_image_for_dims.shape[:2]

                mask_image = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
                if mask_image is None:
                    print(f"Warning: Could not read mask image {mask_path}. Skipping.")
                    continue

                contours, _ = cv2.findContours(mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                label_filename_base = os.path.splitext(img_filename)[0]
                label_path = os.path.join(output_label_dir, f"{label_filename_base}.txt")

                with open(label_path, 'w') as f_label:
                    for contour in contours:
                        if cv2.contourArea(contour) < 10: # Skip small contours
                            continue
                        
                        # Normalize contour points
                        normalized_contour = []
                        for point in contour.squeeze(axis=1): # Squeeze to remove redundant dimension
                            x_norm = point[0] / img_width
                            y_norm = point[1] / img_height
                            normalized_contour.extend([x_norm, y_norm])
                        
                        if normalized_contour:
                            f_label.write(f"0 {' '.join(map(str, normalized_contour))}\n")
            except Exception as e:
                print(f"Error processing pair ({img_path}, {mask_path}) for {split_type}: {e}")


    # Create dataset.yaml
    # The paths 'train' and 'val' should be relative to the location of dataset.yaml.
    # 'path' key is often used to specify the root of the dataset if the YAML is elsewhere,
    # but if dataset.yaml is in output_dir, then 'path: ../{args.output_dir}' or absolute path is good.
    # For Ultralytics, it's common to have dataset.yaml in the root of the dataset dir,
    # and 'train', 'val' paths are relative to this yaml file.
    
    yaml_content = {
        'path': os.path.abspath(args.output_dir), # Absolute path to the dataset directory
        'train': 'images/train',  # Relative path from dataset.yaml to train images
        'val': 'images/val',      # Relative path from dataset.yaml to val images
        'names': {
            0: 'leaf'
        }
    }
    # A simpler version if yolo command is run from parent of output_dir:
    # yaml_content_alt = {
    #    'train': os.path.join(args.output_dir, 'images/train'),
    #    'val': os.path.join(args.output_dir, 'images/val'),
    #    'names': { 0: 'leaf' }
    #}
    # However, the prompt asks for dataset.yaml to be IN output_dir.
    # So, the paths inside it should be relative to output_dir.

    yaml_path = os.path.join(args.output_dir, 'dataset.yaml')
    with open(yaml_path, 'w') as f_yaml:
        yaml.dump(yaml_content, f_yaml, sort_keys=False)

    print(f"Dataset creation complete. YOLO formatted dataset saved in: {args.output_dir}")
    print(f"Dataset configuration file: {yaml_path}")

if __name__ == "__main__":
    args = parse_args()
    create_yolo_dataset(args)
