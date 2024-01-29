<script setup lang="ts">
const router = useRouter()

const nav = [
  { label: 'Intro', to: '/' },
  { label: 'HW', to: '/HW' },
  { label: 'Test', to: '/Test' },
]
</script>

<template>
	<NuxtTab dir="routing/pages" :nav="nav" current-route>
		<NuxtLoadingIndicator />
		<v-app>
			<NuxtPage />
		</v-app>
	</NuxtTab>
</template>
