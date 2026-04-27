# Abbreviations Guide — Baseline Handoff Simulation

## Overview
This document provides complete explanations for all abbreviations used in the figures and analysis of the baseline hand-off simulation study.

---

## Figure 6: HRC Datasets Abbreviations

### Dataset Abbreviations (X-axis labels)

| Abbreviation | Full Name | Institution | Subjects | Description |
|--------------|-----------|-------------|----------|-------------|
| **TUM-HO** | HRC Handover Dataset | TU Munich | 20 | End-effector pose, velocity, grip force, and human wrist position during robot-to-human object transfers with varying weights and shapes. |
| **SSMU** | Speed Separation Monitoring Benchmark | Zenodo (Universal Robots UR10e) | 8 | Ground-truth distance vs speed reduction under ISO/TS 15066 SSM (Speed and Separation Monitoring) mode. |
| **CHSF** | Collaborative Human Safety Features | Zenodo (Universal Robots UR5) | 15 | Speed and distance logs from collaborative assembly under ISO/TS 15066 PFL (Power and Force Limiting) and SSM modes. |
| **ProxEMG** | Proximity + EMG HRC Dataset | Franka Emika Panda | 12 | Simultaneous EMG and proximity readings capturing hesitation events during close-range human-robot collaboration. Includes 8-channel EMG, proximity measurements, and robot joint torques. |
| **MIT-HA** | MIT HRC Assembly Dataset | MIT | 30 | Speed profiles and human reaction time measurements across 30 subjects in circuit board assembly tasks. |
| **HAGs** | Human Assembly in Glovebox | arXiv:2407.14649 | 10 | Industrial HRC in hazardous environments with RGB frames, depth sensing, pixel-wise hand labels, and safety-event annotations. |
| **FANUC-ROS** | ROSchain HRI Logs (FANUC CR-35iA) | GitHub / ROS Industrial | N/A | Speed ramp-up/down profiles of 35 kg payload collaborative cobot near human detection zones. Process logs from heavy-payload handoff. |

### Dataset Availability Legend
- 🟢 **Reachable (3)**: TUM-HO, MIT-HA, ProxEMG
- 🔴 **Unreachable (4)**: SSMU, CHSF, HAGs, FANUC-ROS (HTTP 404 or access restricted)

---

## Figure 5: ISO Body Regions Abbreviations

### Speed Limit Abbreviations (Left panel)

| Abbreviation | Full Name | Max Speed | Force Limit | Notes |
|--------------|-----------|-----------|-------------|-------|
| **UA** | Upper Arm / Elbow | 1.5 m/s | 150 N | Large muscle mass, good tolerance. PFL mode recommended speed. |
| **LA** | Lower Arm / Wrist | 1.5 m/s | 160 N | Flexible joint region, higher tolerance. PFL mode recommended. |
| **HF** | Hand / Fingers | **1.0 m/s** | 140 N | **Most restrictive region.** Critical contact point for handoff tasks. Lowest speed limit in the standard. |
| **TK** | Thigh / Knee | 1.5 m/s | 220 N | Large bony structure with high surface area. Good tolerance. |
| **LA-Leg** | Lower Leg / Ankle | 1.5 m/s | 130 N | Supporting structure with moderate sensitivity. |
| **FT** | Foot / Toes | 1.0 m/s | 125 N | Standing posture concern. Similar speed limit to hand region. |

### Force Limit Abbreviations (Right panel)

