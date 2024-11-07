<script lang="ts">
	import { Badge } from '$lib/components/ui/badge';
	import type { BasicInfo } from '../types';

	export let basicInfo: BasicInfo[];
</script>

<div class="mx-2 my-4 flex flex-col">
	<h1 class="p-4 text-3xl">Basic Stock Information</h1>
	<div class="grid grid-cols-1 gap-2 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
		{#each basicInfo as info}
			<div class="flex flex-col sm:flex-row sm:items-center px-4 py-2">
				<Badge variant="secondary" class="rounded-lg text-sm">{info.Metric}</Badge>
				<span class="pl-4">{info.Value}</span>
			</div>
		{/each}
	</div>
</div>


