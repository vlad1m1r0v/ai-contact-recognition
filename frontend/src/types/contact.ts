export interface ContactMethod {
  type: string
  value: string
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
  positions: string[]
  services: string[]
  addresses: string[]
  digital_contacts: ContactMethod[]
  summary?: string
}

export interface PaginatedResponse {
  items: ContactCard[]
  total: number
  page: number
  limit: number
}
