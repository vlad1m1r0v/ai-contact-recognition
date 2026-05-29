<script setup lang="ts">
import { Input } from "@/components/ui/input"
import { Search } from "@lucide/vue"

const model = defineModel<string>("search")
</script>

<template>
  <div class="relative flex-1">
    <Search class="text-muted-foreground absolute top-1/2 left-3 size-4 -translate-y-1/2" />
    <Input
      v-model="model"
      placeholder="Search by display name..."
      class="w-full pl-9"
    />
  </div>
</template>
