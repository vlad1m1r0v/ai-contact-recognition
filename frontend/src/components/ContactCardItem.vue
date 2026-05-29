<script setup lang="ts">
import type { ContactCard } from "@/types/contact"

const props = defineProps<{
  card: ContactCard
}>()

const emit = defineEmits<{
  (e: "click", card: ContactCard): void
}>()

function formatTime(iso: string): string {
  const d = new Date(iso)
  const hh = String(d.getHours()).padStart(2, "0")
  const mm = String(d.getMinutes()).padStart(2, "0")
  const day = String(d.getDate()).padStart(2, "0")
  const month = String(d.getMonth() + 1).padStart(2, "0")
  const year = String(d.getFullYear()).slice(-2)
  return `${hh}:${mm} ${day}.${month}.${year}`
}
</script>

<template>
  <div
    class="bg-card hover:bg-accent/50 flex cursor-pointer flex-col overflow-hidden rounded-md border shadow-xs transition-colors"
    @click="emit('click', card)"
  >
    <div class="aspect-[3/2] w-full overflow-hidden">
      <img
        :src="card.image_url"
        :alt="card.display_name"
        class="h-full w-full object-cover"
      />
    </div>
    <div class="flex items-center justify-between gap-2 p-3">
      <span class="truncate font-medium text-sm">{{ card.display_name }}</span>
      <span class="text-muted-foreground shrink-0 text-xs">{{ formatTime(card.created_at) }}</span>
    </div>
  </div>
</template>
