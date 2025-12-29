uniform vec3 uColor;
uniform vec3 uLightDir;

varying vec3 vNormal;

void main() {
    float intensity = dot(normalize(vNormal), normalize(uLightDir));
    
    // Cel shading steps
    if (intensity > 0.95) intensity = 1.0;
    else if (intensity > 0.5) intensity = 0.6;
    else if (intensity > 0.25) intensity = 0.4;
    else intensity = 0.2;
    
    gl_FragColor = vec4(uColor * intensity, 1.0);
}
