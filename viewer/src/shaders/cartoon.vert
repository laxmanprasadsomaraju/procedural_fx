// Cartoon Vertex Shader
precision highp float;

varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vColor;

void main() {
    vNormal = normalMatrix * normal;
    vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
    vColor = color;
    
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
