"use client";

import { useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";

export function AosInit() {
  useEffect(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    AOS.init({
      duration: 700,
      easing: "ease-out-cubic",
      once: true,
      offset: 56,
      delay: 0,
      disable: reduce,
    });
  }, []);

  return null;
}