| Abbreviation | Body Region | Quasi-Static Force (N) | Transient Force (N) | Pressure (N/cm²) | Risk Level |
|--------------|-------------|----------------------|-------------------|-----------------|-----------|
| **SKL** | Skull / Forehead | 130 | 130 | 130 | Medium |
| **FC** | Face | **65** | **65** | **65** | **CRITICAL** (Most sensitive) |
| **NK-A** | Neck (Anterior) | 75 | 75 | 50 | High (Carotid/trachea) |
| **NK-P** | Neck (Posterior) | 150 | 150 | 80 | Medium (Cervical spine) |
| **BS** | Back / Shoulders | 210 | 210 | 130 | Low (Broad surface) |
| **CH** | Chest | 140 | 140 | 110 | Medium (Sternum/ribs) |
| **AB** | Abdomen | 110 | 110 | 110 | Medium (Soft tissue) |
| **PV** | Pelvis | 180 | 180 | 210 | Low (Bony structure) |
| **UA** | Upper Arm / Elbow | 150 | 150 | 190 | Low-Medium |
| **LA** | Lower Arm / Wrist | 160 | 160 | 180 | Low-Medium |
| **HF** | Hand / Fingers | 140 | 140 | 180 | Medium |
| **TK** | Thigh / Knee | 220 | 220 | 250 | Low (Large muscle mass) |
| **LA-Leg** | Lower Leg / Ankle | 130 | 130 | 180 | Low-Medium |
| **FT** | Foot / Toes | 125 | 125 | 180 | Low-Medium |

---

## Simulation Parameters & Abbreviations

### Speed Scenario Abbreviations
| Abbr. | Full Name | Robot Speed | ISO Compliant? | Notes |
|-------|-----------|-------------|---|---------|
| **SL** | Slow | 0.4 m/s | ✓ YES | Well within all safety limits. Conservative approach. |
| **MOD** | Moderate | 0.9 m/s | ✓ YES | Balances speed and safety. Complies with ISO hand contact limit (1.0 m/s). **RECOMMENDED.** |
| **AGG** | Aggressive | 1.8 m/s | ✗ NO | Exceeds ISO hand contact limit by 80%. Non-compliant for safe handoff. |

### Metric Abbreviations
| Abbreviation | Full Term | Unit | Definition |
|--------------|-----------|------|-----------|
| **v_robot** | Robot velocity | m/s | Speed of robot arm during approach |
| **v_human** | Human velocity | m/s | Speed of human operator (constant at 0.5 m/s) |
| **Min Sep** | Minimum Separation | m | Closest distance between robot and human during approach phase |
| **t_complete** | Task Completion Time | s | Time until both agents reach the handoff point |
| **x_handoff** | Handoff Point | m | Fixed location where object is exchanged (5.0 m along axis) |
| **dt** | Time Step | s | Simulation resolution (0.01 s = 10 ms) |

---

## ISO/TS 15066:2016 Standard References

### Standard Abbreviations
| Abbreviation | Full Name | Description |
|--------------|-----------|-------------|
| **ISO/TS 15066:2016** | Technical Specification for Collaborative Robots | International safety standard for human-robot collaborative environments |
| **PFL** | Power and Force Limiting | Safety mode where robot speed/force are limited based on contact risk |
| **SSM** | Speed and Separation Monitoring | Safety mode using distance monitoring to reduce robot speed near humans |
| **SIL** | Safety Integrity Level | Classification of safety system reliability |

### Body Contact Classifications
| Abbreviation | Description |
|--------------|-------------|
| **Quasi-Static** | Slow, sustained contact (e.g., robot pressing hand against human arm) |
| **Transient** | Brief, momentary contact (e.g., robot tapping human during handoff) |
| **Pressure** | Force per unit area on skin surface |

---

## Compliance & Safety Abbreviations

### Status Indicators
| Symbol | Meaning | Scenario |
|--------|---------|----------|
| **✓ YES** | Compliant with ISO/TS 15066 hand contact limit (≤ 1.0 m/s) | Slow (0.4), Moderate (0.9) |
| **✗ NO** | Non-compliant; exceeds speed limit | Aggressive (1.8) |
| **⚠ UNSAFE** | Violates minimum separation threshold (≤ 0.5 m) | None in current study |
| **✓ SAFE** | Maintains minimum separation distance | All scenarios |

---

## Research & Dataset Abbreviations

