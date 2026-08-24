"use client";

/* eslint-disable @next/next/no-img-element -- Property sources are user/data-driven remote URLs; this wrapper supplies a reliable fallback. */

import { useEffect, useState, type ImgHTMLAttributes, type SyntheticEvent } from "react";

const FALLBACK_SOURCE = "/property-placeholder.svg";

type PropertyImageProps = Omit<ImgHTMLAttributes<HTMLImageElement>, "src"> & {
  src?: string | null;
};

export default function PropertyImage({ src, alt, onError, ...props }: PropertyImageProps) {
  const [currentSource, setCurrentSource] = useState(src || FALLBACK_SOURCE);

  useEffect(() => {
    setCurrentSource(src || FALLBACK_SOURCE);
  }, [src]);

  const handleError = (event: SyntheticEvent<HTMLImageElement>) => {
    onError?.(event);
    if (currentSource !== FALLBACK_SOURCE) setCurrentSource(FALLBACK_SOURCE);
  };

  return <img {...props} src={currentSource} alt={alt} onError={handleError} />;
}
