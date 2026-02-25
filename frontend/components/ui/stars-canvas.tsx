'use client';

import { useEffect, useRef } from 'react';

interface StarsCanvasProps {
  transparent?: boolean;
  maxStars?: number;
  hue?: number;
  brightness?: number;
  speedMultiplier?: number;
  twinkleIntensity?: number;
  className?: string;
  paused?: boolean;
}

export function StarsCanvas({
  transparent = false,
  maxStars = 900,
  hue = 217,
  brightness = 0.9,
  speedMultiplier = 1,
  twinkleIntensity = 18,
  className = '',
  paused = false,
}: StarsCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationRef = useRef<number | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let w = 0;
    let h = 0;
    let cx = 0;
    let cy = 0;
    const depth = 1400;

    type Star = {
      x: number;
      y: number;
      z: number;
      alpha: number;
      twinkleOffset: number;
    };

    const stars: Star[] = [];

    const randomRange = (min: number, max: number) => Math.random() * (max - min) + min;

    const resetStar = (s: Star, near = false) => {
      const spread = Math.max(w, h) * 1.4;
      s.x = randomRange(-spread, spread);
      s.y = randomRange(-spread, spread);
      s.z = near ? randomRange(40, depth * 0.35) : randomRange(40, depth);
      s.alpha = randomRange(0.48, 1) * brightness;
      s.twinkleOffset = randomRange(0, Math.PI * 2);
    };

    const initStars = () => {
      stars.length = 0;
      for (let i = 0; i < maxStars; i += 1) {
        const s: Star = { x: 0, y: 0, z: 0, alpha: 1, twinkleOffset: 0 };
        resetStar(s, i % 8 === 0);
        stars.push(s);
      }
    };

    const resize = () => {
      const rect = canvas.parentElement?.getBoundingClientRect();
      w = Math.max(1, Math.floor(rect?.width ?? window.innerWidth));
      h = Math.max(1, Math.floor(rect?.height ?? window.innerHeight));
      canvas.width = w;
      canvas.height = h;
      cx = w * 0.5;
      cy = h * 0.5;
      initStars();
    };
    resize();

    const animate = () => {
      if (!paused) {
        // Hard clear each frame to remove all trails.
        ctx.clearRect(0, 0, w, h);
        if (!transparent) {
          ctx.fillStyle = 'rgba(2, 6, 18, 1)';
          ctx.fillRect(0, 0, w, h);
        }

        const zSpeed = 4.2 * speedMultiplier;
        const pulse = performance.now() * 0.0013;

        for (let i = 0; i < stars.length; i += 1) {
          const s = stars[i];
          s.z -= zSpeed;
          if (s.z <= 1) {
            resetStar(s, true);
            s.z = depth;
          }

          const perspective = 320 / s.z;
          const sx = s.x * perspective + cx;
          const sy = s.y * perspective + cy;

          if (sx < -20 || sx > w + 20 || sy < -20 || sy > h + 20) {
            resetStar(s, false);
            s.z = depth;
            continue;
          }

          const twinkle =
            0.82 + 0.18 * Math.sin(pulse * twinkleIntensity + s.twinkleOffset);
          const intensity = Math.max(0.08, s.alpha * twinkle);
          const size = Math.max(0.45, perspective * 3.2);

          const core = `hsla(${hue}, 92%, 88%, ${Math.min(1, intensity)})`;
          const glow = `hsla(${hue}, 100%, 68%, ${Math.min(0.85, intensity * 0.48)})`;

          // Glow ring
          const g = ctx.createRadialGradient(sx, sy, 0, sx, sy, size * 3.2);
          g.addColorStop(0, glow);
          g.addColorStop(1, 'transparent');
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.arc(sx, sy, size * 3.2, 0, Math.PI * 2);
          ctx.fill();

          // Crisp star core
          ctx.fillStyle = core;
          ctx.beginPath();
          ctx.arc(sx, sy, size, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);

    const handleResize = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);
    return () => {
      if (animationRef.current !== null) cancelAnimationFrame(animationRef.current);
      window.removeEventListener('resize', handleResize);
    };
  }, [transparent, maxStars, hue, brightness, speedMultiplier, twinkleIntensity, paused]);

  return (
    <canvas
      ref={canvasRef}
      className={`absolute left-0 top-0 h-full w-full ${className}`}
      style={{ display: 'block' }}
    />
  );
}
