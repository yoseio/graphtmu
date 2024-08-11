import { MetadataRoute } from "next"

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: "https://graphtmu.vercel.app",
    },
    {
      url: "https://graphtmu.vercel.app/teacher",
    },
    {
      url: "https://graphtmu.vercel.app/teacher/all",
    },
  ]
}
