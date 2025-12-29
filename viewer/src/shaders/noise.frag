uniform vec3 uColor;
varying vec3 vNormal;
varying float vNoise;

void main() {
    // vary color based on noise height
    vec3 color = uColor + (vNoise * 0.5);
    gl_FragColor = vec4(color, 1.0);
}
