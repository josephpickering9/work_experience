module.exports = {
  extends: [
    '@nuxtjs/eslint-config-typescript',
    'plugin:prettier/recommended',
    'prettier',
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:vue/vue3-essential',
  ],
  plugins: ['prettier', 'unused-imports', '@typescript-eslint', 'vue'],
  root: true,
  rules: {
    'prettier/prettier': ['error', require('./.prettierrc.json')],
    '@typescript-eslint/no-var-requires': 0,
    'no-this-alias': 0,
    'vue/no-v-html': 0,
    'import/named': 0,
    'vue/multi-word-component-names': 0,
    'import/no-named-as-default': 0,
    '@typescript-eslint/ban-ts-comment': 0,
    '@typescript-eslint/no-explicit-any': 0,
    'vue/component-name-in-template-casing': [
      'error',
      'PascalCase',
      {
        registeredComponentsOnly: false,
        ignores: [],
      },
    ],
    'vue/order-in-components': [
      'error',
      {
        order: [
          'el',
          'name',
          'key',
          'parent',
          'functional',
          ['delimiters', 'comments'],
          ['components', 'directives', 'filters'],
          'extends',
          'mixins',
          ['provide', 'inject'],
          'ROUTER_GUARDS',
          'layout',
          'middleware',
          'validate',
          'scrollToTop',
          'transition',
          'loading',
          'inheritAttrs',
          'model',
          ['props', 'propsData'],
          'emits',
          'setup',
          'asyncData',
          'data',
          'fetch',
          'head',
          'computed',
          'validations',
          'LIFECYCLE_HOOKS',
          'methods',
          'watch',
          'watchQuery',
          ['template', 'render'],
          'renderError',
        ],
      },
    ],
    '@typescript-eslint/no-unused-vars': 'off',
    'vue/no-unused-vars': ['error'],
    'unused-imports/no-unused-imports': 'error',
    'unused-imports/no-unused-vars': [
      'warn',
      { vars: 'all', varsIgnorePattern: '^', args: 'after-used', argsIgnorePattern: '^' },
    ],
    'no-console': ['error'],
    'no-alert': ['error'],
    'vue/match-component-file-name': [
      'error',
      {
        extensions: ['vue'],
        shouldMatchCase: false,
      },
    ],
    'vue/padding-line-between-blocks': ['error', 'always'],
    'no-restricted-imports': [
      'error',
      {
        patterns: [
          {
            group: ['~'],
            message: 'Please use an explicit path in Storybook imports. 😡',
          },
        ],
      },
    ],
  },
}
