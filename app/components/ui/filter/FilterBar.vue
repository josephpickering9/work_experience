<template>
  <div class="flex flex-wrap items-center gap-2">
    <FilterChip
      v-for="(filter, index) in filters"
      :key="`${filter.type}-${index}`"
      :filter="filter"
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
          <TextInput
            v-model="searchValue"
            placeholder="Search projects..."
          />
          <button
            v-for="filterType in filterTypes.filter(ft => ft.value !== 'search')"
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

          <CompanyAutoComplete
            v-if="selectedFilterType === 'company'"
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
import type { Filter } from '~/types/Filter'
import { FilterType } from '~/types/FilterType'

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
const searchValue = ref<string>('')
const searchTimeout = ref<NodeJS.Timeout | null>(null)
const container = ref<HTMLElement | null>(null)

const filterTypes = [
  { value: FilterType.SEARCH, label: 'Search', icon: 'heroicons:magnifying-glass' },
  { value: FilterType.COMPANY, label: 'Company', icon: 'heroicons:building-office' },
  { value: FilterType.TAG_TYPE, label: 'Tag Type', icon: 'heroicons:tag' },
  { value: FilterType.TAG, label: 'Tag', icon: 'heroicons:tag' },
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
  filterValue.value = type === FilterType.TAG ? [] : ''
}

function resetFilterType() {
  selectedFilterType.value = null
  filterValue.value = ''
}

function applyFilter() {
  if (!selectedFilterType.value) return
  
  if (selectedFilterType.value === FilterType.TAG) {
    const tags = Array.isArray(filterValue.value) ? filterValue.value : []
    if (tags.length === 0) return
    
    const filterType = filterTypes.find(ft => ft.value === selectedFilterType.value)
    if (!filterType) return

    const newFilter: Filter = {
      type: FilterType.TAG,
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
  if (selectedFilterType.value === FilterType.COMPANY) {
    const company = companies.value.find(c => c.id === filterValue.value)
    displayValue = company?.name
  }

  const newFilter: Filter = {
    type: selectedFilterType.value as FilterType,
    value: filterValue.value,
    label: filterType.label,
    displayValue,
  }

  emit('update:filters', [...props.filters, newFilter])
  
  // Close dropdown except for search
  if (selectedFilterType.value !== FilterType.SEARCH) {
    close()
  }
}

function removeFilter(index: number) {
  const updatedFilters = [...props.filters]
  const removedFilter = updatedFilters.splice(index, 1)[0]
  
  if (removedFilter?.type === FilterType.SEARCH) searchValue.value = ''
  
  emit('update:filters', updatedFilters)
}

function applySearchFilter() {
  if (!searchValue.value.trim()) {
    const searchFilterIndex = props.filters.findIndex(f => f.type === FilterType.SEARCH)
    if (searchFilterIndex !== -1) removeFilter(searchFilterIndex)
    return
  }

  const updatedFilters = [...props.filters]
  const searchFilterIndex = updatedFilters.findIndex(f => f.type === FilterType.SEARCH)
  
  const searchFilter: Filter = {
    type: FilterType.SEARCH,
    value: searchValue.value.trim(),
    label: 'Search',
  }

  if (searchFilterIndex !== -1) updatedFilters[searchFilterIndex] = searchFilter
  else updatedFilters.push(searchFilter)

  emit('update:filters', updatedFilters)
}

function handleClickOutside(event: MouseEvent) {
  if (container.value && !container.value.contains(event.target as Node)) {
    close()
  }
}

watch(() => props.filters, (newFilters) => {
  const searchFilter = newFilters.find(f => f.type === FilterType.SEARCH)
  if (searchFilter && searchFilter.value !== searchValue.value) {
    searchValue.value = searchFilter.value
  } else if (!searchFilter && searchValue.value) {
    searchValue.value = ''
  }
}, { deep: true, immediate: true })

watch(() => searchValue.value, () => {
  applySearchFilter()
})

watch(filterValue, (newValue, oldValue) => {
  if (selectedFilterType.value && selectedFilterType.value !== FilterType.SEARCH) {
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

