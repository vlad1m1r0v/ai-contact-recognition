<script setup lang="ts">
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationFirst,
  PaginationItem,
  PaginationLast,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"

const props = defineProps<{
  total: number
  page: number
  pageSize: number
}>()

const emit = defineEmits<{
  (e: "update:page", page: number): void
}>()

const totalPages = Math.max(1, Math.ceil(props.total / props.pageSize))

function goTo(p: number) {
  if (p >= 1 && p <= totalPages) {
    emit("update:page", p)
  }
}

function range(): (number | "ellipsis")[] {
  const pages: (number | "ellipsis")[] = []
  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) pages.push(i)
  } else {
    pages.push(1)
    if (props.page > 3) pages.push("ellipsis")
    for (let i = Math.max(2, props.page - 1); i <= Math.min(totalPages - 1, props.page + 1); i++) {
      pages.push(i)
    }
    if (props.page < totalPages - 2) pages.push("ellipsis")
    pages.push(totalPages)
  }
  return pages
}
</script>

<template>
  <Pagination v-if="totalPages > 1" :page="page" :total="totalPages" :items-per-page="1">
    <PaginationContent>
      <PaginationFirst @click="goTo(1)" :disabled="page === 1" />
      <PaginationPrevious @click="goTo(page - 1)" :disabled="page === 1" />

      <template v-for="p in range()" :key="typeof p === 'number' ? p : 'e' + Math.random()">
        <PaginationEllipsis v-if="p === 'ellipsis'" />
        <PaginationItem v-else :value="p" :is-active="p === page" @click="goTo(p)">
          {{ p }}
        </PaginationItem>
      </template>

      <PaginationNext @click="goTo(page + 1)" :disabled="page === totalPages" />
      <PaginationLast @click="goTo(totalPages)" :disabled="page === totalPages" />
    </PaginationContent>
  </Pagination>
</template>