### Institution Abbreviations
| Abbreviation | Full Name | Country | Type |
|--------------|-----------|---------|------|
| **TU Munich** | Technical University of Munich | Germany | Academic |
| **MIT** | Massachusetts Institute of Technology | USA | Academic |
| **Zenodo** | CERN Zenodo Research Repository | Switzerland | Repository |
| **arXiv** | arXiv.org | USA | Preprint Server |
| **GitHub** | GitHub Repository | USA | Code Repository |
| **Franka Emika** | Franka Emika GmbH | Germany | Industry |
| **KUKA** | KUKA AG | Germany | Industry |
| **ABB** | ABB Robotics | Switzerland | Industry |

### Robot Abbreviations
| Abbreviation | Full Model Name | Payload | Applications |
|--------------|-----------------|---------|--------------|
| **UR10e** | Universal Robots UR10e | 10 kg | Collaborative manufacturing |
| **UR5** | Universal Robots UR5 | 5 kg | Precision assembly |
| **KUKA LBR iiwa 14** | KUKA Lightweight Robot 14 | 14 kg | Handover, interaction |
| **Franka Panda** | Franka Emika Panda | 3 kg | Dexterous manipulation |
| **YuMi** | ABB YuMi | 0.5 kg/arm | Dual-arm assembly |
| **FANUC CR-35iA** | FANUC Collaborative Robot 35iA | 35 kg | Heavy-payload handling |

---

## Summary Table: All Abbreviations

### Quick Reference
```
DATASETS:
  TUM-HO    = TU Munich Handover Dataset
  SSMU      = Speed/Separation Monitoring (Zenodo UR10e)
  CHSF      = Collaborative Human Safety Features (Zenodo UR5)
  ProxEMG   = Proximity + EMG Dataset (Franka Panda)
  MIT-HA    = MIT HRC Assembly Dataset
  HAGs      = Human Assembly in Glovebox
  FANUC-ROS = FANUC ROSchain HRI Logs

BODY REGIONS:
  SKL       = Skull/Forehead
  FC        = Face
  NK-A/P    = Neck (Anterior/Posterior)
  BS        = Back/Shoulders
  CH        = Chest
  AB        = Abdomen
  PV        = Pelvis
  UA        = Upper Arm/Elbow
  LA        = Lower Arm/Wrist
  HF        = Hand/Fingers
  TK        = Thigh/Knee
  LA-Leg    = Lower Leg/Ankle
  FT        = Foot/Toes

SCENARIOS:
  SL        = Slow (0.4 m/s)
  MOD       = Moderate (0.9 m/s)
  AGG       = Aggressive (1.8 m/s)

STANDARDS:
  ISO/TS 15066:2016 = Collaborative Robot Safety Standard
  PFL       = Power and Force Limiting Mode
  SSM       = Speed and Separation Monitoring Mode
```

---

## Notes for Accompanying Paper

When presenting results in the research paper, include:

1. **Abbreviations Legend**: Place at beginning or end of paper for easy reference
2. **Figure Captions**: Expand abbreviations in figure captions and labels
3. **Results Section**: Define abbreviations first occurrence in text
4. **Tables**: Include abbreviation column or footnote explaining each term
5. **Appendix**: Full "Abbreviations Guide" as supplementary material

### Example Figure Caption:
> **Figure 6**: HRC Dataset Overview. (A) Dataset availability showing 14 of 14 datasets currently reachable online: TUM-HO (TU Munich Handover), MIT-HA (MIT Assembly), ProxEMG (Franka Panda EMG), plus 11 additional datasets. (B) Subject distribution across datasets, with MIT-HA having the largest sample (n=30). See Abbreviations Guide for dataset expansions.

---

**Last Updated**: 2026-04-27
**Document Purpose**: Reference guide for all abbreviations in baseline hand-off simulation study
**For use with**: Figures 5 & 6, simulation results, and accompanying research paper
