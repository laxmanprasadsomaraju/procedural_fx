uniform vec3 uColor;
uniform vec3 uRimColor;
uniform float uRimPower;
uniform vec3 uLightDir; // Used for base lighting

varying vec3 vNormal;
varying vec3 vViewPosition;

void main() {
    vec3 normal = normalize(vNormal);
    vec3 viewDir = normalize(vViewPosition); // View position is (0,0,0) in view space, vViewPosition is -mvPos
    // Actually vViewPosition is just -mvPos.xyz, so vector TO camera is normalize(vViewPosition)
    
    // Base Light
    float NdotL = max(dot(normal, normalize(uLightDir)), 0.0);
    vec3 diffuse = uColor * (NdotL * 0.5 + 0.5); // Half-Lambert
    
    // Rim Light
    float rimFactor = 1.0 - max(dot(viewDir, normal), 0.0);
    rimFactor = pow(rimFactor, uRimPower);
    
    vec3 finalColor = diffuse + (uRimColor * rimFactor);
    
    gl_FragColor = vec4(finalColor, 1.0);
}
