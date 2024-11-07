<script lang="ts">
	export let data: string;

	const re = new RegExp(/^\d+\./);
</script>

<div class="mx-2 my-4 flex flex-col">
	<h1 class="p-4 text-3xl">Fundamental Summary</h1>
	<div class="flex flex-col px-4 pb-6">
		{#each data.split('\n') as line}
			{#if line.trim() !== 'Summary:' && line.trim() !== 'Fundamental Summary:'}
				{#if re.test(line)}
					<h2 class="my-1 ml-4">{line.trim()}</h2>
				{:else if line.trim().startsWith('*')}
					<p class="mb-2 ml-4">• {line.trim().slice(1).trim()}</p>
				{:else if line.trim().startsWith('+')}
					<p class="mb-2 ml-8">- {line.trim().slice(1).trim()}</p>
				{:else if line.trim() !== ''}
					<p class="mb-2 mt-4">{line.trim()}</p>
				{/if}
			{/if}
		{/each}
	</div>
</div>
