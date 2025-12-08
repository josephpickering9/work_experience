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

      <div v-if="isOpen" class="dropdown-content z-[1] mt-2 w-56 rounded-box bg-base-100 p-2 shadow-xl ring-1 ring-base-content/10" @click.stop>
        <div class="flex flex-col gap-1">
          <div class="px-2 py-1">
            <TextInput
              v-model="searchValue"
              placeholder="Search projects..."
              size="sm"
            />
          </div>

          <div class="divider my-0" />

          <div
            v-for="filterType in filterTypes.filter(ft => ft.value !== FilterType.SEARCH)"
            :key="filterType.value"
            class="relative"
            @mouseenter="handleFilterTypeHover(filterType.value, $event)"
            @mouseleave="handleFilterTypeLeave"
          >
            <button
              type="button"
              class="btn btn-sm btn-ghost w-full justify-start gap-2 font-normal"
            >
              <Icon :name="filterType.icon" size="1.2em" />
              <span class="flex-1 text-left">{{ filterType.label }}</span>
              <Icon name="heroicons:chevron-right" size="1em" class="opacity-50" />
            </button>

            <div
              v-if="hoveredFilterType === filterType.value"
              ref="submenuContainer"
              class="absolute top-0 w-64 rounded-box bg-base-100 p-3 shadow-xl ring-1 ring-base-content/10 z-10"
              :class="submenuPosition === 'left' ? 'right-full mr-1' : 'left-full ml-1'"
              @mouseenter="handleSubmenuEnter(filterType.value)"
              @mouseleave="handleSubmenuLeave"
            >
              <CompanyFilterList
                v-if="filterType.value === FilterType.COMPANY"
                @select="handleCompanySelect"
              />

              <TagTypeFilterList
                v-else-if="filterType.value === FilterType.TAG_TYPE"
                @select="handleTagTypeSelect"
              />

              <TagFilterList
                v-else-if="filterType.value === FilterType.TAG"
                @select="handleTagSelect"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { Icon } from '#components'
import { useCompanyStore } from '~/store/CompanyStore'
import { useTagStore } from '~/store/TagStore'
import FilterChip from './FilterChip.vue'
import TextInput from '~/components/ui/input/TextInput.vue'
import CompanyFilterList from '~/components/company/filter/CompanyFilterList.vue'
import TagTypeFilterList from '~/components/tag/filter/TagTypeFilterList.vue'
import TagFilterList from '~/components/tag/filter/TagFilterList.vue'
import type { Filter } from '~/types/Filter'
import { FilterType } from '~/types/FilterType'
import type { TagType } from '@api'

interface Props {
  filters: Filter[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:filters': [filters: Filter[]]
}>()

const companyStore = useCompanyStore()
const tagStore = useTagStore()

const isOpen = ref(false)
const searchValue = ref<string>('')
const hoveredFilterType = ref<string | null>(null)
const submenuPosition = ref<'left' | 'right'>('right')
const container = ref<HTMLElement | null>(null)
const hideTimeout = ref<NodeJS.Timeout | null>(null)

const filterTypes = [
  { value: FilterType.SEARCH, label: 'Search', icon: 'heroicons:magnifying-glass' },
  { value: FilterType.COMPANY, label: 'Company', icon: 'heroicons:building-office' },
  { value: FilterType.TAG_TYPE, label: 'Tag Type', icon: 'heroicons:tag' },
  { value: FilterType.TAG, label: 'Tag', icon: 'heroicons:tag' },
]

const companies = computed(() => companyStore.companies)

function toggle() {
  isOpen.value = !isOpen.value
  if (!isOpen.value) {
    hoveredFilterType.value = null
  }
}

function close() {
  isOpen.value = false
  hoveredFilterType.value = null
}

function handleSubmenuLeave() {
  // Delay hiding to allow user to move mouse from button to submenu
  hideTimeout.value = setTimeout(() => {
    hoveredFilterType.value = null
  }, 150)
}

function handleFilterTypeLeave() {
  // Delay hiding to allow user to move mouse to submenu
  hideTimeout.value = setTimeout(() => {
    hoveredFilterType.value = null
  }, 150)
}

function handleSubmenuEnter(filterTypeValue: string) {
  // Clear any pending hide timeout when entering submenu
  if (hideTimeout.value) {
    clearTimeout(hideTimeout.value)
    hideTimeout.value = null
  }
  // Ensure the submenu stays visible
  hoveredFilterType.value = filterTypeValue
}

function handleFilterTypeHover(filterTypeValue: string, event: MouseEvent) {
  // Clear any pending hide timeout when hovering
  if (hideTimeout.value) {
    clearTimeout(hideTimeout.value)
    hideTimeout.value = null
  }
  
  hoveredFilterType.value = filterTypeValue
  
  // Calculate if submenu would overflow on the right
  const target = event.currentTarget as HTMLElement
  if (target) {
    const rect = target.getBoundingClientRect()
    const submenuWidth = 350
    const buffer = 16
    const viewportWidth = window.innerWidth
    
    // Check if there's enough space on the right
    const spaceOnRight = viewportWidth - rect.right
    const wouldOverflow = spaceOnRight < (submenuWidth + buffer)
    
    submenuPosition.value = wouldOverflow ? 'left' : 'right'
  }
}

function handleCompanySelect(companyId: string) {
  const company = companies.value.find(c => c.id === companyId)
  if (!company) return

  const newFilter: Filter = {
    type: FilterType.COMPANY,
    value: companyId,
    label: 'Company',
    displayValue: company.name,
    logo: company.logo,
  }

  emit('update:filters', [...props.filters, newFilter])
  close()
}

function handleTagTypeSelect(tagType: TagType) {
  const newFilter: Filter = {
    type: FilterType.TAG_TYPE,
    value: tagType,
    label: 'Tag Type',
    displayValue: tagType,
  }

  emit('update:filters', [...props.filters, newFilter])
  close()
}

function handleTagSelect(tagTitle: string) {
  const tag = tagStore.tags.find(t => t.title === tagTitle)
  
  const newFilter: Filter = {
    type: FilterType.TAG,
    value: tagTitle,
    label: 'Tag',
    displayValue: tagTitle,
    icon: tag?.icon ?? undefined,
  }

  emit('update:filters', [...props.filters, newFilter])
  close()
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

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>


