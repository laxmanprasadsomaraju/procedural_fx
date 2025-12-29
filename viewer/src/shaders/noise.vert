uniform float uTime;
varying vec3 vNormal;
varying float vNoise;

// Simple pseudo-random/noise function
float random(vec3 st) {
    return fract(sin(dot(st.xyz, vec3(12.9898,78.233,45.5432))) * 43758.5453123);
}

void main() {
    vNormal = normalize(normalMatrix * normal);
    
    float noise = sin(position.y * 10.0 + uTime) * 0.1;
    vNoise = noise;
    
    vec3 newPosition = position + (normal * noise);
    
    gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
}
