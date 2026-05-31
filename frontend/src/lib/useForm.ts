import { reactive, computed } from "vue"
import * as yup from "yup"

function isSchema(field: unknown): field is yup.Schema {
  return typeof field === "object" && field !== null && "validateSync" in field
}

function schemaType(field: unknown): string | undefined {
  return (field as Record<string, unknown> | null)?.type as string | undefined
}

export function useForm<T extends Record<string, any>>({
  validationSchema,
  initialValues,
}: {
  validationSchema: yup.ObjectSchema<T>
  initialValues: T
}) {
  const values = reactive({ ...initialValues }) as T

  const errors = computed(() => {
    const result: Record<string, string | undefined> = {}
    for (const key of Object.keys(validationSchema.fields)) {
      const field = validationSchema.fields[key]
      if (!isSchema(field) || schemaType(field) === "array") continue
      try {
        ;(field as yup.Schema<any>).validateSync((values as any)[key])
      } catch (e: unknown) {
        if (e instanceof yup.ValidationError) result[key] = e.message
      }
    }
    return result
  })

  const meta = computed(() => ({
    valid: validationSchema.isValidSync(values),
  }))

  function defineField(name: string) {
    return computed({
      get: () => (values as any)[name],
      set: (v: any) => {
        (values as any)[name] = v
      },
    })
  }

  function defineArray(name: string) {
    const field = validationSchema.fields[name]
    if (!isSchema(field) || schemaType(field) !== "array") {
      throw new Error(`${name} is not an array schema`)
    }
    const innerType = (field as yup.ArraySchema<any, any, any, any>).innerType
    if (!innerType) {
      throw new Error(`${name} has no inner type`)
    }

    const items = computed(() => {
      const v = (values as any)[name]
      return Array.isArray(v) ? v : []
    })

    const errors = computed(() =>
      items.value.map((item: any) => {
        try {
          ;(innerType as yup.Schema<any>).validateSync(item)
          return undefined
        } catch (e: unknown) {
          if (e instanceof yup.ValidationError) return e.message
          return undefined
        }
      }),
    )

    function setItems(newItems: any[]) {
      ;(values as any)[name] = newItems
    }

    return { items, errors, setItems }
  }

  function handleSubmit(cb: (values: T) => void) {
    return (e?: Event) => {
      e?.preventDefault()
      try {
        validationSchema.validateSync(values, { abortEarly: false })
        cb({ ...values })
      } catch {
        // invalid — abort submit
      }
    }
  }

  function resetForm(opts: { values: T }) {
    Object.assign(values, opts.values)
  }

  return {
    values,
    errors,
    meta,
    defineField,
    defineArray,
    handleSubmit,
    resetForm,
  }
}
