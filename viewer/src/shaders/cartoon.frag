// Cartoon/Toon Fragment Shader
// Creates cel-shaded look with discrete lighting bands

precision highp float;

varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vColor;

uniform vec3 uLightDir;

void main() {
    vec3 normal = normalize(vNormal);
    vec3 lightDir = normalize(uLightDir);
    
    // Cel-shading: quantize lighting into bands
    float diff = dot(normal, lightDir);
    float intensity;
    
    if (diff > 0.8) {
        intensity = 1.0;
    } else if (diff > 0.5) {
        intensity = 0.7;
    } else if (diff > 0.2) {
        intensity = 0.5;
    } else {
        intensity = 0.3;
    }
    
    vec3 color = vColor * intensity;
    
    // Add slight rim light for cartoon pop
    vec3 viewDir = normalize(-vPosition);
    float rim = 1.0 - max(dot(viewDir, normal), 0.0);
    rim = smoothstep(0.6, 1.0, rim);
    color += vec3(0.2) * rim;
    
    gl_FragColor = vec4(color, 1.0);
}
