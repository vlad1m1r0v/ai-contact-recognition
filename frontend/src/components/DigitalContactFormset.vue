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
import type { ContactMethod } from "@/types/contact"

const contactTypes = [
  "phone",
  "email",
  "website",
  "telegram",
  "linkedin",
  "whatsapp",
  "facebook",
  "instagram",
  "viber",
  "x",
  "vk",
]

const props = withDefaults(
  defineProps<{
    modelValue: ContactMethod[]
    errors?: (string | undefined)[]
  }>(),
  {
    modelValue: () => [{ type: "phone", value: "" }],
    errors: () => [],
  },
)

const emit = defineEmits<{
  (e: "update:modelValue", items: ContactMethod[]): void
}>()

function addItem() {
  emit("update:modelValue", [
    ...props.modelValue,
    { type: "phone", value: "" },
  ])
}

function removeItem(index: number) {
  emit(
    "update:modelValue",
    props.modelValue.filter((_, i) => i !== index),
  )
}

function updateType(index: number, type: string) {
  const next = [...props.modelValue]
  next[index] = { ...next[index], type }
  emit("update:modelValue", next)
}

function updateValue(index: number, value: string) {
  const next = [...props.modelValue]
  next[index] = { ...next[index], value }
  emit("update:modelValue", next)
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <div
      v-for="(item, index) in modelValue"
      :key="index"
      class="flex flex-col gap-1"
    >
      <div class="flex items-center gap-2">
        <Select
          :model-value="item.type"
          @update:model-value="(v: unknown) => updateType(index, String(v))"
        >
          <SelectTrigger class="min-w-0 flex-1" :class="errors?.[index] && 'border-destructive'">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem v-for="t in contactTypes" :key="t" :value="t">
              {{ t }}
            </SelectItem>
          </SelectContent>
        </Select>
        <Input
          :model-value="item.value"
          placeholder="Value"
          @update:model-value="(v: unknown) => updateValue(index, String(v))"
          class="min-w-0 flex-1"
          :class="errors?.[index] && 'border-destructive'"
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
      <span v-if="errors?.[index]" class="text-destructive text-xs">{{ errors[index] }}</span>
    </div>
    <Button variant="outline" size="sm" type="button" class="w-full" @click="addItem">
      Add Contact Method
    </Button>
  </div>
</template>
