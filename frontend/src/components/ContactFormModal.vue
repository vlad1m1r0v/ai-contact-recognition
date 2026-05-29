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
import type { ContactCard, SocialMedia } from "@/types/contact"
import { SocialPlatform } from "@/types/contact"
import DynamicFormset from "./DynamicFormset.vue"
import SocialMediaFormset from "./SocialMediaFormset.vue"

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
    position?: string
    services: string[]
    addresses: string[]
    phone_number?: string
    email?: string
    website?: string
    social_media: SocialMedia[]
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
      position: props.card.position || "",
      summary: props.card.summary || "",
      phone_number: props.card.phone_number || "",
      email: props.card.email || "",
      website: props.card.website || "",
      services: props.card.services.length ? props.card.services : [""],
      addresses: props.card.addresses.length ? props.card.addresses : [""],
      social_media: props.card.social_media.length
        ? props.card.social_media
        : [{ platform: SocialPlatform.TELEGRAM, username_or_link: "" }],
    }
  }
  return {
    first_name: "",
    last_name: "",
    middle_name: "",
    company_name: "",
    position: "",
    summary: "",
    phone_number: "",
    email: "",
    website: "",
    services: [""],
    addresses: [""],
    social_media: [{ platform: SocialPlatform.TELEGRAM, username_or_link: "" } as SocialMedia],
  }
}

const isEditing = computed(() => !!props.card)

