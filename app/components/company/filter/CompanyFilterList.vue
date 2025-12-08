<template>
  <div class="flex flex-col max-h-64 overflow-y-auto">
    <TextInput
      v-model="searchQuery"
      placeholder="Search companies..."
    />
    <button
      v-for="company in filteredCompanies"
      :key="company.id"
      type="button"
      class="btn btn-sm btn-ghost justify-start gap-2 font-normal hover:bg-base-200 h-auto py-2"
      @click="selectCompany(company.id)"
    >
      <CompanyItem :company="company" size="sm" />
    </button>
    <div v-if="filteredCompanies.length === 0" class="text-sm text-center py-4 opacity-50">
      No companies found
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Company } from '@api'
import { useCompanyStore } from '~/store/CompanyStore'
import CompanyItem from '../form/CompanyItem.vue'

const emit = defineEmits<{
  'select': [companyId: string]
}>()

const companyStore = useCompanyStore()
const searchQuery = ref('')

const companies = computed((): Company[] => {
  const sorted = [...companyStore.companies].sort((a, b) => {
    if (!a.startDate && !b.startDate) return 0
    if (!a.startDate) return -1
    if (!b.startDate) return 1
    return b.startDate!.localeCompare(a.startDate!)
  })
  return sorted
})

const filteredCompanies = computed(() => {
  if (!searchQuery.value) return companies.value
  
  const query = searchQuery.value.toLowerCase()
  return companies.value.filter(company => 
    company.name.toLowerCase().includes(query)
  )
})

function selectCompany(companyId: string) {
  emit('select', companyId)
}
</script>
