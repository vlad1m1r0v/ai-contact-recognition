<script setup lang="ts">
import { Trash2 } from "@lucide/vue"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const props = withDefaults(
  defineProps<{
    modelValue: string[]
    maxLength?: number
    placeholder?: string
    minLength?: number
  }>(),
  {
    maxLength: 100,
    placeholder: "Enter a value",
    minLength: 3,
  },
)

const emit = defineEmits<{
  (e: "update:modelValue", items: string[]): void
}>()

function addItem() {
  emit("update:modelValue", [...props.modelValue, ""])
}

function removeItem(index: number) {
  emit(
    "update:modelValue",
    props.modelValue.filter((_, i) => i !== index),
  )
}

function updateItem(index: number, value: string) {
  const next = [...props.modelValue]
  next[index] = value
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
      <Input
        :model-value="item"
        :placeholder="placeholder"
        @update:model-value="updateItem(index, $event)"
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
      Add Item
    </Button>
  </div>
</template>