const platformUrlPatterns: Record<string, RegExp> = {
  [SocialPlatform.TELEGRAM]: /^(https?:\/\/)?(t\.me\/|telegram\.me\/)|@\w+/i,
  [SocialPlatform.LINKEDIN]: /^(https?:\/\/)?(www\.)?linkedin\.com\/(in|company)\/\w+/i,
  [SocialPlatform.WHATSAPP]: /^(https?:\/\/)?(wa\.me\/|api\.whatsapp\.com\/send\/?)/i,
  [SocialPlatform.FACEBOOK]: /^(https?:\/\/)?(www\.)?facebook\.com\/\w+/i,
  [SocialPlatform.INSTAGRAM]: /^(https?:\/\/)?(www\.)?instagram\.com\/\w+/i,
  [SocialPlatform.VIBER]: /^\+?[\d\s]+$/,
  [SocialPlatform.X]: /^(https?:\/\/)?(www\.)?(x\.com|twitter\.com)\/\w+/i,
  [SocialPlatform.VK]: /^(https?:\/\/)?(www\.)?vk\.com\/\w+/i,
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
  position: yup
    .string()
    .test("position", "Minimum 2 characters", (v) => !v || !v.trim() || v.trim().length >= 2)
    .test("position", "Maximum 50 characters", (v) => !v || !v.trim() || v.trim().length <= 50),
  summary: yup
    .string()
    .test("summary", "Maximum 250 characters", (v) => !v || !v.trim() || v.trim().length <= 250),
  phone_number: yup
    .string()
    .test("phone", "Only digits, spaces, and + allowed", (v) => !v || !v.trim() || /^[\d\s+]+$/.test(v.trim())),
  email: yup
    .string()
    .test("email", "Invalid email format", (v) => {
      if (!v || !v.trim()) return true
      return yup.string().email().isValidSync(v.trim())
    }),
  website: yup
    .string()
    .test("website", "Invalid URL format", (v) => {
      if (!v || !v.trim()) return true
      return yup.string().url().isValidSync(v.trim())
    }),
  services: yup.array().of(
    yup
      .string()
      .test("svc", "Must be 3-100 characters if filled", (v) => !v || !v.trim() || (v.trim().length >= 3 && v.trim().length <= 100)),
  ),
  addresses: yup.array().of(
    yup
      .string()
      .test("addr", "Must be 3-100 characters if filled", (v) => !v || !v.trim() || (v.trim().length >= 3 && v.trim().length <= 100)),
  ),
  social_media: yup.array().of(
    yup.object({
      platform: yup.string().required(),
      username_or_link: yup
        .string()
        .test("platform-url", "Invalid URL or handle for the selected platform", function (value) {
          if (!value || !value.trim()) return true
          const socialItem = this.parent as { platform: string; username_or_link: string }
          const pattern = platformUrlPatterns[socialItem.platform]
          return pattern ? pattern.test(value) : true
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
const { value: position, errorMessage: positionErr } = useField<string>("position")
const { value: summary, errorMessage: summaryErr } = useField<string>("summary")
const { value: phoneNumber, errorMessage: phoneNumberErr } = useField<string>("phone_number")
const { value: email, errorMessage: emailErr } = useField<string>("email")
const { value: website, errorMessage: websiteErr } = useField<string>("website")

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
        social_media: mockData.social_media?.length
          ? mockData.social_media
          : [{ platform: SocialPlatform.TELEGRAM, username_or_link: "" }],
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
      phone_number: "+1 555 000 0000",
      email: "alex@example.com",
      website: "https://example.com",
      services: ["Web Development", "API Design"],
      addresses: ["742 Evergreen Terrace, Springfield"],
      social_media: [
        { platform: SocialPlatform.LINKEDIN, username_or_link: "https://linkedin.com/in/alexjohnson" },
      ] as SocialMedia[],
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

  const services = formValues.services.filter((s: string) => s.trim())
  const addresses = formValues.addresses.filter((a: string) => a.trim())
  const socialMedia = formValues.social_media.filter(
    (s: SocialMedia) => s.username_or_link.trim(),
  )

  const data = {
    display_name: displayName,
    image_url: imageUrl,
    first_name: formValues.first_name?.trim() || undefined,
    last_name: formValues.last_name?.trim() || undefined,
    middle_name: formValues.middle_name?.trim() || undefined,
    company_name: formValues.company_name?.trim() || undefined,
    position: formValues.position?.trim() || undefined,
    services,
    addresses,
    phone_number: formValues.phone_number?.trim() || undefined,
    email: formValues.email?.trim() || undefined,
    website: formValues.website?.trim() || undefined,
    social_media: socialMedia,
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
              placeholder="M"
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
            <label class="text-muted-foreground text-xs font-medium">Position</label>
            <Input
              v-model="position"
              placeholder="CEO"
              :class="positionErr && 'border-destructive'"
            />
            <span v-if="positionErr" class="text-destructive text-xs">{{ positionErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Summary</label>
            <textarea
              v-model="summary"
              placeholder="1-2 sentence brief description..."
              class="border-input placeholder:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 flex h-20 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-xs transition-[color,box-shadow] outline-none focus-visible:ring-[3px]"
              :class="summaryErr && 'border-destructive'"
              maxlength="250"
            />
            <span v-if="summaryErr" class="text-destructive text-xs">{{ summaryErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Phone Number</label>
            <Input
              v-model="phoneNumber"
              placeholder="+1 555 123 4567"
              :class="phoneNumberErr && 'border-destructive'"
            />
            <span v-if="phoneNumberErr" class="text-destructive text-xs">{{ phoneNumberErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Email</label>
            <Input
              v-model="email"
              placeholder="john@acme.com"
              :class="emailErr && 'border-destructive'"
            />
            <span v-if="emailErr" class="text-destructive text-xs">{{ emailErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Website</label>
            <Input
              v-model="website"
              placeholder="https://acme.com"
              :class="websiteErr && 'border-destructive'"
            />
            <span v-if="websiteErr" class="text-destructive text-xs">{{ websiteErr }}</span>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Services</label>
            <DynamicFormset
              :model-value="(values.services as string[]) || ['']"
              @update:model-value="(v: string[]) => setFieldValue('services', v)"
              placeholder="Enter a service"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Addresses</label>
            <DynamicFormset
              :model-value="(values.addresses as string[]) || ['']"
              @update:model-value="(v: string[]) => setFieldValue('addresses', v)"
              placeholder="Enter an address"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-muted-foreground text-xs font-medium">Social Media</label>
            <SocialMediaFormset
              :model-value="(values.social_media as SocialMedia[]) || [{ platform: SocialPlatform.TELEGRAM, username_or_link: '' }]"
              @update:model-value="(v: SocialMedia[]) => setFieldValue('social_media', v)"
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
