import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCompany, getCompanyById, getCompanyBySlug, postCompany, putCompanyById, deleteCompanyById } from '@api'
import { asyncForm, tryCatchFinally } from '~/utils/async-helper'
import type { Company, CreateCompany } from '@api'


export const useCompanyStore = defineStore('companyStore', {
  state: () => ({
    companiesForm: asyncForm<Company[]>(),
    companyForm: asyncForm<Company>(),
    companyCreateForm: asyncForm<Company>(),
  }),
  getters: {
    companies: (state) => state.companiesForm.data ?? [],
    companiesLoading: (state) => state.companiesForm.loading,
    companiesError: (state) => state.companiesForm.error,
    company: (state) => state.companyForm.data,
    companyLoading: (state) => state.companyForm.loading,
    companyError: (state) => state.companyForm.error,
    companyCreating: (state) => state.companyCreateForm.loading,
    companyCreateError: (state) => state.companyCreateForm.error,
  },
  actions: {
    async getCompanies(search?: string): Promise<void> {
      if (this.companiesForm.loading) return

      await tryCatchFinally(ref(this.companiesForm), () => getCompany({ query: { search } }))
    },
    async getCompany(id: string): Promise<void> {
      if (!id || this.companyForm.loading) return

      await tryCatchFinally(ref(this.companyForm), () => getCompanyById({ path: { id } }))
    },
    async getCompanyBySlug(slug: string): Promise<void> {
      if (!slug || this.companyForm.loading) return

      await tryCatchFinally(ref(this.companyForm), () => getCompanyBySlug({ path: { slug } }))
    },
    async createCompany(company: CreateCompany): Promise<Company | undefined> {
      if (!company || this.companyCreateForm.loading) return

      return await tryCatchFinally(ref(this.companyCreateForm), () => postCompany({ body: { createCompany: company } }))
    },
    async updateCompany(id: string, company: CreateCompany): Promise<Company | undefined> {
      if (!company || this.companyCreateForm.loading) return

      return await tryCatchFinally(ref(this.companyCreateForm), () => putCompanyById({ path: { id }, body: { createCompany: company } }))
    },
    async deleteCompany(id: string): Promise<void> {
      if (!id || this.companyCreateForm.loading) return

      await tryCatchFinally(ref(this.companyCreateForm), () => deleteCompanyById({ path: { id } }))
    },
  },
})
