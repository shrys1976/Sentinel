'use client';

import { cn } from '@/lib/utils';
import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

type DottedSurfaceProps = Omit<React.ComponentProps<'div'>, 'ref'> & {
  pointColor?: string;
};

export function DottedSurface({ className, pointColor = '#dbe7ff', ...props }: DottedSurfaceProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const SEPARATION = 132;
    const AMOUNTX = 40;
    const AMOUNTY = 56;

    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x050d29, 2400, 9800);

    const camera = new THREE.PerspectiveCamera(56, 1, 1, 10000);
    camera.position.set(0, 320, 1220);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    container.appendChild(renderer.domElement);

    const geometry = new THREE.BufferGeometry();
    const positions: number[] = [];
    const color = new THREE.Color(pointColor);
    const colors: number[] = [];

    for (let ix = 0; ix < AMOUNTX; ix++) {
      for (let iy = 0; iy < AMOUNTY; iy++) {
        const x = ix * SEPARATION - (AMOUNTX * SEPARATION) / 2;
        const y = 0;
        const z = iy * SEPARATION - (AMOUNTY * SEPARATION) / 2;

        positions.push(x, y, z);
        colors.push(color.r, color.g, color.b);
      }
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 5.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.72,
      sizeAttenuation: true,
    });

    const points = new THREE.Points(geometry, material);
    scene.add(points);

    // Soft parallax layer for a more premium depth effect.
    const geometryLayer2 = geometry.clone();
    const materialLayer2 = material.clone();
    materialLayer2.size = 3.2;
    materialLayer2.opacity = 0.34;
    const pointsLayer2 = new THREE.Points(geometryLayer2, materialLayer2);
    pointsLayer2.position.y = 22;
    pointsLayer2.position.z = -110;
    scene.add(pointsLayer2);

    let count = 0;
    let animationId = 0;

    const resize = () => {
      const { clientWidth, clientHeight } = container;
      if (clientWidth === 0 || clientHeight === 0) return;
      camera.aspect = clientWidth / clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(clientWidth, clientHeight);
    };

    const animate = () => {
      animationId = requestAnimationFrame(animate);

      const positionAttribute = geometry.attributes.position;
      const positionArray = positionAttribute.array as Float32Array;

      let i = 0;
      for (let ix = 0; ix < AMOUNTX; ix++) {
        for (let iy = 0; iy < AMOUNTY; iy++) {
          const index = i * 3;
          positionArray[index + 1] =
            Math.sin((ix + count) * 0.22) * 34 +
            Math.sin((iy + count * 1.05) * 0.38) * 36;
          i += 1;
        }
      }

      positionAttribute.needsUpdate = true;
      points.rotation.y = Math.sin(count * 0.04) * 0.04;
      pointsLayer2.rotation.y = Math.sin(count * 0.05 + 1.3) * 0.05;
      renderer.render(scene, camera);
      count += 0.048;
    };

    const resizeObserver = new ResizeObserver(() => resize());
    resizeObserver.observe(container);
    resize();
    animate();

    return () => {
      resizeObserver.disconnect();
      cancelAnimationFrame(animationId);
      geometry.dispose();
      material.dispose();
      geometryLayer2.dispose();
      materialLayer2.dispose();
      renderer.dispose();
      if (renderer.domElement.parentNode === container) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [pointColor]);

  return <div ref={containerRef} className={cn('pointer-events-none absolute inset-0', className)} {...props} />;
}
