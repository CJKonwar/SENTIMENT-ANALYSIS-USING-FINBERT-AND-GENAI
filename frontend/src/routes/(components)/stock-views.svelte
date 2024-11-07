<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Skeleton } from '$lib/components/ui/skeleton';

	let { bearishView = '', bullishView = '' }: { bearishView: string; bullishView: string } =
		$props();
</script>

<div class="mx-2 my-8 flex flex-col">
	<!-- <h1 class="p-4 text-3xl">Stock Views</h1> -->
	<div class="mx-2 flex flex-col sm:flex-row gap-6">
		<Card.Root class="w-full sm:w-1/2 border-green-500">
			<Card.Header>
				<Card.Title class="text-xl text-green-500">Bullish Views</Card.Title>
			</Card.Header>
			<Card.Content>
				{#if bullishView.length > 0}
					{#each bullishView.split('\n') as line}
						{#if line.trim().startsWith('*')}
							<p class="mb-2 ml-4">• {line.trim().slice(1).trim()}</p>
						{:else if line.trim().startsWith('+')}
							<p class="mb-2 ml-8">- {line.trim().slice(1).trim()}</p>
						{/if}
					{/each}
				{:else}
					<Skeleton class="h-32 w-full" />
				{/if}
			</Card.Content>
		</Card.Root>
		<Card.Root class="w-full sm:w-1/2 border-red-500">
			<Card.Header>
				<Card.Title class="text-xl text-red-500">Bearish Views</Card.Title>
			</Card.Header>
			<Card.Content>
				{#if bearishView.length > 0}
					{#each bearishView.split('\n') as line}
						{#if line.trim().startsWith('*')}
							<p class="mb-2 ml-4">• {line.trim().slice(1).trim()}</p>
						{:else if line.trim().startsWith('+')}
							<p class="mb-2 ml-8">- {line.trim().slice(1).trim()}</p>
						{/if}
					{/each}
				{:else}
					<Skeleton class="h-32 w-full" />
				{/if}
			</Card.Content>
		</Card.Root>
	</div>
</div>
