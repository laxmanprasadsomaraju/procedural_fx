import * as THREE from 'three';
import { PointerLockControls } from 'three/examples/jsm/controls/PointerLockControls.js';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import * as dat from 'dat.gui';

// Shaders
import cartoonVert from './src/shaders/cartoon.vert?raw';
import cartoonFrag from './src/shaders/cartoon.frag?raw';
import neonVert from './src/shaders/neon.vert?raw';
import neonFrag from './src/shaders/neon.frag?raw';
import hologramVert from './src/shaders/hologram.vert?raw';
import hologramFrag from './src/shaders/hologram.frag?raw';

// =============================================================================
// SCENE SETUP
// =============================================================================
const scene = new THREE.Scene();
const bgCol = 0x050510;
scene.background = new THREE.Color(bgCol);
scene.fog = new THREE.FogExp2(bgCol, 0.008);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 500);
camera.position.set(0, 8, 25);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);

// =============================================================================
// CONTROLS
// =============================================================================
const controls = new PointerLockControls(camera, document.body);
const blocker = document.createElement('div');
blocker.style.cssText = `
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Segoe UI', sans-serif;
    font-size: 28px;
    color: white;
    text-align: center;
    background: linear-gradient(135deg, rgba(20,20,40,0.9), rgba(40,20,60,0.9));
    padding: 30px 50px;
    border-radius: 15px;
    border: 2px solid rgba(100,100,255,0.3);
    cursor: pointer;
    box-shadow: 0 0 30px rgba(100,100,255,0.3);
`;
blocker.innerHTML = `
    <div style="font-size: 36px; margin-bottom: 10px;">🏙️ PROCEDURAL CITY</div>
    <div style="font-size: 18px; opacity: 0.8;">Click to Enter</div>
    <div style="font-size: 14px; opacity: 0.6; margin-top: 10px;">WASD to Move | Mouse to Look | GUI to Customize</div>
`;
document.body.appendChild(blocker);

blocker.addEventListener('click', () => controls.lock());
controls.addEventListener('lock', () => blocker.style.display = 'none');
controls.addEventListener('unlock', () => blocker.style.display = 'block');

// Movement
let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false;
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();

document.addEventListener('keydown', (e) => {
    switch (e.code) {
        case 'ArrowUp': case 'KeyW': moveForward = true; break;
        case 'ArrowLeft': case 'KeyA': moveLeft = true; break;
        case 'ArrowDown': case 'KeyS': moveBackward = true; break;
        case 'ArrowRight': case 'KeyD': moveRight = true; break;
    }
});
document.addEventListener('keyup', (e) => {
    switch (e.code) {
        case 'ArrowUp': case 'KeyW': moveForward = false; break;
        case 'ArrowLeft': case 'KeyA': moveLeft = false; break;
        case 'ArrowDown': case 'KeyS': moveBackward = false; break;
        case 'ArrowRight': case 'KeyD': moveRight = false; break;
    }
});

// =============================================================================
// LIGHTING
// =============================================================================
const hemiLight = new THREE.HemisphereLight(0x8888ff, 0x442244, 0.3);
hemiLight.position.set(0, 50, 0);
scene.add(hemiLight);

const dirLight = new THREE.DirectionalLight(0xffeedd, 0.4);
dirLight.position.set(50, 100, 50);
scene.add(dirLight);

// Point lights for city ambiance
const cityLights = [];
for (let i = 0; i < 5; i++) {
    const light = new THREE.PointLight(0xff8844, 0.5, 50);
    light.position.set(
        (Math.random() - 0.5) * 80,
        10,
        (Math.random() - 0.5) * 80
    );
    scene.add(light);
    cityLights.push(light);
}

// =============================================================================
// POST PROCESSING
// =============================================================================
const renderScene = new RenderPass(scene, camera);
const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    1.5, 0.4, 0.85
);
bloomPass.threshold = 0.3;
bloomPass.strength = 1.0;
bloomPass.radius = 0.8;

const composer = new EffectComposer(renderer);
composer.addPass(renderScene);
composer.addPass(bloomPass);

// =============================================================================
// MATERIALS - 3 STYLES
// =============================================================================
let worldMesh = null;
let currentStyle = 'Neon';

const materials = {
    'Realistic': new THREE.MeshStandardMaterial({
        vertexColors: true,
        roughness: 0.6,
        metalness: 0.2
    }),
    'Cartoon': new THREE.ShaderMaterial({
        uniforms: {
            uLightDir: { value: new THREE.Vector3(1, 1, 1).normalize() }
        },
        vertexShader: cartoonVert,
        fragmentShader: cartoonFrag,
        vertexColors: true
    }),
    'Neon': new THREE.ShaderMaterial({
        uniforms: {
            uTime: { value: 0 }
        },
        vertexShader: neonVert,
        fragmentShader: neonFrag,
        vertexColors: true
    })
};

function setStyle(styleName) {
    currentStyle = styleName;
    if (worldMesh) {
        worldMesh.material = materials[styleName];
    }

    // Adjust bloom for style
    switch (styleName) {
        case 'Realistic':
            bloomPass.strength = 0.3;
            bloomPass.threshold = 0.8;
            scene.fog = new THREE.FogExp2(bgCol, 0.005);
            break;
        case 'Cartoon':
            bloomPass.strength = 0.5;
            bloomPass.threshold = 0.6;
            scene.fog = new THREE.FogExp2(0x222244, 0.003);
            break;
        case 'Neon':
            bloomPass.strength = 1.2;
            bloomPass.threshold = 0.2;
            scene.fog = new THREE.FogExp2(bgCol, 0.008);
            break;
    }
}

