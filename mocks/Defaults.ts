import type { CreateProject } from '@api/models/CreateProject'

export const defaultProjectForm: CreateProject = {
    title: '',
    shortDescription: '',
    description: '',
    companyId: undefined,
    year: new Date().getFullYear(),
    website: undefined,
    showMockup: false,
    images: [],
    tags: [],
    repositories: [],
}
