export interface Filter {
    type: 'search' | 'company' | 'tagType' | 'tag'
    value: string
    label: string
    displayValue?: string
}