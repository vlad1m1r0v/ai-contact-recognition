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
import type { ContactCard, ContactMethod } from "@/types/contact"

const {
  searchQuery,
  currentPage,
  paginatedContacts,
  totalFiltered,
  totalPages,
  pageSize,
  deleteCard,
  createCard,
} = useContacts()

const showDetailModal = ref(false)
const showFormModal = ref(false)
const selectedCard = ref<ContactCard | null>(null)
const editingCard = ref<ContactCard | null>(null)

function openDetail(card: ContactCard) {
  selectedCard.value = card
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

async function handleSave(data: {
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
}) {
  await createCard(data)
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

    <ContactCardGrid
      v-if="paginatedContacts.length"
      :cards="paginatedContacts"
      @card-click="openDetail"
    />
    <div v-else class="text-muted-foreground py-12 text-center text-sm">
      No contacts found.
    </div>

    <AppPagination
      v-if="totalPages > 1"
      :total="totalFiltered"
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
      @update:open="showFormModal = $event"
      @save="handleSave"
    />
  </div>
</template>
