<script setup lang="ts">
import { Trash2 } from "@lucide/vue"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import type { SocialMedia } from "@/types/contact"
import { SocialPlatform } from "@/types/contact"

const platforms = Object.values(SocialPlatform)

const props = withDefaults(
  defineProps<{
    modelValue: SocialMedia[]
  }>(),
  {
    modelValue: () => [{ platform: SocialPlatform.TELEGRAM, username_or_link: "" }],
  },
)

const emit = defineEmits<{
  (e: "update:modelValue", items: SocialMedia[]): void
}>()

function addItem() {
  emit("update:modelValue", [
    ...props.modelValue,
    { platform: SocialPlatform.TELEGRAM, username_or_link: "" },
  ])
}

function removeItem(index: number) {
  emit(
    "update:modelValue",
    props.modelValue.filter((_, i) => i !== index),
  )
}

function updatePlatform(index: number, platform: SocialPlatform) {
  const next = [...props.modelValue]
  next[index] = { ...next[index], platform }
  emit("update:modelValue", next)
}

function updateLink(index: number, value: string) {
  const next = [...props.modelValue]
  next[index] = { ...next[index], username_or_link: value }
  emit("update:modelValue", next)
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <div
      v-for="(item, index) in modelValue"
      :key="index"
      class="flex items-center gap-2"
    >
      <Select
        :model-value="item.platform"
        @update:model-value="(v: SocialPlatform) => updatePlatform(index, v)"
      >
        <SelectTrigger class="min-w-0 flex-1">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem v-for="p in platforms" :key="p" :value="p">
            {{ p }}
          </SelectItem>
        </SelectContent>
      </Select>
      <Input
        :model-value="item.username_or_link"
        placeholder="Handle or URL"
        @update:model-value="(v: string) => updateLink(index, v)"
        class="min-w-0 flex-1"
      />
      <Button
        variant="ghost"
        size="icon-sm"
        type="button"
        class="shrink-0"
        @click="removeItem(index)"
      >
        <Trash2 class="size-4 text-destructive" />
      </Button>
    </div>
    <Button variant="outline" size="sm" type="button" class="w-full" @click="addItem">
      Add Social Media
    </Button>
  </div>
</template>
