import type { SVGProps } from "react";

type IconProps = SVGProps<SVGSVGElement> & { size?: number };

function Svg({ size = 16, children, ...props }: IconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8}
      strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false" {...props}>
      {children}
    </svg>
  );
}

export const IconHeart = (p: IconProps) => <Svg {...p}><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" /></Svg>;
export const IconArrowRight = (p: IconProps) => <Svg {...p}><path d="M5 12h14M12 5l7 7-7 7" /></Svg>;
export const IconChevronDown = (p: IconProps) => <Svg {...p}><path d="m6 9 6 6 6-6" /></Svg>;
export const IconSend = (p: IconProps) => <Svg {...p}><path d="m22 2-7 20-4-9-9-4Z" /><path d="M22 2 11 13" /></Svg>;
export const IconLink = (p: IconProps) => <Svg {...p}><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" /><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" /></Svg>;
export const IconSearch = (p: IconProps) => <Svg {...p}><circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" /></Svg>;
export const IconCheck = (p: IconProps) => <Svg {...p}><path d="M20 6 9 17l-5-5" /></Svg>;
export const IconPlus = (p: IconProps) => <Svg {...p}><path d="M5 12h14M12 5v14" /></Svg>;
export const IconMinus = (p: IconProps) => <Svg {...p}><path d="M5 12h14" /></Svg>;
export const IconLock = (p: IconProps) => <Svg {...p}><rect width="18" height="11" x="3" y="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></Svg>;
export const IconPause = (p: IconProps) => <Svg {...p}><rect x="6" y="4" width="4" height="16" rx="1" /><rect x="14" y="4" width="4" height="16" rx="1" /></Svg>;
export const IconInfinity = (p: IconProps) => <Svg {...p}><path d="M12 12c-2-2.67-4-4-6-4a4 4 0 1 0 0 8c2 0 4-1.33 6-4Zm0 0c2 2.67 4 4 6 4a4 4 0 0 0 0-8c-2 0-4 1.33-6 4Z" /></Svg>;
export const IconShield = (p: IconProps) => <Svg {...p}><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1Z" /><path d="m9 12 2 2 4-4" /></Svg>;
export const IconTimer = (p: IconProps) => <Svg {...p}><path d="M10 2h4M12 14l3-3" /><circle cx="12" cy="14" r="8" /></Svg>;
export const IconHeadset = (p: IconProps) => <Svg {...p}><path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3" /></Svg>;
export const IconMessage = (p: IconProps) => <Svg {...p}><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z" /></Svg>;
export const IconInstagram = (p: IconProps) => <Svg {...p}><rect width="20" height="20" x="2" y="2" rx="5" /><circle cx="12" cy="12" r="4" /><path d="M17.5 6.5h.01" /></Svg>;
export const IconYoutube = (p: IconProps) => <Svg {...p}><path d="M2.5 17a24 24 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.6 49.6 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24 24 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.6 49.6 0 0 1-16.2 0A2 2 0 0 1 2.5 17" /><path d="m10 15 5-3-5-3z" /></Svg>;
export const IconFacebook = (p: IconProps) => <Svg {...p}><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z" /></Svg>;
export const IconMail = (p: IconProps) => <Svg {...p}><rect width="20" height="16" x="2" y="4" rx="2" /><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" /></Svg>;
export const IconEye = (p: IconProps) => <Svg {...p}><path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0" /><circle cx="12" cy="12" r="3" /></Svg>;
export const IconEyeOff = (p: IconProps) => <Svg {...p}><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68M6.61 6.61A13.53 13.53 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61M2 2l20 20M14.12 14.12a3 3 0 1 1-4.24-4.24" /></Svg>;
export const IconStar = (p: IconProps) => <Svg {...p}><path d="M11.53 2.3a.53.53 0 0 1 .95 0l2.31 4.68a2.12 2.12 0 0 0 1.6 1.16l5.16.76a.53.53 0 0 1 .3.9l-3.74 3.64a2.12 2.12 0 0 0-.61 1.88l.88 5.14a.53.53 0 0 1-.77.56l-4.62-2.43a2.12 2.12 0 0 0-1.97 0L6.4 21.01a.53.53 0 0 1-.77-.56l.88-5.14a2.12 2.12 0 0 0-.61-1.88L2.16 9.8a.53.53 0 0 1 .3-.9l5.16-.76a2.12 2.12 0 0 0 1.6-1.16Z" /></Svg>;
export const IconQr = (p: IconProps) => (
  <svg viewBox="0 0 29 29" aria-hidden="true" focusable="false" {...p}>
    <g fill="currentColor">
      <path d="M0 0h9v9H0zM2 2v5h5V2zM20 0h9v9h-9zm2 2v5h5V2zM0 20h9v9H0zm2 2v5h5v-5z" fillRule="evenodd" />
      <path d="M3 3h3v3H3zM23 3h3v3h-3zM3 23h3v3H3zM11 0h2v3h-2zM15 2h3v2h-3zM11 5h4v2h-4zM16 6h2v4h-2zM11 9h3v2h-3zM0 11h3v2H0zM5 11h4v2H5zM11 13h2v3h-2zM14 12h4v2h-4zM20 11h3v3h-3zM25 11h4v2h-4zM20 16h2v4h-2zM23 15h3v2h-3zM27 15h2v5h-2zM11 18h3v2h-3zM15 17h3v4h-3zM11 22h2v4h-2zM14 23h4v2h-4zM20 22h3v2h-3zM24 21h2v4h-2zM20 26h3v3h-3zM26 26h3v3h-3zM15 27h3v2h-3z" />
    </g>
  </svg>
);
export const IconGoogle = (p: IconProps) => <Svg {...p}><path d="M21.8 12.2c0-.7-.1-1.4-.2-2H12v3.9h5.5a4.7 4.7 0 0 1-2 3.1v2.6h3.3c1.9-1.8 3-4.4 3-7.6Z" /><path d="M12 22c2.7 0 5-.9 6.8-2.4l-3.3-2.6c-.9.6-2.1 1-3.5 1-2.7 0-4.9-1.8-5.7-4.2H2.9v2.6A10 10 0 0 0 12 22Z" /><path d="M6.3 13.8a6 6 0 0 1 0-3.8V7.4H2.9a10 10 0 0 0 0 9Z" /><path d="M12 6c1.5 0 2.8.5 3.9 1.5l2.9-2.9A10 10 0 0 0 2.9 7.4L6.3 10C7.1 7.7 9.3 6 12 6Z" /></Svg>;
