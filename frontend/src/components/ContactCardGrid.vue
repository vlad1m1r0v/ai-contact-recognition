<script setup lang="ts">
import type { ContactCard } from "@/types/contact"
import ContactCardItem from "./ContactCardItem.vue"

defineProps<{
  cards: ContactCard[]
}>()

const emit = defineEmits<{
  (e: "card-click", card: ContactCard): void
}>()
</script>

<template>
  <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    <ContactCardItem
      v-for="card in cards"
      :key="card.id"
      :card="card"
      @click="emit('card-click', card)"
    />
  </div>
</template>
