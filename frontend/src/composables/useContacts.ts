import { ref, computed, watch } from "vue"
import { watchDebounced } from "@vueuse/core"
import { toast } from "vue-sonner"
import {
  getContacts as apiGetContacts,
  createContact as apiCreateContact,
  updateContact as apiUpdateContact,
  deleteContact as apiDeleteContact,
} from "@/lib/api"
import type { CardListItem, ContactCard, ContactMethod } from "@/types/contact"

const PAGE_SIZE = 10

export function useContacts() {
  const searchQuery = ref("")
  const currentPage = ref(1)
  const contacts = ref<CardListItem[]>([])
  const totalItems = ref(0)
  const isLoading = ref(false)
  const isSaving = ref(false)
  const error = ref<string | null>(null)

  const totalPages = computed(() =>
    Math.max(1, Math.ceil(totalItems.value / PAGE_SIZE)),
  )

  async function fetchContacts() {
    isLoading.value = true
    error.value = null
    try {
      const res = await apiGetContacts(
        currentPage.value,
        PAGE_SIZE,
        searchQuery.value || undefined,
      )
      contacts.value = res.items
      totalItems.value = res.total
    } catch (e) {
      error.value = (e as Error).message
      contacts.value = []
      totalItems.value = 0
    } finally {
      isLoading.value = false
    }
  }

  watchDebounced(searchQuery, fetchContacts, { debounce: 300, immediate: true })
  watch(currentPage, fetchContacts)

  async function deleteCard(id: string): Promise<void> {
    try {
      await apiDeleteContact(id)
      toast.success("Contact deleted")
      currentPage.value = 1
      await fetchContacts()
    } catch (e) {
      toast.error((e as Error).message)
      throw e
    }
  }

  async function createCard(data: {
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
    isSaving.value = true
    try {
      const card = await apiCreateContact(data)
      toast.success("Contact created")
      currentPage.value = 1
      await fetchContacts()
      return card
    } catch (e) {
      toast.error((e as Error).message)
      throw e
    } finally {
      isSaving.value = false
    }
  }

  async function updateCard(
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
    isSaving.value = true
    try {
      const card = await apiUpdateContact(id, data)
      toast.success("Contact updated")
      await fetchContacts()
      return card
    } catch (e) {
      toast.error((e as Error).message)
      throw e
    } finally {
      isSaving.value = false
    }
  }

  return {
    searchQuery,
    currentPage,
    contacts,
    totalItems,
    totalPages,
    isLoading,
    isSaving,
    error,
    pageSize: PAGE_SIZE,
    deleteCard,
    createCard,
    updateCard,
    fetchContacts,
  }
}
