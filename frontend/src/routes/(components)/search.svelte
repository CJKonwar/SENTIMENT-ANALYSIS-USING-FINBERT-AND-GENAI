<script lang="ts">
	import { tick, onMount, createEventDispatcher } from 'svelte';
	import * as Popover from '$lib/components/ui/popover/index.js';
	import * as Command from '$lib/components/ui/command/index.js';
	import { Button } from '$lib/components/ui/button/index.js';

	import type { Company } from '../types';

	let { selectedCompany }: { selectedCompany: Company } = $props();

	let loading = $state(true);
	let companies = $state<Company[]>([]);

	onMount(async () => {
		try {
			const response = await fetch('http://localhost:5000/api/companies');
			if (!response.ok) throw new Error(`Error: ${response.status}`);
			companies = await response.json();
			loading = false;
		} catch (error) {
			console.error('Failed to fetch companies:', error);
		}
	});

	let open = $state(false);

	const dispatch = createEventDispatcher();

	function select(symbol: string) {
		const selected = companies.find((s) => s.stock_symbol === symbol) ?? {
			company_name: '',
			stock_symbol: ''
		};
		dispatch('updateCompany', selected);
	}

	// We want to refocus the trigger button when the user selects
	// an item from the list so users can continue navigating the
	// rest of the form with the keyboard.
	function closeAndFocusTrigger(triggerId: string) {
		open = false;
		tick().then(() => {
			document.getElementById(triggerId)?.focus();
		});
	}
</script>

<div class="flex flex-col sm:flex-row items-center space-y-4 sm:space-x-6 sm:space-y-0">
	<p class="text-2xl">Company:</p>
	<Popover.Root bind:open let:ids>
		<Popover.Trigger asChild let:builder>
			<Button
				builders={[builder]}
				variant="outline"
				size="sm"
				class="h-12 sm:w-[500px] w-full justify-start overflow-clip text-ellipsis px-4 text-xl text-muted-foreground"
			>
				{#if selectedCompany.company_name !== '' }
					<div class="flex w-full justify-between">
						<span class="max-w-fit text-ellipsis">
							{selectedCompany.company_name}
						</span>
						<span class="text-md min-w-fit text-muted-foreground text-opacity-60">
							{selectedCompany.stock_symbol}
						</span>
					</div>
				{:else}
					Select Company
				{/if}
			</Button>
		</Popover.Trigger>
		<Popover.Content class="w-[350px] sm:w-[350px] border-gray-600 p-0 text-2xl" side="bottom" align="start">
			<Command.Root>
				<Command.Input placeholder="Search..." />
				<Command.List>
					<Command.Empty class="text-xl">
						{#if loading}
							Loading...
						{:else}
							No results found.
						{/if}
					</Command.Empty>
					<Command.Group>
						{#each companies as company}
							<Command.Item
								bind:value={company.stock_symbol}
								onSelect={(currentValue: string) => {
									select(currentValue);
									closeAndFocusTrigger(ids.trigger);
								}}
							>
								<div class="flex w-full justify-between">
									<span>
										{company.company_name}
									</span>
									<span class="text-muted-foreground">
										{company.stock_symbol}
									</span>
								</div>
							</Command.Item>
						{/each}
					</Command.Group>
				</Command.List>
			</Command.Root>
		</Popover.Content>
	</Popover.Root>
</div>

