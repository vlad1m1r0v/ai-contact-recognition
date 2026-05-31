import type { ContactCard, ContactMethod, PaginatedResponse } from "@/types/contact"

const BASE: string =
  (import.meta as unknown as Record<string, Record<string, string>>).env
    ?.VITE_API_BASE_URL ?? "http://127.0.0.1:9211"

function computeDisplayName(card: {
  first_name?: string | null
  last_name?: string | null
  middle_name?: string | null
  company_name?: string | null
}): string {
  const name = [card.first_name, card.middle_name, card.last_name]
    .filter(Boolean)
    .join(" ")
  return card.company_name || name || "Unnamed"
}

function mapCard(raw: Record<string, unknown>): ContactCard {
  return {
    id: raw.id as string,
    image_url: (raw.image_url as string) ?? "",
    display_name:
      (raw.display_name as string) ??
      computeDisplayName(raw as Parameters<typeof computeDisplayName>[0]),
    created_at: (raw.created_at as string) ?? new Date().toISOString(),
    first_name: raw.first_name as string | undefined,
    last_name: raw.last_name as string | undefined,
    middle_name: raw.middle_name as string | undefined,
    company_name: raw.company_name as string | undefined,
    positions: (raw.positions as string[]) ?? [],
    services: (raw.services as string[]) ?? [],
    addresses: (raw.addresses as string[]) ?? [],
    digital_contacts: (raw.digital_contacts as ContactMethod[]) ?? [],
    summary: raw.summary as string | undefined,
  }
}

async function checkResponse(res: Response): Promise<void> {
  if (res.ok) return
  let detail: string | undefined
  try {
    const body = await res.json()
    detail = body.message ?? body.detail?.[0]?.msg ?? body.detail
  } catch {
    detail = res.statusText
  }
  throw new Error(detail ?? `Request failed with status ${res.status}`)
}

export async function getContacts(
  page: number,
  limit: number,
  search?: string,
): Promise<PaginatedResponse> {
  const params = new URLSearchParams({ page: String(page), limit: String(limit) })
  if (search) params.set("search", search)

  const res = await fetch(`${BASE}/contacts?${params}`)
  await checkResponse(res)
  const data: PaginatedResponse = await res.json()
  return { ...data, items: data.items.map(mapCard) }
}

export async function getContact(id: string): Promise<ContactCard> {
  const res = await fetch(`${BASE}/contacts/${id}`)
  await checkResponse(res)
  const data: Record<string, unknown> = await res.json()
  return mapCard(data)
}

export async function extractContact(file: File): Promise<ContactCard> {
  const fd = new FormData()
  fd.append("file", file)

  const res = await fetch(`${BASE}/contacts/extract`, {
    method: "POST",
    body: fd,
  })
  await checkResponse(res)
  const data: Record<string, unknown> = await res.json()
  return mapCard(data)
}

export async function createContact(data: {
  image_base64: string
  first_name?: string
  last_name?: string
  middle_name?: string
  company_name?: string
  positions?: string[]
  services?: string[]
  addresses?: string[]
  digital_contacts?: ContactMethod[]
  summary?: string
}): Promise<ContactCard> {
  const res = await fetch(`${BASE}/contacts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  await checkResponse(res)
  const raw: Record<string, unknown> = await res.json()
  return mapCard(raw)
}

export async function updateContact(
  id: string,
  data: Partial<{
    image_base64: string
    first_name?: string
    last_name?: string
    middle_name?: string
    company_name?: string
    positions?: string[]
    services?: string[]
    addresses?: string[]
    digital_contacts?: ContactMethod[]
    summary?: string
  }>,
): Promise<ContactCard> {
  const res = await fetch(`${BASE}/contacts/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  await checkResponse(res)
  const raw: Record<string, unknown> = await res.json()
  return mapCard(raw)
}

export async function deleteContact(id: string): Promise<void> {
  const res = await fetch(`${BASE}/contacts/${id}`, { method: "DELETE" })
  await checkResponse(res)
}
