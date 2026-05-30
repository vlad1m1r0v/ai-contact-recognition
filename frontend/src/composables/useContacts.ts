import { ref, computed } from "vue"
import type { ContactCard, ContactMethod } from "@/types/contact"

function createMockContacts(): ContactCard[] {
  return [
    {
      id: "1",
      image_url: "https://placehold.co/600x400?text=Card+1",
      display_name: "Acme Corp",
      created_at: "2026-05-28T14:30:00Z",
      company_name: "Acme Corp",
      position: "CEO",
      first_name: "John",
      last_name: "Doe",
      services: ["Software Development", "Consulting"],
      addresses: ["123 Main St, New York, NY"],
      digital_contacts: [
        { type: "phone", value: "+1 555 123 4567" },
        { type: "email", value: "john@acme.com" },
        { type: "website", value: "https://acme.com" },
        { type: "linkedin", value: "https://linkedin.com/in/johndoe" },
      ],
      summary: "John Doe is the CEO of Acme Corp, a leading software development and consulting firm.",
    },
    {
      id: "2",
      image_url: "https://placehold.co/600x400?text=Card+2",
      display_name: "Jane Smith",
      created_at: "2026-05-27T10:15:00Z",
      first_name: "Jane",
      last_name: "Smith",
      company_name: "TechStart Inc",
      position: "CTO",
      services: ["AI Solutions", "Cloud Infrastructure"],
      addresses: ["456 Oak Ave, San Francisco, CA"],
      digital_contacts: [
        { type: "phone", value: "+1 555 987 6543" },
        { type: "email", value: "jane@techstart.io" },
        { type: "website", value: "https://techstart.io" },
        { type: "telegram", value: "@janesmith" },
        { type: "x", value: "https://x.com/janesmith" },
      ],
      summary: "Jane Smith is CTO at TechStart Inc, delivering AI and cloud infrastructure solutions.",
    },
    {
      id: "3",
      image_url: "https://placehold.co/600x400?text=Card+3",
      display_name: "Global Ventures LLC",
      created_at: "2026-05-26T09:00:00Z",
      company_name: "Global Ventures LLC",
      position: "Founder",
      first_name: "Alex",
      middle_name: "M",
      last_name: "Johnson",
      services: ["Venture Capital", "Business Development"],
      addresses: ["789 Bond St, London, UK"],
      digital_contacts: [
        { type: "phone", value: "+44 20 7946 0958" },
        { type: "email", value: "alex@globalventures.co.uk" },
        { type: "website", value: "https://globalventures.co.uk" },
        { type: "facebook", value: "https://facebook.com/alexjohnson" },
      ],
      summary: "Alex Johnson is the Founder of Global Ventures LLC, specializing in venture capital and business development.",
    },
    {
      id: "4",
      image_url: "https://placehold.co/600x400?text=Card+4",
      display_name: "Maria Garcia Design",
      created_at: "2026-05-25T16:45:00Z",
      company_name: "Maria Garcia Design",
      position: "Creative Director",
      first_name: "Maria",
      last_name: "Garcia",
      services: ["Graphic Design", "Brand Identity", "Web Design"],
      addresses: ["Calle Mayor 10, Madrid, Spain"],
      digital_contacts: [
        { type: "phone", value: "+34 91 123 4567" },
        { type: "email", value: "maria@mariagarciadesign.es" },
        { type: "website", value: "https://mariagarciadesign.es" },
        { type: "instagram", value: "https://instagram.com/mariagarciadesign" },
      ],
      summary: "Maria Garcia runs a creative design studio offering graphic design, brand identity, and web design services.",
    },
    {
      id: "5",
      image_url: "https://placehold.co/600x400?text=Card+5",
      display_name: "Tanaka Industries",
      created_at: "2026-05-24T11:30:00Z",
      company_name: "Tanaka Industries",
      position: "Director",
      first_name: "Kenji",
      last_name: "Tanaka",
      services: ["Manufacturing", "Logistics"],
      addresses: ["1-2-3 Shibuya, Tokyo, Japan", "Osaka Branch Office"],
      digital_contacts: [
        { type: "phone", value: "+81 3 5555 1234" },
        { type: "email", value: "kenji@tanaka-ind.co.jp" },
        { type: "website", value: "https://tanaka-ind.co.jp" },
        { type: "viber", value: "+81355551234" },
      ],
      summary: "Kenji Tanaka is the Director of Tanaka Industries, a manufacturing and logistics company based in Tokyo.",
    },
    {
      id: "6",
      image_url: "https://placehold.co/600x400?text=Card+6",
      display_name: "Sarah Williams",
      created_at: "2026-05-23T08:20:00Z",
      first_name: "Sarah",
      last_name: "Williams",
      company_name: "Freelance Marketing",
      position: "Marketing Consultant",
      services: ["Digital Marketing", "SEO", "Content Strategy"],
      addresses: ["123 George St, Sydney, Australia"],
      digital_contacts: [
        { type: "phone", value: "+61 2 5555 6789" },
        { type: "email", value: "sarah@freelancemarketing.au" },
        { type: "linkedin", value: "https://linkedin.com/in/sarahwilliams" },
        { type: "instagram", value: "https://instagram.com/sarahwilliams_mkt" },
      ],
      summary: "Sarah Williams is a freelance marketing consultant specializing in digital marketing, SEO, and content strategy.",
    },
    {
      id: "7",
      image_url: "https://placehold.co/600x400?text=Card+7",
      display_name: "Petrov Engineering",
      created_at: "2026-05-22T13:00:00Z",
      company_name: "Petrov Engineering",
      position: "Lead Engineer",
      first_name: "Dmitri",
      last_name: "Petrov",
      services: ["Civil Engineering", "Architecture", "Project Management"],
      addresses: ["ul. Tverskaya 15, Moscow, Russia"],
      digital_contacts: [
        { type: "phone", value: "+7 495 123 4567" },
        { type: "email", value: "dmitri@petrov-eng.ru" },
        { type: "vk", value: "https://vk.com/dmitripetrov" },
      ],
      summary: "Dmitri Petrov is the Lead Engineer at Petrov Engineering, offering civil engineering, architecture, and project management services.",
    },
    {
      id: "8",
      image_url: "https://placehold.co/600x400?text=Card+8",
      display_name: "Lee & Associates",
      created_at: "2026-05-21T15:10:00Z",
      company_name: "Lee & Associates",
      position: "Partner",
      first_name: "Emily",
      last_name: "Lee",
      services: ["Legal Services", "Corporate Law"],
      addresses: ["123 Gangnam-daero, Seoul, South Korea"],
      digital_contacts: [
        { type: "phone", value: "+82 2 5555 7890" },
        { type: "email", value: "emily@lee-associates.kr" },
        { type: "website", value: "https://lee-associates.kr" },
        { type: "linkedin", value: "https://linkedin.com/in/emilylee" },
      ],
      summary: "Emily Lee is a Partner at Lee & Associates, providing legal services specializing in corporate law.",
    },
    {
      id: "9",
      image_url: "https://placehold.co/600x400?text=Card+9",
      display_name: "Müller Healthcare",
      created_at: "2026-05-20T09:45:00Z",
      company_name: "Müller Healthcare",
      position: "Chief Medical Officer",
      first_name: "Hans",
      last_name: "Müller",
      services: ["Medical Consulting", "Healthcare Innovation"],
      addresses: ["Unter den Linden 50, Berlin, Germany"],
      digital_contacts: [
        { type: "phone", value: "+49 30 5555 1234" },
        { type: "email", value: "hans@mueller-healthcare.de" },
        { type: "website", value: "https://mueller-healthcare.de" },
        { type: "x", value: "https://x.com/hansmueller" },
        { type: "whatsapp", value: "+493055551234" },
      ],
      summary: "Dr. Hans Müller is the Chief Medical Officer at Müller Healthcare, driving medical consulting and healthcare innovation.",
    },
    {
      id: "10",
      image_url: "https://placehold.co/600x400?text=Card+10",
      display_name: "Green Earth Co",
      created_at: "2026-05-19T11:00:00Z",
      company_name: "Green Earth Co",
      position: "Sustainability Lead",
      first_name: "Aisha",
      last_name: "Patel",
      services: ["Sustainability Consulting", "Environmental Impact Assessment", "Green Building"],
      addresses: ["1 Waterfront Dr, Cape Town, South Africa"],
      digital_contacts: [
        { type: "phone", value: "+27 21 555 6789" },
        { type: "email", value: "aisha@greenearth.co.za" },
        { type: "website", value: "https://greenearth.co.za" },
        { type: "instagram", value: "https://instagram.com/greenearthco" },
        { type: "linkedin", value: "https://linkedin.com/company/greenearthco" },
      ],
      summary: "Aisha Patel leads sustainability efforts at Green Earth Co, offering consulting and environmental assessment services.",
    },
  ]
}

