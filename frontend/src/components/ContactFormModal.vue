<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { useForm } from "vee-validate"
import { toTypedSchema } from "@vee-validate/yup"
import { ImagePlus, Loader2 } from "@lucide/vue"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Dialog,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import DialogScrollContent from "@/components/ui/dialog/DialogScrollContent.vue"
import {
  formSchema,
  getPositionErrors,
  getServiceErrors,
  getAddressErrors,
  getDigitalContactErrors,
} from "@/lib/validation"
import { extractContact } from "@/lib/api"
import type { ContactCard, ContactMethod } from "@/types/contact"
import DynamicFormset from "./DynamicFormset.vue"
import DigitalContactFormset from "./DigitalContactFormset.vue"

const props = withDefaults(
  defineProps<{
    open: boolean
    card?: ContactCard | null
  }>(),
  { card: null },
)

const emit = defineEmits<{
  (e: "update:open", value: boolean): void
  (e: "save", data: {
    image_base64: string
    first_name?: string
    last_name?: string
    middle_name?: string
    company_name?: string
    positions: string[]
    services: string[]
    addresses: string[]
    digital_contacts: ContactMethod[]
    summary?: string
  }): void
  (e: "update", data: { id: string } & Record<string, unknown>): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const imagePreview = ref<string | null>(null)
const imageBase64 = ref<string>("")
const isParsing = ref(false)
const isEditing = ref(false)

function buildInitialValues() {
  if (props.card) {
    isEditing.value = true
    return {
      first_name: props.card.first_name || "",
      last_name: props.card.last_name || "",
      middle_name: props.card.middle_name || "",
      company_name: props.card.company_name || "",
      positions:
        props.card.positions?.length ? props.card.positions : [""],
      summary: props.card.summary || "",
      services: props.card.services?.length ? props.card.services : [""],
      addresses: props.card.addresses?.length ? props.card.addresses : [""],
      digital_contacts: props.card.digital_contacts?.length
        ? props.card.digital_contacts
        : [{ type: "phone", value: "" }],
    }
  }
  isEditing.value = false
  return {
    first_name: "",
    last_name: "",
    middle_name: "",
    company_name: "",
    positions: [""],
    summary: "",
    services: [""],
    addresses: [""],
    digital_contacts: [{ type: "phone", value: "" } as ContactMethod],
  }
}

const { defineField, handleSubmit, setFieldValue, resetForm, values, errors, meta } =
  useForm({
    validationSchema: toTypedSchema(formSchema),
    initialValues: buildInitialValues(),
  })

const [firstName, firstNameProps] = defineField("first_name")
const [lastName, lastNameProps] = defineField("last_name")
const [middleName, middleNameProps] = defineField("middle_name")
const [companyName, companyNameProps] = defineField("company_name")
const [summary, summaryProps] = defineField("summary")

const positionsErrors = computed(() =>
  getPositionErrors((values.positions as string[]) || []),
)
const servicesErrors = computed(() =>
  getServiceErrors((values.services as string[]) || []),
)
const addressesErrors = computed(() =>
  getAddressErrors((values.addresses as string[]) || []),
)
const digitalContactsErrors = computed(() =>
  getDigitalContactErrors((values.digital_contacts as ContactMethod[]) || []),
)

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      resetForm({ values: buildInitialValues() })
      imagePreview.value = props.card?.image_url || null
      imageBase64.value = ""
      isParsing.value = false
    }
  },
)

async function onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  imagePreview.value = URL.createObjectURL(file)

  const reader = new FileReader()
  reader.onload = async () => {
    const base64 = reader.result as string
    imageBase64.value = base64
    if (props.card) return

    isParsing.value = true
    try {
      const extracted = await extractContact(file)
      const defaults = buildInitialValues()
      resetForm({
        values: {
          ...defaults,
          first_name: extracted.first_name || "",
          last_name: extracted.last_name || "",
          middle_name: extracted.middle_name || "",
          company_name: extracted.company_name || "",
          positions:
            extracted.positions?.length ? extracted.positions : [""],
          summary: extracted.summary || "",
          services:
            extracted.services?.length ? extracted.services : [""],
          addresses:
            extracted.addresses?.length ? extracted.addresses : [""],
          digital_contacts: extracted.digital_contacts?.length
            ? extracted.digital_contacts
            : [{ type: "phone", value: "" }],
        },
      })
    } catch {
      // extraction failed – leave fields empty
    } finally {
      isParsing.value = false
    }
  }
  reader.readAsDataURL(file)
}

