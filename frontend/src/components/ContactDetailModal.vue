<script setup lang="ts">
import {computed, ref} from "vue"
import {Button} from "@/components/ui/button"
import {Skeleton} from "@/components/ui/skeleton"
import {
  Dialog,
  DialogClose,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import DialogScrollContent from "@/components/ui/dialog/DialogScrollContent.vue"
import type {ContactCard} from "@/types/contact"

const props = defineProps<{
  card: ContactCard | null
  open: boolean
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: "update:open", value: boolean): void
  (e: "edit", card: ContactCard): void
  (e: "delete", id: string): void
}>()

const confirmingDelete = ref(false)

const displayName = computed(() => {
  if (!props.card) return ""
  const parts = [props.card.first_name, props.card.middle_name, props.card.last_name].filter(Boolean)
  return props.card.company_name || parts.join(" ") || "Unnamed"
})

function formatTime(iso: string): string {
  if (!iso) return ""
  const d = new Date(iso)
  const hh = String(d.getHours()).padStart(2, "0")
  const mm = String(d.getMinutes()).padStart(2, "0")
  const day = String(d.getDate()).padStart(2, "0")
  const month = String(d.getMonth() + 1).padStart(2, "0")
  const year = String(d.getFullYear()).slice(-2)
  return `${hh}:${mm} ${day}.${month}.${year}`
}

function confirmDelete() {
  if (props.card) {
    emit("delete", props.card.id)
  }
  confirmingDelete.value = false
}
</script>

<template>
  <Dialog :open="open" @update:open="emit('update:open', $event)">
    <DialogScrollContent class="sm:max-w-xl gap-4">
      <template v-if="loading">
        <DialogHeader class="shrink-0">
          <Skeleton class="h-6 w-48" />
        </DialogHeader>
        <div class="flex min-h-0 flex-1 flex-col gap-3">
          <Skeleton class="aspect-[3/2] w-full rounded-lg" />
          <div class="flex flex-col gap-2">
            <Skeleton class="h-3 w-16" />
            <Skeleton class="h-4 w-40" />
          </div>
          <div class="flex flex-col gap-2">
            <Skeleton class="h-3 w-16" />
            <Skeleton class="h-4 w-32" />
          </div>
          <div class="flex flex-col gap-2">
            <Skeleton class="h-3 w-16" />
            <Skeleton class="h-4 w-56" />
          </div>
        </div>
        <DialogFooter class="shrink-0">
          <div class="grid w-full grid-cols-1 gap-2 sm:grid-cols-3">
            <Skeleton class="h-9 w-full" />
            <Skeleton class="h-9 w-full" />
            <Skeleton class="h-9 w-full" />
          </div>
        </DialogFooter>
      </template>

      <template v-else-if="card && confirmingDelete">
        <DialogHeader class="shrink-0">
          <DialogTitle>Delete Contact</DialogTitle>
        </DialogHeader>
        <p class="text-muted-foreground text-sm">
          Are you sure you want to delete <strong>{{ displayName }}</strong>? This action cannot be undone.
        </p>
        <DialogFooter class="shrink-0">
          <div class="grid w-full grid-cols-1 gap-2 sm:grid-cols-2">
            <Button variant="outline" @click="confirmingDelete = false">
              Cancel
            </Button>
            <Button variant="destructive" @click="confirmDelete">
              Delete
            </Button>
          </div>
        </DialogFooter>
      </template>

      <template v-else-if="card">
        <DialogHeader class="shrink-0">
          <DialogTitle>{{ displayName }}</DialogTitle>
        </DialogHeader>

        <div class="flex min-h-0 flex-1 flex-col gap-3">
          <div class="aspect-[3/2] w-full shrink-0 overflow-hidden rounded-lg">
            <img
                :src="card.image_url"
                :alt="displayName"
                class="h-full w-full object-cover"
            />
          </div>

          <div class="flex flex-1 flex-col gap-3 overflow-y-auto text-sm">
            <div v-if="card.company_name" class="flex flex-col">
              <span class="text-muted-foreground text-xs font-medium uppercase">Company</span>
              <span>{{ card.company_name }}</span>
            </div>

            <div v-if="card.positions?.length" class="flex flex-col">
              <span class="text-muted-foreground text-xs font-medium uppercase">Positions</span>
              <ul class="list-inside list-disc">
                <li v-for="p in card.positions" :key="p">{{ p }}</li>
              </ul>
            </div>

            <div v-if="card.first_name || card.last_name" class="flex flex-col">
              <span class="text-muted-foreground text-xs font-medium uppercase">Name</span>
              <span>{{ [card.first_name, card.middle_name, card.last_name].filter(Boolean).join(" ") }}</span>
            </div>

            <div v-if="card.digital_contacts.length" class="flex flex-col">
              <span class="text-muted-foreground text-xs font-medium uppercase">Digital Contacts</span>
              <ul class="list-inside list-disc">
                <li v-for="(dc, i) in card.digital_contacts" :key="i">
                  {{ dc.type }}: {{ dc.value }}
                </li>
              </ul>
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
            <DialogClose as-child>
              <Button variant="outline">Close</Button>
            </DialogClose>
            <Button @click="emit('edit', card)">
              Edit Contact
            </Button>
            <Button
                variant="destructive"
                @click="confirmingDelete = true"
            >
              Delete Contact
            </Button>
          </div>
        </DialogFooter>
      </template>
    </DialogScrollContent>
  </Dialog>
</template>
