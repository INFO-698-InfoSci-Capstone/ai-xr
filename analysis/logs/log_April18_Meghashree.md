# Weekly/Bi-Weekly Log  
**Date:** April 1 - 14, 2024  
**Hours Invested:**  
| Task                      | Hours | Cumulative (3 Weeks) |  
|---------------------------|-------|-----------------------|  
| Data Collection           | 3     | 12                    |  
| Data Cleaning             | 2     | 8                     |  
| Annotation/Labeling       | 3     | 10                    |  
| Model Training (YOLOv11)  | 8     | 24                    |  
| Roboflow Implementation   | 4     | 12                    |  

## 🌹 Rose (Successes)  
1. **Roboflow Workflow Mastery**  
   - Successfully integrated Roboflow's auto-annotation tools, reducing labeling time by 40%  
   - Implemented smart preprocessing:  
     ✓ Adaptive histogram equalization  
     ✓ Custom anchor box optimization  
     ✓ Automated dataset version control  

2. **Validation Metrics**  
   - Achieved 0.78 mAP@50 on validation set for majority classes  
   - Reduced false positives by 15% through NMS threshold tuning  

## 🌱 Bud (Opportunities)  
1. **Class Imbalance Mitigation**  
   - Plan A: Implement Class-Balanced Focal Loss (α=0.8, γ=2)  
   - Plan B: Test Roboflow's oversampling with these augmentations:  
     ✓ Mosaic (20% probability)  
     ✓ CutMix (β=0.7)  
     ✓ Class-specific rotation (±15° for underrepresented classes)  

2. **Accuracy Improvement Pipeline**  
   - Experiment 1: Test YOLOv11-X vs current YOLOv11-S  
   - Experiment 2: Implement TTA (Test-Time Augmentation)  
   - Experiment 3: Curriculum learning strategy  

## 🌵 Thorn (Challenges)  
1. **Accuracy Plateau at 0.82 mAP@50**  
   - Root Cause Analysis:  
     ✓ 23% of "plastic" class FP due to reflective surfaces  
     ✓ 18% of "metal" FN in low-light conditions  

2. **Confidence Calibration Issues**  
   - Current State: 85% predictions >0.9 confidence (overconfident)  
   - Proposed Fixes:  
     ✓ Temperature scaling during inference  
     ✓ Bayesian neural network layer  

## 📌 Additional Insights  
**Key Learnings:**  
1. Data quality > quantity: Cleaned dataset improved accuracy 12% vs raw data  
2. Roboflow's synthetic data generator reduced annotation needs by 30%  

**Hardware Limitations:**  
- Current batch size 16 (max before OOM errors)  
- Training 1 epoch takes 47min (RTX 3060) vs 28min on cloud TPU  

**Next Week Priority Stack:**  
1. [High] Implement Class-Balanced Focal Loss  
2. [Med] Build lighting-invariant preprocessing pipeline  
3. [Low] Benchmark against Mask R-CNN baseline  