const onSubmit = handleSubmit((formValues) => {
  const services = (formValues.services ?? []).filter(
    (s): s is string => !!s?.trim(),
  )
  const addresses = (formValues.addresses ?? []).filter(
    (a): a is string => !!a?.trim(),
  )
  const digitalContacts = (formValues.digital_contacts ?? []).filter(
    (d): d is ContactMethod => !!d.value?.trim(),
  )
  const positions = (formValues.positions ?? []).filter(
    (p): p is string => !!p?.trim(),
  )

  const data = {
    image_base64: imageBase64.value,
    first_name: formValues.first_name?.trim() || undefined,
    last_name: formValues.last_name?.trim() || undefined,
    middle_name: formValues.middle_name?.trim() || undefined,
    company_name: formValues.company_name?.trim() || undefined,
    positions,
    services,
    addresses,
    digital_contacts: digitalContacts,
    summary: formValues.summary?.trim() || undefined,
  }

  emit("save", data)
  emit("update:open", false)
})

function triggerFileInput() {
  fileInput.value?.click()
}
</script>

<template>
  <Dialog :open="open" @update:open="emit('update:open', $event)">
    <DialogScrollContent class="sm:max-w-xl gap-4">
      <DialogHeader class="shrink-0">
        <DialogTitle>{{
          isEditing ? "Edit Contact" : "Add New Contact"
        }}</DialogTitle>
      </DialogHeader>

      <form @submit="onSubmit" class="flex min-h-0 flex-1 flex-col">
        <div class="flex-1 space-y-4 overflow-y-auto pr-1 min-h-0">
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="onFileSelected"
          />

          <div v-if="imagePreview">
            <img
              :src="imagePreview"
              alt="Preview"
              class="max-h-40 w-full rounded-md object-contain"
            />
          </div>

          <Button
            type="button"
            variant="outline"
            class="w-full"
            @click="triggerFileInput"
          >
            <ImagePlus class="mr-1 size-4" />
            {{ imagePreview ? "Change Image" : "Upload Image" }}
          </Button>
          <div
            v-if="isParsing"
            class="flex items-center justify-center gap-2"
          >
            <Loader2 class="size-4 animate-spin text-muted-foreground" />
            <span class="text-muted-foreground text-xs">Parsing card...</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >First Name</label
            >
            <Input
              v-model="firstName"
              v-bind="firstNameProps"
              placeholder="John"
            />
            <span
              v-if="errors.first_name"
              class="text-destructive text-xs"
              >{{ errors.first_name }}</span
            >
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >Last Name</label
            >
            <Input
              v-model="lastName"
              v-bind="lastNameProps"
              placeholder="Doe"
            />
            <span
              v-if="errors.last_name"
              class="text-destructive text-xs"
              >{{ errors.last_name }}</span
            >
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >Middle Name</label
            >
            <Input
              v-model="middleName"
              v-bind="middleNameProps"
              placeholder="James"
            />
            <span
              v-if="errors.middle_name"
              class="text-destructive text-xs"
              >{{ errors.middle_name }}</span
            >
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >Company Name</label
            >
            <Input
              v-model="companyName"
              v-bind="companyNameProps"
              placeholder="Acme Corp"
            />
            <span
              v-if="errors.company_name"
              class="text-destructive text-xs"
              >{{ errors.company_name }}</span
            >
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >Positions</label
            >
            <DynamicFormset
              :model-value="(values.positions as string[]) || ['']"
              @update:model-value="
                (v: string[]) => setFieldValue('positions', v)
              "
              placeholder="Enter a position"
              :errors="positionsErrors"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >Summary</label
            >
            <textarea
              v-model="summary"
              v-bind="summaryProps"
              placeholder="1-2 sentence brief description..."
              class="border-input placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 flex h-20 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-xs transition-[color,box-shadow] outline-none focus-visible:ring-[3px]"
            />
            <span
              v-if="errors.summary"
              class="text-destructive text-xs"
              >{{ errors.summary }}</span
            >
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >Services</label
            >
            <DynamicFormset
              :model-value="(values.services as string[]) || ['']"
              @update:model-value="
                (v: string[]) => setFieldValue('services', v)
              "
              placeholder="Enter a service"
              :errors="servicesErrors"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >Addresses</label
            >
            <DynamicFormset
              :model-value="(values.addresses as string[]) || ['']"
              @update:model-value="
                (v: string[]) => setFieldValue('addresses', v)
              "
              placeholder="Enter an address"
              :errors="addressesErrors"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium"
              >Digital Contacts</label
            >
            <DigitalContactFormset
              :model-value="
                (values.digital_contacts as ContactMethod[]) || [
                  { type: 'phone', value: '' },
                ]
              "
              @update:model-value="
                (v: ContactMethod[]) => setFieldValue('digital_contacts', v)
              "
              :errors="digitalContactsErrors"
            />
          </div>
        </div>

        <DialogFooter class="border-border shrink-0 border-t pt-4">
          <Button type="submit" class="w-full" :disabled="!meta.valid">
            {{ isEditing ? "Update Contact" : "Save Contact" }}
          </Button>
        </DialogFooter>
      </form>
    </DialogScrollContent>
  </Dialog>
</template>
