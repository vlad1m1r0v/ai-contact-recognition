export enum SocialPlatform {
  TELEGRAM = "telegram",
  LINKEDIN = "linkedin",
  WHATSAPP = "whatsapp",
  FACEBOOK = "facebook",
  INSTAGRAM = "instagram",
  VIBER = "viber",
  X = "x",
  VK = "vk",
}

export interface SocialMedia {
  platform: SocialPlatform
  username_or_link: string
}

export interface ContactCard {
  id: string
  image_url: string
  display_name: string
  created_at: string
  first_name?: string
  last_name?: string
  middle_name?: string
  company_name?: string
  position?: string
  services: string[]
  addresses: string[]
  phone_number?: string
  email?: string
  website?: string
  social_media: SocialMedia[]
  summary?: string
}

export interface PaginatedResponse {
  items: ContactCard[]
  total: number
  page: number
  limit: number
}
