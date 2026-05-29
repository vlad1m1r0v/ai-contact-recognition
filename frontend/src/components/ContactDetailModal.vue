<script setup lang="ts">
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import DialogScrollContent from "@/components/ui/dialog/DialogScrollContent.vue"
import type { ContactCard } from "@/types/contact"

defineProps<{
  card: ContactCard
  open: boolean
}>()

const emit = defineEmits<{
  (e: "update:open", value: boolean): void
  (e: "edit", card: ContactCard): void
  (e: "delete", id: string): void
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
  <Dialog :open="open" @update:open="emit('update:open', $event)">
    <DialogScrollContent class="sm:max-w-xl gap-4">
      <DialogHeader class="shrink-0">
        <DialogTitle>{{ card.display_name }}</DialogTitle>
      </DialogHeader>

      <div class="flex min-h-0 flex-1 flex-col gap-3">
        <div class="aspect-[3/2] w-full shrink-0 overflow-hidden rounded-lg">
          <img
            :src="card.image_url"
            :alt="card.display_name"
            class="h-full w-full object-cover"
          />
        </div>

        <div class="flex flex-1 flex-col gap-3 overflow-y-auto text-sm">
          <div v-if="card.company_name" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Company</span>
            <span>{{ card.company_name }}</span>
          </div>

          <div v-if="card.position" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Position</span>
            <span>{{ card.position }}</span>
          </div>

          <div v-if="card.first_name || card.last_name" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Name</span>
            <span>{{ [card.first_name, card.middle_name, card.last_name].filter(Boolean).join(" ") }}</span>
          </div>

          <div v-if="card.phone_number" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Phone</span>
            <span>{{ card.phone_number }}</span>
          </div>

          <div v-if="card.email" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Email</span>
            <span>{{ card.email }}</span>
          </div>

          <div v-if="card.website" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Website</span>
            <span>{{ card.website }}</span>
          </div>

          <div v-if="card.services.length" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Services</span>
            <ul class="list-inside list-disc">
              <li v-for="s in card.services" :key="s">{{ s }}</li>
            </ul>
          </div>

          <div v-if="card.addresses.length" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Addresses</span>
            <ul class="list-inside list-disc">
              <li v-for="a in card.addresses" :key="a">{{ a }}</li>
            </ul>
          </div>

          <div v-if="card.social_media.length" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Social Media</span>
            <ul class="list-inside list-disc">
              <li v-for="s in card.social_media" :key="s.platform + s.username_or_link">
                {{ s.platform }}: {{ s.username_or_link }}
              </li>
            </ul>
          </div>

          <div v-if="card.summary" class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Summary</span>
            <p class="text-sm leading-relaxed">{{ card.summary }}</p>
          </div>

          <div class="flex flex-col">
            <span class="text-muted-foreground text-xs font-medium uppercase">Scanned At</span>
            <span>{{ formatTime(card.created_at) }}</span>
          </div>
        </div>
      </div>

      <DialogFooter class="shrink-0">
        <div class="grid w-full grid-cols-1 gap-2 sm:grid-cols-3">
          <Button
            variant="destructive"
            @click="emit('delete', card.id)"
          >
            Delete Contact
          </Button>
          <DialogClose as-child>
            <Button variant="outline">Close</Button>
          </DialogClose>
          <Button @click="emit('edit', card)">
            Edit Contact
          </Button>
        </div>
      </DialogFooter>
    </DialogScrollContent>
  </Dialog>
</template>
