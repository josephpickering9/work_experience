<template>
  <div class="w-full max-w-5xl">
    <div class="mb-8">
      <h1>
        {{ isUpdate ? 'Update' : 'Create' }} Tag
      </h1>
      <p class="text-gray-500 dark:text-gray-400">
        {{ isUpdate ? 'Modify existing tag details' : 'Add a new tag to the collection' }}
      </p>
    </div>

    <div class="grid gap-8 lg:grid-cols-2">
      <div class="flex flex-col gap-6 rounded-2xl border border-white/10 bg-white/5 p-8 backdrop-blur-md dark:bg-gray-900/40">
        <TextInput v-model="title" label="Title" placeholder="e.g. Vue.js" :disabled="loading" />
        <TagTypeSelectList v-model="type" label="Type" :disabled="loading" />
        <IconAutoComplete v-model="icon" label="Icon" :disabled="loading" />
        <ColourPicker v-model="customColour" label="Custom Colour" :disabled="loading" />

        <div class="flex items-center justify-between space-x-3 pt-4">
           <FormButton
            v-if="isUpdate"
            label="Delete"
            type="error"
            size="md"
            icon="material-symbols:delete"
            :disabled="loading"
            variant="ghost"
            @click="remove"
          />
          <FormButton label="Save Tag" type="primary" size="md" :loading="loading" icon="heroicons:check" @click="save" />
        </div>
      </div>

      <div class="flex flex-col space-y-4">
        <h3 class="ml-1 text-sm font-medium uppercase tracking-wider text-gray-500">Live Preview</h3>
        <div class="sticky top-24">
          <TagListItem :tag="previewTag" preview />
          
          <div class="mt-8 rounded-xl bg-blue-50/50 p-6 text-sm text-blue-800 backdrop-blur-sm dark:bg-blue-900/20 dark:text-blue-200">
            <div class="mb-2 flex items-center font-bold">
              <Icon name="heroicons:information-circle" class="mr-2 h-5 w-5" />
              Pro Tip
            </div>
            Tags are used to categorize projects. Selecting the correct type ensures it appears in the right section on the Tags page.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTagStore } from '~/store/TagStore'
import { useNotificationStore } from '~/store/NotificationStore'
import { TagType, type CreateTag, type Tag } from '@api'
import TextInput from '~/components/ui/input/TextInput.vue'
import FormButton from '~/components/ui/form/FormButton.vue'
import ColourPicker from '~/components/ui/input/ColourPicker.vue'
import IconAutoComplete from '~/components/ui/input/IconAutoComplete.vue'
import TagListItem from '~/components/tag/list/TagListItem.vue'
import TagTypeSelectList from './TagTypeSelectList.vue'

interface Props {
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  id: undefined,
})

const router = useRouter()
const tagStore = useTagStore()
const notificationStore = useNotificationStore()

const title = ref('')
const type = ref<TagType>(TagType.DEFAULT)
const icon = ref<string | undefined>(undefined)
const customColour = ref<string | undefined>(undefined)

const isUpdate = computed((): boolean => {
  return props.id != null
})

const tag = computed((): Tag | undefined => {
  return tagStore.tag
})

const tagError = computed((): string | undefined => {
  return tagStore.tagError
})

const loading = computed((): boolean => {
  return tagStore.tagCreating || tagStore.tagLoading
})

const error = computed((): string | undefined => {
  return tagStore.tagCreateError
})

const createTagValue = computed((): CreateTag => {
  return {
    title: title.value,
    type: type.value,
    icon: icon.value,
    customColour: customColour.value,
  }
})

const previewTag = computed((): Tag => {
  return {
    id: 'preview',
    title: title.value || 'New Tag',
    type: type.value,
    icon: icon.value,
    customColour: customColour.value,
    slug: 'preview-slug'
  }
})

async function save() {
  let response: Tag | undefined

  if (isUpdate.value && props.id) {
    response = await tagStore.updateTag(props.id, createTagValue.value)
  } else {
    response = await tagStore.createTag(createTagValue.value)
  }

  if (!error.value && response) {
    router.push(`/tags`)
    notificationStore.displaySuccessNotification(`Tag ${isUpdate.value ? 'updated' : 'created'} successfully`)
  } else {
    notificationStore.displayErrorNotification(error.value || 'An error occurred')
  }
}

async function remove() {
  if (isUpdate.value && props.id) {
    await tagStore.deleteTag(props.id)

    if (!error.value) {
      router.push(`/tags`)
      notificationStore.displaySuccessNotification('Tag deleted successfully')
    } else {
      notificationStore.displayErrorNotification(error.value || 'An error occurred')
    }
  }
}

onMounted(async () => {
  if (isUpdate.value && props.id) {
    await tagStore.getTag(props.id)

    if (!tagError.value && tag.value) {
      title.value = tag.value.title
      type.value = tag.value.type
      icon.value = tag.value.icon ?? ''
      customColour.value = tag.value.customColour ?? ''
    } else {
      notificationStore.displayErrorNotification(tagError.value || 'An error occurred')
    }
  }
})
</script>
