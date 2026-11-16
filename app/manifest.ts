import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Casa Control",
    short_name: "Casa",
    description: "Tarefas da casa",
    start_url: "/hoje",
    scope: "/",
    display: "standalone",
    background_color: "#f3f0e8",
    theme_color: "#1f5c40",
    lang: "pt-BR",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
    ],
  };
}
