import { Canvas, useFrame } from "@react-three/fiber"
import { useRef } from "react"
import * as THREE from "three"

function ShaderPlane() {
  const materialRef = useRef<any>()
  const mouse = useRef(new THREE.Vector2(0, 0))

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uniforms.uTime.value = state.clock.getElapsedTime()

      mouse.current.x = state.mouse.x
      mouse.current.y = state.mouse.y

      materialRef.current.uniforms.uMouse.value = mouse.current
    }
  })

  return (
    <mesh onPointerMove={(e) => console.log(e.uv)}>
      <planeGeometry args={[10, 10]} />

      <shaderMaterial
        ref={materialRef}
        uniforms={{
          uTime: { value: 0 },
          uMouse: { value: new THREE.Vector2(0, 0) },
        }}
        vertexShader={`
          varying vec2 vUv;

          void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }
        `}
        fragmentShader={`
          uniform float uTime;
          uniform vec2 uMouse;
          varying vec2 vUv;

          // --- bruit ---
          float hash(vec2 p) {
            return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
          }

          float noise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);

            float a = hash(i);
            float b = hash(i + vec2(1.0, 0.0));
            float c = hash(i + vec2(0.0, 1.0));
            float d = hash(i + vec2(1.0, 1.0));

            vec2 u = f * f * (3.0 - 2.0 * f);

            return mix(a, b, u.x) +
                   (c - a) * u.y * (1.0 - u.x) +
                   (d - b) * u.x * u.y;
          }

          float fbm(vec2 p) {
            float value = 0.0;
            float amp = 0.5;

            for (int i = 0; i < 5; i++) {
              value += amp * noise(p);
              p *= 2.0;
              amp *= 0.5;
            }

            return value;
          }

          void main() {
            vec2 uv = vUv;

            vec2 p = uv * 3.0;

            // =========================
            // 🎯 INTERACTION SOURIS
            // =========================
            vec2 mouse = uMouse * 0.5 + 0.5;

            float dist = distance(uv, mouse);
            float influence = exp(-dist * 8.0);

            p += (uv - mouse) * pow(influence, 2.0) * 0.35;

            // =========================
            // NOISE
            // =========================
            float n = fbm(p);

            // =========================
            // 🌊 WAVE SUR LES LIGNES (IMPORTANT)
            // =========================
            float wave = sin(uv.y * 10.0 + uTime * 1.5) * 0.04;

            float lines = fract(n * 75.0 + wave);

            float line = smoothstep(0.47, 0.5, lines) -
                          smoothstep(0.5, 0.55, lines);

            // profondeur
            float depth = smoothstep(0.8, 0.2, length(uv - 0.5));

            // glow
            float glow = pow(line, 2.0);

            // couleurs
            vec3 baseColor = vec3(0.0, 0.6, 1.0);
            vec3 glowColor = vec3(0.0, 0.3, 1.0);

            vec3 color = baseColor * line;
            color += glowColor * glow * 5.0;

            color *= depth;
            color += vec3(0.01, 0.02, 0.05);

            gl_FragColor = vec4(color, 1.0);
          }
        `}
      />
    </mesh>
  )
}

export default function BackgroundShader() {
  return (
    <Canvas
      camera={{ position: [0, 0, 1] }}
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        zIndex: -1,
      }}
    >
      <ShaderPlane />
    </Canvas>
  )
}
