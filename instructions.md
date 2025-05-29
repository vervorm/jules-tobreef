### First:

- Do not start a VM, just give me the code,
- will do the training locally.
- Add the code to the repo (jules-tobreef/tree/feat/retrain) that I need

### What I need:

- code to retrain YOLO so it works better for detecting leafs
- add other datasets for detecting leaves if there are available and add them to the training

### Context:

- Dataset format? (COCO, YOLO, Pascal VOC, etc.)  
   =>I have a set of images so no idea what's best dataset format.
- location?  
  => local
- Preferred framework?  
  => (Open to PyTorch/YOLOv8?) suggest me the options GPU
- access?  
  => No, but can be in future
- Current project state? (Existing YOLOv8 model, or starting fresh?)  
  => YOLOv8 or YOLO11 if possible

### DATA:

```
DATA
├── IMAGES/
│   └── healthy-infected/
│       ├── healthy
│       └── infected
└── MASKS/
    └── healthy-infected/
        ├── healthy
        └── infected
```

### Mask

Relation between origin and mask:  
{original*basename}.extention => segmented*{original_basename_without_extension}.jpg

Mask Format:  
the leaf is white and the background is black one mask Class Definition in Masks there is no class definition, the classes are for an ai that will do the clasification we use the YOLO only for segmentation
