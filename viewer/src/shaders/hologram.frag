uniform float uTime;
uniform vec3 uColor;

varying vec3 vNormal;
varying vec3 vViewPosition;
varying vec3 vWorldPosition;

void main() {
    vec3 normal = normalize(vNormal);
    vec3 viewDir = normalize(vViewPosition); // Camera is at 0,0,0 in view space, so vector TO camera is normalize(-vViewPos) = normalize(vViewPosition) since vViewPos is -mvPosition
    
    // Rim Light
    float rim = 1.0 - max(dot(viewDir, normal), 0.0);
    rim = pow(rim, 3.0);
    
    // Scanlines (based on world Y)
    float scanline = sin(vWorldPosition.y * 20.0 - uTime * 3.0);
    float scanlineMix = smoothstep(0.8, 1.0, scanline);
    
    // Pulse
    float pulse = (sin(uTime) * 0.5 + 0.5) * 0.2 + 0.8;
    
    // Grid effect
    float grid = max(
        step(0.95, fract(vWorldPosition.x * 2.0)),
        step(0.95, fract(vWorldPosition.z * 2.0))
    );
    
    vec3 finalColor = uColor * pulse;
    finalColor += uColor * scanlineMix * 0.5;
    finalColor += vec3(1.0) * grid * 0.2;
    finalColor += uColor * rim;
    
    // Alpha
    float alpha = 0.6 + rim * 0.4 + scanlineMix * 0.2;
    
    gl_FragColor = vec4(finalColor, alpha);
}