// =============================================================================
// WORLD LOADING
// =============================================================================
async function loadWorld() {
    try {
        const response = await fetch('./assets/world.json');
        const data = await response.json();

        const geometry = new THREE.BufferGeometry();
        const vertices = new Float32Array(data.vertices.flat());
        const indices = data.faces.flat();

        geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
        geometry.setIndex(indices);

        if (data.colors) {
            const colors = new Float32Array(data.colors.flat());
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        }

        geometry.computeVertexNormals();

        worldMesh = new THREE.Mesh(geometry, materials[currentStyle]);
        scene.add(worldMesh);

        console.log(`✓ City loaded: ${data.vertices.length} vertices, ${data.faces.length} triangles`);

    } catch (err) {
        console.error("Error loading world:", err);
    }
}

// =============================================================================
// GUI CONTROLS
// =============================================================================
const gui = new dat.GUI({ width: 300 });
gui.domElement.style.marginTop = '10px';

const params = {
    style: 'Neon',
    ambientIntensity: hemiLight.intensity,
    dirIntensity: dirLight.intensity,
    bloomStrength: bloomPass.strength,
    bloomRadius: bloomPass.radius,
    fogDensity: 0.008,
    bgColor: bgCol,
    exposure: renderer.toneMappingExposure
};

// Style Selector
const styleFolder = gui.addFolder('🎨 Visual Style');
styleFolder.add(params, 'style', ['Realistic', 'Cartoon', 'Neon'])
    .name('Shader')
    .onChange(v => setStyle(v));
styleFolder.open();

// Lighting
const lightFolder = gui.addFolder('💡 Lighting');
lightFolder.add(params, 'ambientIntensity', 0, 2).name('Ambient')
    .onChange(v => hemiLight.intensity = v);
lightFolder.add(params, 'dirIntensity', 0, 2).name('Directional')
    .onChange(v => dirLight.intensity = v);
lightFolder.add(params, 'exposure', 0.5, 3).name('Exposure')
    .onChange(v => renderer.toneMappingExposure = v);
lightFolder.open();

// Bloom
const bloomFolder = gui.addFolder('✨ Bloom');
bloomFolder.add(params, 'bloomStrength', 0, 3).name('Strength')
    .onChange(v => bloomPass.strength = v);
bloomFolder.add(params, 'bloomRadius', 0, 2).name('Radius')
    .onChange(v => bloomPass.radius = v);
bloomFolder.open();

// World
const worldFolder = gui.addFolder('🌍 World');
worldFolder.addColor(params, 'bgColor').name('Sky Color')
    .onChange(v => {
        scene.background.setHex(v);
        scene.fog.color.setHex(v);
    });
worldFolder.add(params, 'fogDensity', 0, 0.02).name('Fog Density')
    .onChange(v => scene.fog.density = v);
worldFolder.open();

// Stats display
const statsDiv = document.createElement('div');
statsDiv.style.cssText = `
    position: fixed;
    bottom: 20px;
    left: 20px;
    font-family: monospace;
    font-size: 14px;
    color: rgba(255,255,255,0.7);
    background: rgba(0,0,0,0.5);
    padding: 10px 15px;
    border-radius: 8px;
`;
document.body.appendChild(statsDiv);

// =============================================================================
// ANIMATION LOOP
// =============================================================================
let prevTime = performance.now();
let frameCount = 0;
let fps = 0;

function animate() {
    requestAnimationFrame(animate);

    const time = performance.now();
    const delta = (time - prevTime) / 1000;

    // FPS counter
    frameCount++;
    if (time - prevTime > 1000) {
        fps = Math.round(frameCount * 1000 / (time - prevTime));
        frameCount = 0;
    }

    // Movement
    if (controls.isLocked) {
        velocity.x -= velocity.x * 10.0 * delta;
        velocity.z -= velocity.z * 10.0 * delta;

        direction.z = Number(moveForward) - Number(moveBackward);
        direction.x = Number(moveRight) - Number(moveLeft);
        direction.normalize();

        if (moveForward || moveBackward) velocity.z -= direction.z * 400.0 * delta;
        if (moveLeft || moveRight) velocity.x -= direction.x * 400.0 * delta;

        controls.moveRight(-velocity.x * delta);
        controls.moveForward(-velocity.z * delta);

        // Keep camera above ground
        if (camera.position.y < 2) camera.position.y = 2;
    }

    // Update shader uniforms
    if (materials['Neon'].uniforms) {
        materials['Neon'].uniforms.uTime.value = time * 0.001;
    }

    // Update stats
    statsDiv.innerHTML = `
        FPS: ${fps} | Style: ${currentStyle}<br>
        Pos: ${camera.position.x.toFixed(1)}, ${camera.position.z.toFixed(1)}
    `;

    prevTime = time;
    composer.render();
}

// =============================================================================
// INIT
// =============================================================================
loadWorld();
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
});

console.log('🏙️ Procedural City Viewer loaded');
console.log('👆 Click to enter, WASD to move, use GUI to customize');
