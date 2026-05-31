<script setup lang="ts">
import { ref } from "vue"
import { Plus } from "@lucide/vue"
import { Button } from "@/components/ui/button"
import SearchBar from "@/components/SearchBar.vue"
import ContactCardGrid from "@/components/ContactCardGrid.vue"
import AppPagination from "@/components/AppPagination.vue"
import ContactDetailModal from "@/components/ContactDetailModal.vue"
import ContactFormModal from "@/components/ContactFormModal.vue"
import { useContacts } from "@/composables/useContacts"
import { getContact } from "@/lib/api"
import type { CardListItem, ContactCard, ContactMethod } from "@/types/contact"

const {
  searchQuery,
  currentPage,
  contacts,
  totalItems,
  totalPages,
  pageSize,
  isLoading,
  error,
  deleteCard,
  createCard,
  updateCard,
} = useContacts()

const showDetailModal = ref(false)
const showFormModal = ref(false)
const selectedCard = ref<ContactCard | null>(null)
const editingCard = ref<ContactCard | null>(null)

async function openDetail(card: CardListItem) {
  try {
    selectedCard.value = await getContact(card.id)
  } catch {
    selectedCard.value = null
  }
  showDetailModal.value = true
}

function openFormForAdd() {
  editingCard.value = null
  showFormModal.value = true
}

function openFormForEdit(card: ContactCard) {
  showDetailModal.value = false
  editingCard.value = card
  showFormModal.value = true
}

async function handleDelete(id: string) {
  await deleteCard(id)
  showDetailModal.value = false
  selectedCard.value = null
}

interface SavePayload {
  image_base64: string
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

async function handleSave(data: SavePayload) {
  if (editingCard.value) {
    const { image_base64, ...rest } = data
    const payload = image_base64 ? data : rest
    await updateCard(editingCard.value.id, payload)
    editingCard.value = null
  } else {
    await createCard(data)
  }
}
</script>

<template>
  <div class="container mx-auto flex max-w-300 flex-col gap-6 p-4">
    <div class="flex items-center gap-3">
      <SearchBar v-model:search="searchQuery" />
      <Button @click="openFormForAdd">
        <Plus class="size-4" />
        Add New Contact
      </Button>
    </div>

    <hr class="border-border" />

    <div v-if="isLoading" class="text-muted-foreground py-12 text-center text-sm">
      Loading contacts...
    </div>
    <div
      v-else-if="error"
      class="text-destructive py-12 text-center text-sm"
    >
      {{ error }}
    </div>
    <ContactCardGrid
      v-else-if="contacts.length"
      :cards="contacts"
      @card-click="openDetail"
    />
    <div v-else class="text-muted-foreground py-12 text-center text-sm">
      No contacts found.
    </div>

    <AppPagination
      v-if="totalPages > 1"
      :total="totalItems"
      :page="currentPage"
      :page-size="pageSize"
      @update:page="currentPage = $event"
    />

    <ContactDetailModal
      v-if="selectedCard"
      :open="showDetailModal"
      :card="selectedCard"
      @update:open="showDetailModal = $event"
      @edit="openFormForEdit"
      @delete="handleDelete"
    />

    <ContactFormModal
      :open="showFormModal"
      :card="editingCard"
      @update:open="
        (v) => {
          showFormModal = v
          if (!v) editingCard = null
        }
      "
      @save="handleSave"
    />
  </div>
</template>
