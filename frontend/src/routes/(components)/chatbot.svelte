<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';

	import Send from 'lucide-svelte/icons/send';
	import Bot from 'lucide-svelte/icons/bot';

	import type { Chat } from '../types';

	let chats: Chat[] = [
		{
			type: 'response',
			message: 'Hello! How can I help you today?'
		}
	];

	let query: string = '';

	const handleSubmit = async () => {
		chats = [...chats, { type: 'query', message: query }];

		const userQuery = query;
		query = '';

		try {
			const response = await fetch('http://localhost:5000/api/chatbot', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ query: userQuery })
			});

			if (!response.ok) {
				throw new Error(`Server error: ${response.statusText}`);
			}

			const data = await response.json();
			chats = [...chats, { type: 'response', message: data.reply }];
		} catch (error) {
			console.error('Failed to fetch response:', error);
		}
	};
</script>

<div class="flex flex-col">
	<div class="align-items flex gap-2 p-2 text-2xl">
		<Bot class="h-full" />
		<span>ChatBot</span>
	</div>
	<div class="flex h-[400px] flex-col gap-2 overflow-y-scroll p-4">
		{#each chats as chat}
			<div class={`flex w-full ${chat.type}`}>
				<div
					class={`w-fit rounded-md px-2 py-1 ${chat.type === 'query' ? 'bg-black' : 'bg-gray-600'}`}
				>
					{chat.message}
				</div>
			</div>
		{/each}
	</div>
	<Separator />
	<form
		on:submit|preventDefault={handleSubmit}
		class="mt-1 flex w-full items-center justify-around gap-1 space-x-2 p-1"
	>
		<Input
			bind:value={query}
			type="text"
			placeholder="Type your question here..."
			class="h-full w-full rounded-lg text-lg font-light"
		/>
		<Button type="submit" class="aspect-square rounded-full p-2">
			<Send class="aspect-square w-full" />
		</Button>
		<Button class="aspect-square rounded-full p-2">
			<a href="http://localhost:8000/chatbot" target="_blank">LaravelChatbot</a>

		</Button>
	</form>
</div>

<style>
	.query {
		justify-content: flex-end;
	}
	.response {
		justify-content: flex-start;
	}
</style>
