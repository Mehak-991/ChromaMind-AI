import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

const ColorSphere = () => {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.005;
      meshRef.current.rotation.x += 0.002;
    }
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[1.8, 64, 64]} />
      <meshNormalMaterial wireframe={false} />
    </mesh>
  );
};

export const ColorSpace3D: React.FC = () => {
  return (
    <div className="w-full h-[300px] md:h-[400px] rounded-xl overflow-hidden glass border border-slate-800">
      <Canvas camera={{ position: [0, 0, 4] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <ColorSphere />
        <OrbitControls enableZoom={true} autoRotate={false} />
      </Canvas>
    </div>
  );
};
