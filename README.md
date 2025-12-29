# 🏙️ ProceduralFX - Procedural City Generator

**ProceduralFX** is a portfolio project demonstrating a complete procedural generation pipeline for game development. It features a Python-based backend that procedurally generates a 3D city layout (assets, buildings, environment) and a optimized Three.js web viewer for real-time rendering.

![City View](https://procedural-fx.vercel.app/) *Note: Replace with actual screenshot URL locally or after upload*

## 🚀 Features

*   **End-to-End Pipeline**: 
    *   **Python Generator**: Algorithms to create mesh data for skyscrapers, houses, shops, and street props.
    *   **Three.js Viewer**: Real-time rendering of the generated city data (~40k vertices, 60 FPS).
*   **Procedural Assets**: 
    *   Varied building types (Skyscrapers, Shops, Houses)
    *   Environmental details (Recursive fractal trees, streetlights, benches, crystals)
    *   Simple humanoid characters
*   **Advanced Shaders**: Custom GLSL shaders with real-time switching:
    *   **Realistic**: Standard PBR lighting.
    *   **Cartoon**: Cel-shading with outlines and bands.
    *   **Neon**: Cyberpunk-style glowing edges and scanlines.
*   **Interactive Controls**: Full dat.GUI panel to control lighting, bloom, fog, and visual styles.

## 🛠️ Tech Stack

*   **Backend (Generator)**: Python 3 (Standard Library: `json`, `math`, `random`)
*   **Frontend (Viewer)**: Javascript, Three.js, Vite
*   **Shaders**: GLSL (Vertex & Fragment shaders)

## 📦 How to Run Locally

### Prerequisites
*   Node.js & npm
*   Python 3.x (optional, only needed to regenerate the city)

### 1. Clone the Repository
```bash
git clone https://github.com/laxmanprasadsomaraju/procedural_fx.git
cd procedural_fx
```

### 2. Run the Web Viewer
The repository comes with a pre-generated city (`viewer/public/assets/world.json`), so you can run the viewer immediately.

```bash
cd viewer
npm install
npm run dev
```
Open the local URL (typically `http://localhost:5173`) in your browser.

### 3. (Optional) Regenerate the City
To generate a *new* random city layout:

```bash
cd ../generator
# Run the generator script
python3 world_gen.py

# Copy the new city data to the viewer assets
cp output/world.json ../viewer/public/assets/
```
Refresh your browser to see the new city!

## 🌐 How to Run Online (Deployment)

You can easily deploy this project for free using **Vercel** or **Netlify**.

### ⚡ Deploy to Vercel (Recommended)
1.  Go to [Vercel.com](https://vercel.com) and sign up/login with GitHub.
2.  Click **"Add New Project"**.
3.  Select your `procedural_fx` repository.
4.  **Important**: Configure the settings:
    *   **Root Directory**: Click "Edit" and select `viewer`. (The frontend code is inside the `viewer` folder).
    *   **Framework Preset**: It should auto-detect "Vite".
5.  Click **Deploy**.

Vercel will build the project and give you a live URL (e.g., `https://procedural-fx.vercel.app`) to share with anyone!

## 🎨 Controls
*   **WASD / Arrow Keys**: Move camera
*   **Mouse**: Look around (Click to lock cursor)
*   **GUI Panel**:
    *   Change visual style (Realistic/Cartoon/Neon)
    *   Adjust lighting and bloom intensity
    *   Change time of day (Sky color/Fog)

---
*Created by Laxman Prasad Somaraju*
