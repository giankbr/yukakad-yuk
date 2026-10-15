// Rawuh UI icons, backed by Phosphor Icons (MIT, https://phosphoricons.com).
// Every icon keeps the old `IconX` API: `size`, `className`, `style`, plus an optional Phosphor `weight`.
import type { SVGProps } from "react";
import type { Icon as PhosphorIcon, IconWeight } from "@phosphor-icons/react";
import { ArrowRight as PhArrowRight, ArrowsClockwise as PhArrowsClockwise, Bank as PhBank, Broadcast as PhBroadcast, CalendarBlank as PhCalendarBlank, CaretDown as PhCaretDown, CaretRight as PhCaretRight, ChartBar as PhChartBar, ChatCenteredText as PhChatCenteredText, ChatCircle as PhChatCircle, Check as PhCheck, Clock as PhClock, Copy as PhCopy, DeviceMobile as PhDeviceMobile, DownloadSimple as PhDownloadSimple, EnvelopeSimple as PhEnvelopeSimple, Eye as PhEye, EyeSlash as PhEyeSlash, FacebookLogo as PhFacebookLogo, File as PhFile, Gift as PhGift, Globe as PhGlobe, GoogleLogo as PhGoogleLogo, Handshake as PhHandshake, Headset as PhHeadset, Heart as PhHeart, Images as PhImages, Infinity as PhInfinity, InstagramLogo as PhInstagramLogo, LinkSimple as PhLinkSimple, List as PhList, X as PhX, LockSimple as PhLockSimple, MagnifyingGlass as PhMagnifyingGlass, MapPin as PhMapPin, Medal as PhMedal, Minus as PhMinus, Monitor as PhMonitor, MusicNotes as PhMusicNotes, PaperPlaneTilt as PhPaperPlaneTilt, Pause as PhPause, PencilSimple as PhPencilSimple, Plus as PhPlus, Printer as PhPrinter, QrCode as PhQrCode, Receipt as PhReceipt, ShieldCheck as PhShieldCheck, Sparkle as PhSparkle, Star as PhStar, TiktokLogo as PhTiktokLogo, Timer as PhTimer, Translate as PhTranslate, Truck as PhTruck, User as PhUser, Users as PhUsers, VideoCamera as PhVideoCamera, Wallet as PhWallet, WhatsappLogo as PhWhatsappLogo, WifiSlash as PhWifiSlash, YoutubeLogo as PhYoutubeLogo } from "@phosphor-icons/react/ssr";

export type IconProps = Omit<SVGProps<SVGSVGElement>, "ref"> & { size?: number; weight?: IconWeight };

function make(Ph: PhosphorIcon) {
  function RawuhIcon({ size, width, height, weight, strokeWidth, ...props }: IconProps) {
    const resolved = size ?? (typeof width === "number" ? width : typeof height === "number" ? height : 16);
    // Old call sites pass a heavier strokeWidth for emphasis; map it to Phosphor's bold weight.
    const resolvedWeight = weight ?? (Number(strokeWidth) >= 2.2 ? "bold" : "regular");
    return <Ph size={resolved} weight={resolvedWeight} aria-hidden="true" focusable="false" {...props} />;
  }
  return RawuhIcon;
}

export const IconHeart = make(PhHeart);
export const IconMenu = make(PhList);
export const IconClose = make(PhX);
export const IconArrowRight = make(PhArrowRight);
export const IconChevronDown = make(PhCaretDown);
export const IconSend = make(PhPaperPlaneTilt);
export const IconLink = make(PhLinkSimple);
export const IconSearch = make(PhMagnifyingGlass);
export const IconCheck = make(PhCheck);
export const IconPlus = make(PhPlus);
export const IconMinus = make(PhMinus);
export const IconLock = make(PhLockSimple);
export const IconPause = make(PhPause);
export const IconInfinity = make(PhInfinity);
export const IconShield = make(PhShieldCheck);
export const IconTimer = make(PhTimer);
export const IconHeadset = make(PhHeadset);
export const IconMessage = make(PhChatCircle);
export const IconInstagram = make(PhInstagramLogo);
export const IconYoutube = make(PhYoutubeLogo);
export const IconFacebook = make(PhFacebookLogo);
export const IconTiktok = make(PhTiktokLogo);
export const IconWhatsapp = make(PhWhatsappLogo);
export const IconMail = make(PhEnvelopeSimple);
export const IconEye = make(PhEye);
export const IconEyeOff = make(PhEyeSlash);
export const IconStar = make(PhStar);
export const IconQr = make(PhQrCode);
export const IconGoogle = make(PhGoogleLogo);
export const IconChevronRight = make(PhCaretRight);
export const IconGlobe = make(PhGlobe);
export const IconVideo = make(PhVideoCamera);
export const IconPrinter = make(PhPrinter);
export const IconUser = make(PhUser);
export const IconUsers = make(PhUsers);
export const IconCalendar = make(PhCalendarBlank);
export const IconPin = make(PhMapPin);
export const IconImages = make(PhImages);
export const IconMusic = make(PhMusicNotes);
export const IconGift = make(PhGift);
export const IconSparkle = make(PhSparkle);
export const IconRefresh = make(PhArrowsClockwise);
export const IconWifiOff = make(PhWifiSlash);
export const IconDownload = make(PhDownloadSimple);
export const IconFile = make(PhFile);
export const IconTruck = make(PhTruck);
export const IconBank = make(PhBank);
export const IconCopy = make(PhCopy);
export const IconChart = make(PhChartBar);
export const IconClock = make(PhClock);
export const IconLanguages = make(PhTranslate);
export const IconRadio = make(PhBroadcast);
export const IconMessageSquare = make(PhChatCenteredText);
export const IconHandshake = make(PhHandshake);
export const IconPhone = make(PhDeviceMobile);
export const IconMonitor = make(PhMonitor);
export const IconAward = make(PhMedal);
export const IconPencil = make(PhPencilSimple);
export const IconWallet = make(PhWallet);
export const IconReceipt = make(PhReceipt);

/** Decorative QR code used as an illustration (not an icon). */
export const IconQrArt = (p: SVGProps<SVGSVGElement>) => (
  <svg viewBox="0 0 29 29" aria-hidden="true" focusable="false" {...p}>
    <g fill="currentColor">
      <path d="M0 0h9v9H0zM2 2v5h5V2zM20 0h9v9h-9zm2 2v5h5V2zM0 20h9v9H0zm2 2v5h5v-5z" fillRule="evenodd" />
      <path d="M3 3h3v3H3zM23 3h3v3h-3zM3 23h3v3H3zM11 0h2v3h-2zM15 2h3v2h-3zM11 5h4v2h-4zM16 6h2v4h-2zM11 9h3v2h-3zM0 11h3v2H0zM5 11h4v2H5zM11 13h2v3h-2zM14 12h4v2h-4zM20 11h3v3h-3zM25 11h4v2h-4zM20 16h2v4h-2zM23 15h3v2h-3zM27 15h2v5h-2zM11 18h3v2h-3zM15 17h3v4h-3zM11 22h2v4h-2zM14 23h4v2h-4zM20 22h3v2h-3zM24 21h2v4h-2zM20 26h3v3h-3zM26 26h3v3h-3zM15 27h3v2h-3z" />
    </g>
  </svg>
);
