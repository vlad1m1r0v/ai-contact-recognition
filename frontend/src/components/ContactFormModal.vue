<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { useForm, useField } from "vee-validate"
import { toTypedSchema } from "@vee-validate/yup"
import * as yup from "yup"
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
    display_name: string
    image_url: string
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
const isParsing = ref(false)

function buildInitialValues() {
  if (props.card) {
    return {
      first_name: props.card.first_name || "",
      last_name: props.card.last_name || "",
      middle_name: props.card.middle_name || "",
      company_name: props.card.company_name || "",
      positions: props.card.positions?.length ? props.card.positions : [""],
      summary: props.card.summary || "",
      services: props.card.services?.length ? props.card.services : [""],
      addresses: props.card.addresses?.length ? props.card.addresses : [""],
      digital_contacts: props.card.digital_contacts?.length
        ? props.card.digital_contacts
        : [{ type: "phone", value: "" }],
    }
  }
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

const isEditing = computed(() => !!props.card)

function stringItemError(v: string | undefined, min: number, max: number): string | undefined {
  if (!v || !v.trim()) return undefined
  const trimmed = v.trim()
  if (trimmed.length < min || trimmed.length > max) return `Must be ${min}-${max} characters if filled`
  return undefined
}

function digitalContactValueError(value: string | undefined, type: string): string | undefined {
  if (!value || !value.trim()) return undefined
  const v = value.trim()

  switch (type) {
    case "email":
      return yup.string().email().isValidSync(v) ? undefined : "Invalid email format"
    case "website":
      return yup.string().url().isValidSync(v) ? undefined : "Must be a valid URL"
    case "phone":
      return /^[\d\s+()-]+$/.test(v) ? undefined : "Only digits, spaces, +, -, and () allowed"
    case "whatsapp":
      return /^(https?:\/\/)?(wa\.me|whatsapp\.com)\/\w+\/?$|^[\d\s+()-]+$/.test(v)
        ? undefined
        : "Must be a WhatsApp URL or phone number"
    case "viber":
      return /^(https?:\/\/)?(viber\.me)\/[\w.-]+\/?$|^[\d\s+()-]+$/.test(v)
        ? undefined
        : "Must be a Viber URL or phone number"
    case "telegram":
      return /^(https?:\/\/)?(t\.me|telegram\.me)\/\w+\/?$|^@?\w{3,32}$/.test(v)
        ? undefined
        : "Must be a Telegram URL or @username"
    case "linkedin":
      return /^(https?:\/\/)?(www\.)?linkedin\.com\/in\/[\w-]+\/?$|^@?[\w-]{3,100}$/.test(v)
        ? undefined
        : "Must be a LinkedIn profile URL or @username"
    case "facebook":
      return /^(https?:\/\/)?(www\.)?(facebook\.com|fb\.com)\/[\w.]+\/?$|^@?[\w.]{3,}$/.test(v)
        ? undefined
        : "Must be a Facebook profile URL or @username"
    case "instagram":
      return /^(https?:\/\/)?(www\.)?instagram\.com\/[\w.]+\/?$|^@?[\w.]{3,}$/.test(v)
        ? undefined
        : "Must be an Instagram profile URL or @username"
    case "x":
      return /^(https?:\/\/)?(www\.)?x\.com\/\w+\/?$|^@?\w+$/.test(v)
        ? undefined
        : "Must be an X profile URL or @username"
    case "vk":
      return /^(https?:\/\/)?(vk\.com|vk\.ru)\/[\w.-]+\/?$|^@?[\w.-]+$/.test(v)
        ? undefined
        : "Must be a VK profile URL or @username"
    default:
      return undefined
  }
}

const formSchema = yup.object({
  first_name: yup
    .string()
    .test("first_name", "Minimum 2 characters", (v) => !v || !v.trim() || v.trim().length >= 2)
    .test("first_name", "Maximum 50 characters", (v) => !v || !v.trim() || v.trim().length <= 50),
  last_name: yup
    .string()
    .test("last_name", "Minimum 2 characters", (v) => !v || !v.trim() || v.trim().length >= 2)
    .test("last_name", "Maximum 50 characters", (v) => !v || !v.trim() || v.trim().length <= 50),
  middle_name: yup
    .string()
    .test("middle_name", "Minimum 2 characters", (v) => !v || !v.trim() || v.trim().length >= 2)
    .test("middle_name", "Maximum 50 characters", (v) => !v || !v.trim() || v.trim().length <= 50),
  company_name: yup
    .string()
    .test("company_name", "Minimum 2 characters", (v) => !v || !v.trim() || v.trim().length >= 2)
    .test("company_name", "Maximum 50 characters", (v) => !v || !v.trim() || v.trim().length <= 50),
  positions: yup.array().of(
    yup.string().test("pos", "Must be 3-100 characters if filled", (v) => !stringItemError(v, 3, 100)),
  ),
  summary: yup
    .string()
    .test("summary", "Minimum 10 characters", (v) => !v || !v.trim() || v.trim().length >= 10)
    .test("summary", "Maximum 250 characters", (v) => !v || !v.trim() || v.trim().length <= 250),
  services: yup.array().of(
    yup.string().test("svc", "Must be 3-100 characters if filled", (v) => !stringItemError(v, 3, 100)),
  ),
  addresses: yup.array().of(
    yup.string().test("addr", "Must be 3-100 characters if filled", (v) => !stringItemError(v, 3, 100)),
  ),
  digital_contacts: yup.array().of(
    yup.object({
      type: yup.string().required(),
      value: yup.string().test("dc-value", "Invalid value for the selected contact type", function (value) {
        if (!value || !value.trim()) return true
        return !digitalContactValueError(value, this.parent.type)
      }),
    }),
  ),
})

const { handleSubmit, setFieldValue, resetForm, values, meta } = useForm({
  validationSchema: toTypedSchema(formSchema),
  initialValues: buildInitialValues(),
})

const { value: firstName, errorMessage: firstNameErr } = useField<string>("first_name")
const { value: lastName, errorMessage: lastNameErr } = useField<string>("last_name")
const { value: middleName, errorMessage: middleNameErr } = useField<string>("middle_name")
const { value: companyName, errorMessage: companyNameErr } = useField<string>("company_name")
const { value: summary, errorMessage: summaryErr } = useField<string>("summary")

const positionsErrors = computed(() =>
  ((values.positions as string[]) || []).map((v) => stringItemError(v, 3, 100)),
)
const servicesErrors = computed(() =>
  ((values.services as string[]) || []).map((v) => stringItemError(v, 3, 100)),
)
const addressesErrors = computed(() =>
  ((values.addresses as string[]) || []).map((v) => stringItemError(v, 3, 100)),
)
const digitalContactsErrors = computed(() =>
  ((values.digital_contacts as ContactMethod[]) || []).map((d) => digitalContactValueError(d.value, d.type)),
)

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      resetForm({ values: buildInitialValues() })
      imagePreview.value = props.card?.image_url || null
      isParsing.value = false
    }
  },
)

function onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  imagePreview.value = URL.createObjectURL(file)
  isParsing.value = true

  const { simulateAutoPopulate } = useContactsInternal()
  simulateAutoPopulate().then((mockData) => {
    const defaults = buildInitialValues()
    resetForm({
      values: {
        ...defaults,
        ...mockData,
        services: mockData.services?.length ? mockData.services : [""],
        addresses: mockData.addresses?.length ? mockData.addresses : [""],
        digital_contacts: mockData.digital_contacts?.length
          ? mockData.digital_contacts
          : [{ type: "phone", value: "" }],
      },
    })
    isParsing.value = false
  })
}

function useContactsInternal() {
  const delay = (ms: number) => new Promise<void>((r) => setTimeout(r, ms))
  async function simulateAutoPopulate() {
    await delay(1200)
    return {
      first_name: "Alex",
      last_name: "Johnson",
      company_name: "Example Corp",
      position: "Software Engineer",
      services: ["Web Development", "API Design"],
      addresses: ["742 Evergreen Terrace, Springfield"],
      digital_contacts: [
        { type: "phone", value: "+1 555 000 0000" },
        { type: "email", value: "alex@example.com" },
        { type: "website", value: "https://example.com" },
        { type: "linkedin", value: "https://linkedin.com/in/alexjohnson" },
      ] as ContactMethod[],
      summary: "Alex Johnson is a Software Engineer at Example Corp with expertise in web development and API design.",
    }
  }
  return { simulateAutoPopulate }
}

