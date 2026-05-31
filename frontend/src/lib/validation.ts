import * as yup from "yup"
import type { ContactMethod } from "@/types/contact"

const DIGITAL_PATTERNS: Record<string, RegExp> = {
  phone: /^[\d\s+()-]+$/,
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  website: /^https?:\/\/.+/,
  whatsapp:
    /^(https?:\/\/)?(wa\.me|whatsapp\.com)\/\w+\/?$|^[\d\s+()-]+$/,
  viber: /^(https?:\/\/)?(viber\.me)\/[\w.-]+\/?$|^[\d\s+()-]+$/,
  telegram:
    /^(https?:\/\/)?(t\.me|telegram\.me)\/\w+\/?$|^@?\w{3,32}$/,
  linkedin:
    /^(https?:\/\/)?(www\.)?linkedin\.com\/in\/[\w-]+\/?$|^@?[\w-]{3,100}$/,
  facebook:
    /^(https?:\/\/)?(www\.)?(facebook\.com|fb\.com)\/[\w.]+\/?$|^@?[\w.]{3,}$/,
  instagram:
    /^(https?:\/\/)?(www\.)?instagram\.com\/[\w.]+\/?$|^@?[\w.]{3,}$/,
  x: /^(https?:\/\/)?(www\.)?x\.com\/\w+\/?$|^@?\w+$/,
  vk: /^(https?:\/\/)?(vk\.com|vk\.ru)\/[\w.-]+\/?$|^@?[\w.-]+$/,
}

function digitalContactErrorMessage(type: string): string {
  if (type === "phone")
    return "Phone number contains invalid characters. Only digits, spaces, +, -, and () allowed."
  if (type === "email") return "Email address format is invalid."
  const label = type.charAt(0).toUpperCase() + type.slice(1)
  return `${label} must be a valid URL or matching profile handle.`
}

function textField(label: string, min: number, max: number) {
  return yup
    .string()
    .test(
      `${label}-min`,
      `${label} must be at least ${min} characters.`,
      (v) => !v || !v.trim() || v.trim().length >= min,
    )
    .test(
      `${label}-max`,
      `${label} must be at most ${max} characters.`,
      (v) => !v || !v.trim() || v.trim().length <= max,
    )
}

function arrayItemField(label: string, min: number) {
  return yup
    .string()
    .test(
      `${label}-item-min`,
      `${label} item must be at least ${min} characters if filled.`,
      (v) => !v || !v.trim() || v.trim().length >= min,
    )
}

const positionItemSchema = arrayItemField("Position", 3)
const serviceItemSchema = arrayItemField("Service", 3)
const addressItemSchema = arrayItemField("Address", 3)

const digitalContactItemSchema = yup.object({
  type: yup.string().required(),
  value: yup
    .string()
    .test("dc-value", "Invalid value for the selected contact type.", function (v) {
      if (!v || !v.trim()) return true
      const type = (this.parent as { type: string }).type
      const pattern = DIGITAL_PATTERNS[type]
      if (!pattern) return true
      if (pattern.test(v.trim())) return true
      return this.createError({ message: digitalContactErrorMessage(type) })
    }),
})

export const formSchema = yup.object({
  first_name: textField("First Name", 2, 50),
  last_name: textField("Last Name", 2, 50),
  middle_name: textField("Middle Name", 2, 50),
  company_name: textField("Company Name", 2, 50),
  summary: textField("Summary", 10, 250),
  positions: yup.array().of(positionItemSchema),
  services: yup.array().of(serviceItemSchema),
  addresses: yup.array().of(addressItemSchema),
  digital_contacts: yup.array().of(digitalContactItemSchema),
})

export type FormValues = yup.InferType<typeof formSchema>

function validateSync<T>(schema: yup.Schema<T>, value: T): string | undefined {
  try {
    schema.validateSync(value)
    return undefined
  } catch (err: unknown) {
    if (err instanceof yup.ValidationError) return err.message
    return undefined
  }
}

export function getPositionErrors(values: string[]): (string | undefined)[] {
  return values.map((v) => validateSync(positionItemSchema, v))
}

export function getServiceErrors(values: string[]): (string | undefined)[] {
  return values.map((v) => validateSync(serviceItemSchema, v))
}

export function getAddressErrors(values: string[]): (string | undefined)[] {
  return values.map((v) => validateSync(addressItemSchema, v))
}

export function getDigitalContactErrors(
  values: ContactMethod[],
): (string | undefined)[] {
  return values.map((v) => validateSync(digitalContactItemSchema, v))
}
