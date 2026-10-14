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
export const IconChevronRight = (p: IconProps) => <Svg {...p}><path d="m9 18 6-6-6-6" /></Svg>;
export const IconGlobe = (p: IconProps) => <Svg {...p}><circle cx="12" cy="12" r="10" /><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20M2 12h20" /></Svg>;
export const IconVideo = (p: IconProps) => <Svg {...p}><path d="m16 13 5.22 3.48a.5.5 0 0 0 .78-.42V7.94a.5.5 0 0 0-.78-.42L16 11" /><rect x="2" y="6" width="14" height="12" rx="2" /></Svg>;
export const IconPrinter = (p: IconProps) => <Svg {...p}><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2" /><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6" /><rect x="6" y="14" width="12" height="8" rx="1" /></Svg>;
export const IconUser = (p: IconProps) => <Svg {...p}><circle cx="12" cy="8" r="5" /><path d="M20 21a8 8 0 0 0-16 0" /></Svg>;
export const IconUsers = (p: IconProps) => <Svg {...p}><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" /></Svg>;
export const IconCalendar = (p: IconProps) => <Svg {...p}><rect width="18" height="18" x="3" y="4" rx="2" /><path d="M16 2v4M8 2v4M3 10h18M9 16l2 2 4-4" /></Svg>;
export const IconPin = (p: IconProps) => <Svg {...p}><path d="M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0" /><circle cx="12" cy="10" r="3" /></Svg>;
export const IconImages = (p: IconProps) => <Svg {...p}><path d="M18 22H4a2 2 0 0 1-2-2V6" /><path d="m22 13-1.3-1.3a2.4 2.4 0 0 0-3.4 0L11 18" /><circle cx="12" cy="8" r="2" /><rect width="16" height="16" x="6" y="2" rx="2" /></Svg>;
export const IconMusic = (p: IconProps) => <Svg {...p}><path d="M9 18V5l12-2v13" /><circle cx="6" cy="18" r="3" /><circle cx="18" cy="16" r="3" /></Svg>;
export const IconGift = (p: IconProps) => <Svg {...p}><rect x="3" y="8" width="18" height="4" rx="1" /><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5" /></Svg>;
export const IconSparkle = (p: IconProps) => <Svg {...p}><path d="M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.13-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.13a.5.5 0 0 1 .96 0l1.58 6.13a2 2 0 0 0 1.44 1.44l6.13 1.58a.5.5 0 0 1 0 .96l-6.13 1.58a2 2 0 0 0-1.44 1.44l-1.58 6.13a.5.5 0 0 1-.96 0z" /></Svg>;
export const IconRefresh = (p: IconProps) => <Svg {...p}><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M8 16H3v5" /></Svg>;
export const IconWifiOff = (p: IconProps) => <Svg {...p}><path d="M12 20h.01M8.5 16.43a5 5 0 0 1 7 0M2 8.82a15 15 0 0 1 4.17-2.65M10.66 5c4.01-.36 8.14.9 11.34 3.76M16.85 11.25a10 10 0 0 1 2.22 1.68M5 13a10 10 0 0 1 5.24-2.76M2 2l20 20" /></Svg>;
export const IconDownload = (p: IconProps) => <Svg {...p}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" /></Svg>;
export const IconFile = (p: IconProps) => <Svg {...p}><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" /><path d="M14 2v4a2 2 0 0 0 2 2h4" /></Svg>;
export const IconTruck = (p: IconProps) => <Svg {...p}><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2M15 18H9M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14" /><circle cx="17" cy="18" r="2" /><circle cx="7" cy="18" r="2" /></Svg>;
export const IconBank = (p: IconProps) => <Svg {...p}><path d="M3 22h18M6 18v-7M10 18v-7M14 18v-7M18 18v-7M12 2l8 5H4z" /></Svg>;
export const IconCopy = (p: IconProps) => <Svg {...p}><rect width="14" height="14" x="8" y="8" rx="2" /><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" /></Svg>;
export const IconChart = (p: IconProps) => <Svg {...p}><path d="M3 3v16a2 2 0 0 0 2 2h16M18 17V9M13 17V5M8 17v-3" /></Svg>;
export const IconClock = (p: IconProps) => <Svg {...p}><circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" /></Svg>;
export const IconLanguages = (p: IconProps) => <Svg {...p}><path d="m5 8 6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6" /></Svg>;
export const IconRadio = (p: IconProps) => <Svg {...p}><path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5" /><circle cx="12" cy="12" r="2" /><path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5M19.1 4.9C23 8.8 23 15.1 19.1 19" /></Svg>;
export const IconMessageSquare = (p: IconProps) => <Svg {...p}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></Svg>;
export const IconHandshake = (p: IconProps) => <Svg {...p}><path d="m11 17 2 2a1 1 0 1 0 3-3" /><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4" /><path d="m21 3 1 11h-2M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3M3 4h8" /></Svg>;
export const IconPhone = (p: IconProps) => <Svg {...p}><rect width="14" height="20" x="5" y="2" rx="2" /><path d="M12 18h.01" /></Svg>;
export const IconMonitor = (p: IconProps) => <Svg {...p}><rect width="20" height="14" x="2" y="3" rx="2" /><path d="M8 21h8M12 17v4" /></Svg>;
export const IconAward = (p: IconProps) => <Svg {...p}><circle cx="12" cy="8" r="6" /><path d="M15.48 12.89 17 22l-5-3-5 3 1.52-9.11" /></Svg>;
export const IconPencil = (p: IconProps) => <Svg {...p}><path d="M21.17 6.81a1 1 0 0 0-3.99-3.99L3.84 16.17a2 2 0 0 0-.5.83l-1.32 4.35a.5.5 0 0 0 .62.62l4.35-1.32a2 2 0 0 0 .83-.5zM15 5l4 4" /></Svg>;
export const IconWallet = (p: IconProps) => <Svg {...p}><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1" /><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4" /></Svg>;
export const IconReceipt = (p: IconProps) => <Svg {...p}><path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z" /><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8M12 17.5v-11" /></Svg>;