const PAGE_SIZE = 10

let mockContacts = createMockContacts()
let nextId = 11

export function useContacts() {
  const searchQuery = ref("")
  const currentPage = ref(1)
  const contacts = ref<ContactCard[]>(mockContacts)

  const filteredContacts = computed(() => {
    const q = searchQuery.value.toLowerCase().trim()
    if (!q) return contacts.value
    return contacts.value.filter((c) =>
      c.display_name.toLowerCase().includes(q),
    )
  })

  const totalFiltered = computed(() => filteredContacts.value.length)

  const totalPages = computed(() => Math.max(1, Math.ceil(totalFiltered.value / PAGE_SIZE)))

  const paginatedContacts = computed(() => {
    const start = (currentPage.value - 1) * PAGE_SIZE
    return filteredContacts.value.slice(start, start + PAGE_SIZE)
  })

  async function deleteCard(id: string): Promise<void> {
    await delay(300)
    contacts.value = contacts.value.filter((c) => c.id !== id)
  }

  async function createCard(data: {
    display_name: string
    image_url: string
    first_name?: string
    last_name?: string
    middle_name?: string
    company_name?: string
    position?: string
    services: string[]
    addresses: string[]
    digital_contacts: ContactMethod[]
    summary?: string
  }): Promise<ContactCard> {
    await delay(400)
    const card: ContactCard = {
      id: String(nextId++),
      image_url: data.image_url,
      display_name: data.display_name,
      created_at: new Date().toISOString(),
      first_name: data.first_name,
      last_name: data.last_name,
      middle_name: data.middle_name,
      company_name: data.company_name,
      position: data.position,
      services: data.services,
      addresses: data.addresses,
      digital_contacts: data.digital_contacts,
      summary: data.summary,
    }
    contacts.value = [card, ...contacts.value]
    return card
  }

  async function updateCard(id: string, data: Partial<ContactCard>): Promise<ContactCard> {
    await delay(400)
    let updated = null as ContactCard | null
    contacts.value = contacts.value.map((c) => {
      if (c.id === id) {
        updated = { ...c, ...data }
        return updated
      }
      return c
    })
    return updated!
  }

  function simulateAutoPopulate(): Promise<{
    first_name: string
    last_name: string
    company_name: string
    position: string
    services: string[]
    addresses: string[]
    digital_contacts: ContactMethod[]
    summary: string
  }> {
    return delay(1200).then(() => ({
      first_name: "Alex",
      last_name: "Johnson",
      company_name: "Example Corp",
      position: "Software Engineer",
      services: ["Web Development", "API Design"],
      addresses: ["742 Evergreen Terrace, Springfield"],
      digital_contacts: [
        { type: "phone", value: "+1 555 000 0000" },
        { type: "email", value: "alex@example.com" },
        { type: "website", value: "https://example.com" },
        { type: "linkedin", value: "https://linkedin.com/in/alexjohnson" },
      ],
      summary: "Alex Johnson is a Software Engineer at Example Corp with expertise in web development and API design.",
    }))
  }

  return {
    searchQuery,
    currentPage,
    contacts,
    filteredContacts,
    paginatedContacts,
    totalFiltered,
    totalPages,
    pageSize: PAGE_SIZE,
    deleteCard,
    createCard,
    updateCard,
    simulateAutoPopulate,
  }
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}
