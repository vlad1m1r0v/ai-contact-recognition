import type { CardListItem, ContactCard, ContactMethod, PaginatedResponse } from "@/types/contact"

const BASE: string =
  (import.meta as unknown as Record<string, Record<string, string>>).env
    ?.VITE_API_BASE_URL ?? "http://127.0.0.1:9211"

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
  return res.json()
}

export async function getContact(id: string): Promise<ContactCard> {
  const res = await fetch(`${BASE}/contacts/${id}`)
  await checkResponse(res)
  return res.json()
}

export async function extractContact(file: File): Promise<ContactCard> {
  const fd = new FormData()
  fd.append("file", file)

  const res = await fetch(`${BASE}/contacts/extract`, {
    method: "POST",
    body: fd,
  })
  await checkResponse(res)
  return res.json()
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
  return res.json()
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
  return res.json()
}

export async function deleteContact(id: string): Promise<void> {
  const res = await fetch(`${BASE}/contacts/${id}`, { method: "DELETE" })
  await checkResponse(res)
}
