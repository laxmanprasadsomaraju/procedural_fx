// Neon/Cyberpunk Fragment Shader
// Creates glowing edge effect with dark interiors

precision highp float;

varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vColor;

uniform float uTime;

void main() {
    vec3 normal = normalize(vNormal);
    vec3 viewDir = normalize(-vPosition);
    
    // Edge glow (Fresnel effect)
    float fresnel = 1.0 - abs(dot(viewDir, normal));
    fresnel = pow(fresnel, 2.0);
    
    // Pulsing neon effect
    float pulse = 0.8 + 0.2 * sin(uTime * 2.0);
    
    // Base color is dark
    vec3 baseColor = vColor * 0.15;
    
    // Edge color is bright neon version of vertex color
    vec3 neonColor = vColor * 2.0 * pulse;
    
    // Mix based on fresnel
    vec3 color = mix(baseColor, neonColor, fresnel);
    
    // Add scanlines for cyberpunk feel
    float scanline = sin(vPosition.y * 50.0 + uTime * 5.0) * 0.5 + 0.5;
    scanline = smoothstep(0.3, 0.7, scanline);
    color *= 0.9 + 0.1 * scanline;
    
    // Emissive boost for bright colors (windows)
    float brightness = (vColor.r + vColor.g + vColor.b) / 3.0;
    if (brightness > 0.7) {
        color = vColor * 1.5; // Full glow for bright elements
    }
    
    gl_FragColor = vec4(color, 1.0);
}
