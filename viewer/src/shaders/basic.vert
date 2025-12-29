varying vec3 vNormal;
varying vec3 vViewPosition;

void main() {
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    vec4 mvPosition = viewMatrix * worldPosition;
    
    vNormal = normalize(normalMatrix * normal);
    vViewPosition = -mvPosition.xyz;
    
    gl_Position = projectionMatrix * mvPosition;
}
