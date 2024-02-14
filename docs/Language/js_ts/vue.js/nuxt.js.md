p

# init app

```powershell
npx nuxi init <app>
```

# eslint

```powershell
yarn add -D eslint
yarn add -D @nuxtjs/eslint-module


```

2. Add `@nuxtjs/eslint-module` to the `modules` section of `nuxt.config.ts`

```ts
export default defineNuxtConfig({  modules: [    // Simple usage    '@nuxtjs/eslint-module',    // With options    ['@nuxtjs/eslint-module', { /* module options */ }]  ]})
```

# pinia

```powershell
npm i @pinia/nuxt
```

config

```ts
// Nuxt 3
export default defineNuxtConfig({ modules: ["@pinia/nuxt"] });
```

# auto-animate

```powershell
yarn add @formkit/auto-animate
```

# nuxt-vutify

```powershell
yarn add --dev "@invictus.codes/nuxt-vuetify"
```

nuxt-vutify

```powershell
yarn add @nuxt/ui


```

pnpm dev
