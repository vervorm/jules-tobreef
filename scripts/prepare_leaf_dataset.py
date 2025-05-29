import os
import glob
import cv2
import numpy as np
import shutil
import random
import argparse

def get_mask_path(original_image_path, root_masks_dir, image_subdir_name):
    """
    Derives the path to a mask image based on the original image path and naming convention.
    Example: IMAGES/healthy-infected/healthy/image1.jpg -> MASKS/healthy-infected/healthy/segmented_image1.jpg
    """
    base_name = os.path.splitext(os.path.basename(original_image_path))[0]
    mask_name = f"segmented_{base_name}.jpg"
    # Ensure the MASKS directory structure mirrors the IMAGES directory structure
    # e.g., MASKS/healthy-infected/healthy/ or MASKS/healthy-infected/infected/
    return os.path.join(root_masks_dir, "healthy-infected", image_subdir_name, mask_name)

def process_dataset(images_base_dir, masks_base_dir, output_base_dir, train_split_ratio):
    """
    Processes images and masks to create a YOLOv8 compatible segmentation dataset.
    """
    print(f"Starting dataset preparation...")
    print(f"Images source: {images_base_dir}")
    print(f"Masks source: {masks_base_dir}")
    print(f"Output directory: {output_base_dir}")
    print(f"Train split: {train_split_ratio}")

    # Define output paths
    train_images_path = os.path.join(output_base_dir, 'images', 'train')
    val_images_path = os.path.join(output_base_dir, 'images', 'val')
    train_labels_path = os.path.join(output_base_dir, 'labels', 'train')
    val_labels_path = os.path.join(output_base_dir, 'labels', 'val')

    # Create output directories
    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(val_images_path, exist_ok=True)
    os.makedirs(train_labels_path, exist_ok=True)
    os.makedirs(val_labels_path, exist_ok=True)
    print("Output directories created.")

    all_files_data = []
    # Assuming subdirectories like 'healthy', 'infected' are within a 'healthy-infected' parent directory
    # Adjust image_parent_subdir if your IMAGES structure is different (e.g., IMAGES/healthy, IMAGES/infected)
    image_parent_subdir = "healthy-infected" 
    
    if not os.path.isdir(os.path.join(images_base_dir, image_parent_subdir)):
        print(f"Error: Expected directory structure {os.path.join(images_base_dir, image_parent_subdir)} not found.")
        return

    for class_subdir in os.listdir(os.path.join(images_base_dir, image_parent_subdir)):
        class_subdir_path = os.path.join(images_base_dir, image_parent_subdir, class_subdir)
        if not os.path.isdir(class_subdir_path):
            continue # Skip files, only process directories like 'healthy', 'infected'
        
        print(f"Processing images from: {class_subdir_path}")
        # Glob for common image types. Adjust if you have other types like .png, .jpeg
        image_paths = glob.glob(os.path.join(class_subdir_path, "*.jpg")) + \
                      glob.glob(os.path.join(class_subdir_path, "*.JPG")) + \
                      glob.glob(os.path.join(class_subdir_path, "*.png")) + \
                      glob.glob(os.path.join(class_subdir_path, "*.PNG"))


        for img_path in image_paths:
            # 'class_subdir' here corresponds to 'image_subdir_name' in get_mask_path
            # (e.g., 'healthy' or 'infected')
            mask_path = get_mask_path(img_path, masks_base_dir, class_subdir)
            
            if os.path.exists(mask_path):
                all_files_data.append({'image': img_path, 'mask': mask_path, 'original_subdir': class_subdir})
            else:
                print(f"Warning: Mask not found for {img_path} at expected path {mask_path}. Skipping.")
    
    if not all_files_data:
        print("Error: No image-mask pairs found. Please check your IMAGES and MASKS directory structures and paths.")
        return

    random.shuffle(all_files_data)
    split_index = int(len(all_files_data) * train_split_ratio)
    train_data = all_files_data[:split_index]
    val_data = all_files_data[split_index:]

    print(f"Total image-mask pairs: {len(all_files_data)}")
    print(f"Training set size: {len(train_data)}")
    print(f"Validation set size: {len(val_data)}")

    processed_train_count = 0
    processed_val_count = 0

    for i, item_data in enumerate(all_files_data):
        is_train = i < split_index
        
        target_image_dir = train_images_path if is_train else val_images_path
        target_label_dir = train_labels_path if is_train else val_labels_path

        original_image_path = item_data['image']
        mask_path = item_data['mask']
        
        # Load original image to get dimensions
        img_bgr = cv2.imread(original_image_path)
        if img_bgr is None:
            print(f"Warning: Could not read image {original_image_path}. Skipping.")
            continue
        img_height, img_width = img_bgr.shape[:2]

        mask_gray = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask_gray is None:
            print(f"Warning: Could not read mask {mask_path} for image {original_image_path}. Skipping.")
            continue

        # Threshold the mask. Assuming mask pixels are > 0 for the object.
        _, thresh_mask = cv2.threshold(mask_gray, 1, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Optionally, select the largest contour if there could be multiple or noise
            contour = max(contours, key=cv2.contourArea)
            
            # Normalize contour points for YOLO format (class_id x1 y1 x2 y2 ... xN yN)
            yolo_points_str_list = []
            for point in contour:
                x_norm = point[0][0] / img_width
                y_norm = point[0][1] / img_height
                yolo_points_str_list.append(f"{x_norm:.6f}") # Keep 6 decimal places
                yolo_points_str_list.append(f"{y_norm:.6f}")
            
            yolo_label_line = f"0 {' '.join(yolo_points_str_list)}" # Class 0 for 'leaf'
            
            # Save label file
            base_filename = os.path.splitext(os.path.basename(original_image_path))[0]
            label_filename = f"{base_filename}.txt"
            label_filepath = os.path.join(target_label_dir, label_filename)
            
            with open(label_filepath, 'w') as f:
                f.write(yolo_label_line + "\n")
            
            # Copy original image to target directory
            image_dest_path = os.path.join(target_image_dir, os.path.basename(original_image_path))
            shutil.copy2(original_image_path, image_dest_path)

            if is_train:
                processed_train_count += 1
            else:
                processed_val_count += 1
        else:
            print(f"Warning: No contours found in mask {mask_path} for image {original_image_path}. Skipping.")

    print("\n--- Summary ---")
    print(f"Training images processed and copied: {processed_train_count}")
    print(f"Validation images processed and copied: {processed_val_count}")
    print(f"Training labels generated: {processed_train_count}")
    print(f"Validation labels generated: {processed_val_count}")
    print("Dataset preparation complete.")
    print(f"YOLO dataset created at: {output_base_dir}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prepare leaf dataset for YOLOv8 segmentation.")
    parser.add_argument('--images_dir', type=str, default='IMAGES', 
                        help='Path to the root IMAGES directory (containing "healthy-infected" subdir). Default: IMAGES')
    parser.add_argument('--masks_dir', type=str, default='MASKS',
                        help='Path to the root MASKS directory (containing "healthy-infected" subdir). Default: MASKS')
    parser.add_argument('--output_dir', type=str, default='datasets/leaf_segmentation',
                        help='Path to the output directory for the YOLO dataset. Default: datasets/leaf_segmentation')
    parser.add_argument('--train_split', type=float, default=0.8,
                        help='Float value for training split ratio. Default: 0.8')
    
    args = parser.parse_args()
    
    # Basic validation for input directories
    if not os.path.isdir(args.images_dir):
        print(f"Error: Images directory '{args.images_dir}' not found.")
        exit(1)
    if not os.path.isdir(args.masks_dir):
        print(f"Error: Masks directory '{args.masks_dir}' not found.")
        exit(1)

    process_dataset(args.images_dir, args.masks_dir, args.output_dir, args.train_split)
```
