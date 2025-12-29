# ProceduralFX - Product Requirements Document

## Project Overview

**Project Name:** ProceduralFX - Procedural City Generator  
**Version:** 1.0  
**Date:** December 2024  
**Author:** Laxman Prasad Somaraju  

---

## Executive Summary

ProceduralFX is an end-to-end procedural city generation pipeline demonstrating Technical Art skills for game development. It consists of a **Python-based asset generator** that creates 3D city geometry and a **Three.js web viewer** with real-time rendering and multiple shader styles.

---

## Problem Statement

Technical Artists in game development need to demonstrate:
- Ability to **bridge art and code**
- Proficiency in **procedural generation** and **asset pipelines**
- Understanding of **shader development** and **real-time rendering**
- Building **artist-friendly tools** with GUI controls

---

## Solution

### Architecture

```
┌─────────────────────┐     JSON      ┌─────────────────────┐
│   Python Generator  │ ───────────▶  │   Three.js Viewer   │
│   (shapes.py)       │  world.json   │   (main.js)         │
│   (world_gen.py)    │               │   (GLSL Shaders)    │
└─────────────────────┘               └─────────────────────┘
```

---

## Features Implemented

### 1. Python Asset Generator (`generator/`)

| Generator Function | Description |
|-------------------|-------------|
| `generate_skyscraper()` | 15-30 floor towers with glass facade and lit windows |
| `generate_house()` | 1-3 floor residential with pitched roof |
| `generate_shop()` | Wide commercial with storefront and awning |
| `generate_building()` | Medium buildings with window grids |
| `generate_streetlight()` | Lamp posts with glowing bulb |
| `generate_bench()` | Park benches |
| `generate_humanoid()` | Simple human figures with randomized clothing |
| `generate_pro_tree()` | Recursive fractal trees with leaves |
| `generate_crystal_cluster()` | Decorative crystal formations |
| `generate_road_segment()` | Roads with lane markings |

**Output Statistics:**
- 138 procedural objects
- 40,000+ vertices
- 60,000+ triangles
- Configurable via `CONFIG` dictionary

---

### 2. Three.js Web Viewer (`viewer/`)

#### Shader Styles

| Style | Description | Bloom |
|-------|-------------|-------|
| **Realistic** | PBR materials, standard lighting | Low (0.3) |
| **Cartoon** | Cel-shading with 4-band lighting, rim light | Medium (0.5) |
| **Neon** | Cyberpunk glow, edge detection, scanlines | High (1.2) |

#### GUI Controls (dat.GUI)

```
🎨 Visual Style
   └─ Shader: [Realistic | Cartoon | Neon]

💡 Lighting
   ├─ Ambient: 0.0 - 2.0
   ├─ Directional: 0.0 - 2.0
   └─ Exposure: 0.5 - 3.0

✨ Bloom
   ├─ Strength: 0.0 - 3.0
   └─ Radius: 0.0 - 2.0

🌍 World
   ├─ Sky Color: Color Picker
   └─ Fog Density: 0.0 - 0.02
```

#### Controls
- **WASD** - Movement
- **Mouse** - Look around (Pointer Lock)
- **GUI Panel** - Real-time adjustments

---

## Technical Specifications

### Dependencies

**Python (Generator):**
- Python 3.x
- Standard library only (json, math, random)

**JavaScript (Viewer):**
- Three.js r164
- dat.GUI 0.7.9
- Vite 5.x (build tool)

### File Structure

```
procedural_fx/
├── generator/
│   ├── shapes.py          # Mesh generators (500+ lines)
│   ├── world_gen.py       # City layout generator
│   └── output/
│       └── world.json     # Generated city data (1.2MB)
│
└── viewer/
    ├── main.js            # Three.js scene setup
    ├── index.html         # Entry point
    ├── public/assets/     # world.json copy
    └── src/shaders/
        ├── cartoon.vert/frag
        ├── neon.vert/frag
        └── hologram.vert/frag
```

---

## How to Run

### Generate City
```bash
cd procedural_fx/generator
python3 world_gen.py
cp output/world.json ../viewer/public/assets/
```

### Run Viewer
```bash
cd procedural_fx/viewer
npm install
npm run dev
# Open http://localhost:5173/
```

---

## Performance

| Metric | Value |
|--------|-------|
| FPS | 60 (stable) |
| Vertices | 40,984 |
| Triangles | 61,476 |
| Load Time | < 2 seconds |
| File Size | 1.2 MB (JSON) |

---

## Skills Demonstrated

| Skill | Implementation |
|-------|----------------|
| **Procedural Generation** | Python algorithms creating varied city layouts |
| **Shader Programming** | Custom GLSL for Cartoon/Neon effects |
| **Asset Pipelines** | Python → JSON → WebGL workflow |
| **Real-time Rendering** | Three.js with post-processing |
| **Tool Building** | dat.GUI for artist-friendly controls |
| **Performance Optimization** | 60 FPS with 40K+ vertices |

---

## Future Enhancements

- [ ] Port to Unreal Engine / Unity
- [ ] Add Maya/Houdini export
- [ ] Implement LOD (Level of Detail)
- [ ] Add building interiors
- [ ] Day/night cycle animation
- [ ] Procedural textures

---

## Conclusion

ProceduralFX demonstrates the core competencies required for a Technical Art role:
1. **Code-to-Art Pipeline** - Python generates art assets
2. **Shader Development** - Multiple visual styles in GLSL
3. **Artist Tools** - GUI controls for non-programmers
4. **Performance Awareness** - Optimized for real-time

This project is designed as a portfolio piece for the **2K Games Technical Art Graduate Program**.
