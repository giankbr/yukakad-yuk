import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tiurma", groom: "Hotman",
    brideFull: "Tiurma Rosalina br. Sihombing, S.E.", groomFull: "Hotman Parulian Simanjuntak, S.T.",
    brideParents: "Putri kedua dari\nBapak St. Jonggi Sihombing & Ibu Rosmawati br. Pardede", groomParents: "Putra sulung dari\nBapak Pdt. Marihot Simanjuntak & Ibu Lasma br. Siregar",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Tali tiga lembar tak mudah diputuskan. Di tepi Danau Toba kami mengikat janji di hadapan Tuhan dan Dalihan Na Tolu.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-26T10:00:00+07:00",
  place: "HKBP Balige",
  address: "Jl. Gereja No. 1, Balige I, Kec. Balige, Kabupaten Toba",
  stories: [
    { date: "2020", title: "Paduan Suara Naposo", body: "Kami bertemu di latihan paduan suara naposobulung HKBP saat Natal di Medan. Hotman di bas, Tiurma di sopran." },
    { date: "2024", title: "Pulang ke Samosir", body: "Liburan keluarga ke Tuktuk mempertemukan dua keluarga yang ternyata masih bersaudara jauh lewat marga." },
    { date: "2026", title: "Marhusip", body: "Utusan keluarga Simanjuntak datang ke Balige untuk marhusip, membicarakan niat baik dengan hula-hula." },
  ],
  events: [
    { name: "Martumpol", date: "2027-06-18T16:00:00+07:00", time: "16.00 – 18.00 WIB", venue: "HKBP Balige", address: "Jl. Gereja No. 1, Balige I, Kec. Balige, Kabupaten Toba" },
    { name: "Pemberkatan Nikah", date: "2027-06-26T10:00:00+07:00", time: "10.00 – 12.00 WIB", venue: "HKBP Balige", address: "Jl. Gereja No. 1, Balige I, Kec. Balige, Kabupaten Toba" },
    { name: "Pesta Adat Unjuk", date: "2027-06-26T13:00:00+07:00", time: "13.00 – 19.00 WIB", venue: "Jambur Sopo Godang Tuktuk", address: "Jl. Lingkar Tuktuk, Tuktuk Siadong, Kec. Simanindo, Kabupaten Samosir" },
  ],
  gallery: ["/themes/img/r79.webp", "/themes/img/r16.webp", "/themes/img/r102.webp", "/themes/img/r89.webp", "/themes/img/r84.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0213 0104 5567 503", account_name: "Tiurma Rosalina Sihombing" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "107 00 1288 4410", account_name: "Hotman Parulian Simanjuntak" },
    { id: "demo-kado", type: "address", address: "Jl. Sisingamangaraja No. 48, Balige III, Kabupaten Toba 22312", account_name: "Keluarga St. Jonggi Sihombing" },
  ],
  guestName: "Bapak Amang Boru Tambunan & Keluarga",
  guestTable: "Meja Hula-hula 3",
  extras: {
    quote: { text: "Dan bilamana seorang dapat dialahkan, dua orang akan dapat bertahan. Tali tiga lembar tak mudah diputuskan.", source: "Pengkhotbah 4:12" },
    rundown: { items: [
      { time: "13.00", title: "Penyambutan hula-hula", note: "Diiringi gondang sabangunan" },
      { time: "14.00", title: "Makan bersama", note: "Jambar dibagikan" },
      { time: "15.30", title: "Pemberian ulos", note: "Ulos hela dari hula-hula" },
      { time: "18.00", title: "Mangampu & doa penutup" },
    ] },
    dressCode: { note: "Busana resmi dengan sentuhan ulos. Merah, hitam, dan putih dipersilakan.", colors: ["#ad2a1f", "#1d1916", "#f1ebdf", "#4f7e98"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-26T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Kami yang berbahagia", names: ["Kel. Besar St. J. Sihombing / br. Pardede", "Kel. Besar Pdt. M. Simanjuntak / br. Siregar", "Dongan Tubu & Boru ni Raja"] },
    travel: { note: "Untuk tamu dari luar kota, berikut pilihan menuju Samosir.", items: [
      { name: "Kapal Ajibata – Tuktuk", detail: "Setiap jam, ± 45 menit penyeberangan" },
      { name: "Bandara Silangit", detail: "± 1 jam berkendara ke Balige" },
    ] },
  },
});
