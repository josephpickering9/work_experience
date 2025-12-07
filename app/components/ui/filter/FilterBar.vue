<template>
  <div class="flex flex-wrap items-center gap-2">
    <FilterChip
      v-for="(filter, index) in filters"
      :key="`${filter.type}-${index}`"
      :type="filter.type"
      :label="filter.label"
      :value="filter.value"
      :display-value="filter.displayValue"
      @remove="removeFilter(index)"
    />

    <div ref="container" class="dropdown" :class="{ 'dropdown-open': isOpen }">
      <button
        type="button"
        class="btn btn-sm gap-2"
        :class="filters.length > 0 ? 'btn-ghost' : 'btn-outline'"
        @click="toggle"
      >
        <Icon name="heroicons:funnel" size="1.2em" />
        <span>{{ filters.length > 0 ? 'Add Filter' : 'Filter' }}</span>
      </button>

      <div v-if="isOpen" class="dropdown-content z-[1] mt-2 w-80 rounded-box bg-base-100 p-4 shadow-xl ring-1 ring-base-content/10" @click.stop>
        <div v-if="!selectedFilterType" class="flex flex-col gap-2">
          <h3 class="text-sm font-bold opacity-70 mb-2">Select Filter Type</h3>
          <button
            v-for="filterType in filterTypes"
            :key="filterType.value"
            type="button"
            class="btn btn-sm btn-ghost justify-start gap-2"
            @click="selectFilterType(filterType.value)"
          >
            <Icon :name="filterType.icon" size="1.2em" />
            <span>{{ filterType.label }}</span>
          </button>
        </div>
        <div v-else class="flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold opacity-70">{{ selectedFilterTypeLabel }}</h3>
            <button type="button" class="btn btn-circle btn-ghost btn-xs" @click="resetFilterType">
              <Icon name="heroicons:x-mark" />
            </button>
          </div>

          <TextInput
            v-if="selectedFilterType === 'search'"
            v-model="filterValue"
            placeholder="Search projects..."
            @keyup.enter="applyFilter"
          />

          <CompanyAutoComplete
            v-else-if="selectedFilterType === 'company'"
            v-model="filterValue"
            placeholder="Select company..."
          />

          <TagTypeSelectList
            v-else-if="selectedFilterType === 'tagType'"
            v-model="filterValue"
            placeholder="Select tag type..."
          />

          <TagAutoComplete
            v-else-if="selectedFilterType === 'tag'"
            v-model="tagFilterValue"
            placeholder="Select tag..."
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { Icon } from '#components'
import { useCompanyStore } from '~/store/CompanyStore'
import FilterChip from './FilterChip.vue'
import TextInput from '~/components/ui/input/TextInput.vue'
import CompanyAutoComplete from '~/components/company/form/CompanyAutoComplete.vue'
import TagTypeSelectList from '~/components/tag/form/TagTypeSelectList.vue'
import TagAutoComplete from '~/components/tag/form/TagAutoComplete.vue'
import { concat } from 'lodash-es'
import type { Filter } from '~/types/Filter'

interface Props {
  filters: Filter[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:filters': [filters: Filter[]]
}>()

const companyStore = useCompanyStore()

const isOpen = ref(false)
const selectedFilterType = ref<string | null>(null)
const filterValue = ref<string | string[]>('')
const container = ref<HTMLElement | null>(null)

const filterTypes = [
  { value: 'search', label: 'Search', icon: 'heroicons:magnifying-glass' },
  { value: 'company', label: 'Company', icon: 'heroicons:building-office' },
  { value: 'tagType', label: 'Tag Type', icon: 'heroicons:tag' },
  { value: 'tag', label: 'Tag', icon: 'heroicons:tag' },
]

const companies = computed(() => companyStore.companies)

const selectedFilterTypeLabel = computed(() => {
  return filterTypes.find(ft => ft.value === selectedFilterType.value)?.label || ''
})

const tagFilterValue = computed({
  get: () => {
    if (selectedFilterType.value === 'tag') {
      return Array.isArray(filterValue.value) ? filterValue.value : []
    }
    return []
  },
  set: (val: string[]) => {
    filterValue.value = val
  }
})

function toggle() {
  isOpen.value = !isOpen.value
  if (!isOpen.value) {
    resetFilterType()
  }
}

function close() {
  isOpen.value = false
  resetFilterType()
}

function selectFilterType(type: string) {
  selectedFilterType.value = type
  filterValue.value = type === 'tag' ? [] : ''
}

function resetFilterType() {
  selectedFilterType.value = null
  filterValue.value = ''
}

function applyFilter() {
  if (!selectedFilterType.value) return
  
  if (selectedFilterType.value === 'tag') {
    const tags = Array.isArray(filterValue.value) ? filterValue.value : []
    if (tags.length === 0) return
    
    const filterType = filterTypes.find(ft => ft.value === selectedFilterType.value)
    if (!filterType) return

    const newFilter: Filter = {
      type: 'tag',
      value: tags[0] || '',
      label: filterType.label,
      displayValue: tags[0],
    }

    emit('update:filters', [...props.filters, newFilter])
    close()
    return
  }

  if (!filterValue.value || Array.isArray(filterValue.value)) return

  const filterType = filterTypes.find(ft => ft.value === selectedFilterType.value)
  if (!filterType) return

  let displayValue: string | undefined
  if (selectedFilterType.value === 'company') {
    const company = companies.value.find(c => c.id === filterValue.value)
    displayValue = company?.name
  }

  const newFilter: Filter = {
    type: selectedFilterType.value as Filter['type'],
    value: filterValue.value,
    label: filterType.label,
    displayValue: displayValue || '',
  }

  emit('update:filters', concat(props.filters, newFilter))
  
  if (selectedFilterType.value !== 'search') {
    close()
  }
}

function removeFilter(index: number) {
  const updatedFilters = [...props.filters]
  updatedFilters.splice(index, 1)
  emit('update:filters', updatedFilters)
}

function handleClickOutside(event: MouseEvent) {
  if (container.value && !container.value.contains(event.target as Node)) {
    close()
  }
}

watch(filterValue, (newValue, oldValue) => {
  if (selectedFilterType.value && selectedFilterType.value !== 'search') {
    if (newValue && newValue !== oldValue) {
      applyFilter()
    }
  }
})

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