const onSubmit = handleSubmit((formValues) => {
  const company = formValues.company_name?.trim()
  const first = formValues.first_name?.trim() || ""
  const last = formValues.last_name?.trim() || ""
  const middle = formValues.middle_name?.trim() || ""
  const fullName = [first, middle, last].filter(Boolean).join(" ")
  const displayName = company || fullName || "Unnamed Organization"

  const imageUrl = imagePreview.value || "https://placehold.co/600x400?text=Card"

  const services = (formValues.services ?? []).filter((s): s is string => !!s?.trim())
  const addresses = (formValues.addresses ?? []).filter((a): a is string => !!a?.trim())
  const digitalContacts = (formValues.digital_contacts ?? []).filter((d): d is ContactMethod => !!d.value?.trim())

  const data = {
    display_name: displayName,
    image_url: imageUrl,
    first_name: formValues.first_name?.trim() || undefined,
    last_name: formValues.last_name?.trim() || undefined,
    middle_name: formValues.middle_name?.trim() || undefined,
    company_name: formValues.company_name?.trim() || undefined,
    positions: (formValues.positions ?? []).filter((p): p is string => !!p?.trim()),
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
        <DialogTitle>{{ isEditing ? "Edit Contact" : "Add New Contact" }}</DialogTitle>
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

          <Button type="button" variant="outline" class="w-full" @click="triggerFileInput">
            <ImagePlus class="mr-1 size-4" />
            {{ imagePreview ? "Change Image" : "Upload Image" }}
          </Button>
          <div v-if="isParsing" class="flex items-center justify-center gap-2">
            <Loader2 class="size-4 animate-spin text-muted-foreground" />
            <span class="text-muted-foreground text-xs">Parsing card...</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">First Name</label>
            <Input
              v-model="firstName"
              placeholder="John"
              :class="firstNameErr && 'border-destructive'"
            />
            <span v-if="firstNameErr" class="text-destructive text-xs">{{ firstNameErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Last Name</label>
            <Input
              v-model="lastName"
              placeholder="Doe"
              :class="lastNameErr && 'border-destructive'"
            />
            <span v-if="lastNameErr" class="text-destructive text-xs">{{ lastNameErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Middle Name</label>
            <Input
              v-model="middleName"
              placeholder="James"
              :class="middleNameErr && 'border-destructive'"
            />
            <span v-if="middleNameErr" class="text-destructive text-xs">{{ middleNameErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Company Name</label>
            <Input
              v-model="companyName"
              placeholder="Acme Corp"
              :class="companyNameErr && 'border-destructive'"
            />
            <span v-if="companyNameErr" class="text-destructive text-xs">{{ companyNameErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Positions</label>
            <DynamicFormset
              :model-value="(values.positions as string[]) || ['']"
              @update:model-value="(v: string[]) => setFieldValue('positions', v)"
              placeholder="Enter a position"
              :errors="positionsErrors"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Summary</label>
            <textarea
              v-model="summary"
              placeholder="1-2 sentence brief description..."
              class="border-input placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 flex h-20 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-xs transition-[color,box-shadow] outline-none focus-visible:ring-[3px]"
              :class="summaryErr && 'border-destructive'"
            />
            <span v-if="summaryErr" class="text-destructive text-xs">{{ summaryErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Services</label>
            <DynamicFormset
              :model-value="(values.services as string[]) || ['']"
              @update:model-value="(v: string[]) => setFieldValue('services', v)"
              placeholder="Enter a service"
              :errors="servicesErrors"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Addresses</label>
            <DynamicFormset
              :model-value="(values.addresses as string[]) || ['']"
              @update:model-value="(v: string[]) => setFieldValue('addresses', v)"
              placeholder="Enter an address"
              :errors="addressesErrors"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Digital Contacts</label>
            <DigitalContactFormset
              :model-value="(values.digital_contacts as ContactMethod[]) || [{ type: 'phone', value: '' }]"
              @update:model-value="(v: ContactMethod[]) => setFieldValue('digital_contacts', v)"
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
