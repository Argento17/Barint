"use client";
import { useEffect, useRef } from "react";
import PlantHero from "./plant-hero-engine";
import styles from "./plant-hero.module.css";

export function PlantHeroBackground() {
  const stageRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!stageRef.current) return;
    const inst = new PlantHero({
      stage: stageRef.current,
      assetBase: "/plant/",
      size: 540, opacity: 0.22, mode: "watermark",
      shatter: true, period: 7, constellation: true, particles: 0.6, parallax: true,
    });
    return () => inst.destroy();
  }, []);
  return (
    <>
      <div ref={stageRef} className={styles.stage} aria-hidden />
      <div className={styles.scrim} aria-hidden />
    </>
  );
}
