<script lang="ts">
	import { Badge } from '$lib/components/ui/badge';
	import type { News } from '../types';

	let { url = '#', urlToImg, title, confidence, sentiment, publishedAt }: News = $props();

	function calcScore(number: number, precision: number) {
		const factor = 10 ** precision;
		return ((Math.round(number * factor) / factor) * 10).toFixed(1);
	}

	function Opacity(num: number) {
		const n = 0.35 + num * 0.35;
		const factor = 100;
		return Math.round(n * factor) / factor;
	}

	function Color(sentiment: string) {
		switch (sentiment.toLowerCase()) {
			case 'negative':
				return '222, 0, 32';
			case 'positive':
				return '76, 174, 79';
			default:
				return '64, 64, 64';
		}
	}

	function formatTimestamp(timestamp: string) {
		return (
			new Date(timestamp).toLocaleString('en-US', {
				year: 'numeric',
				month: 'long',
				day: 'numeric',
				hour: '2-digit',
				minute: '2-digit',
				hour12: false,
				timeZone: 'UTC'
			}) + ' UTC'
		);
	}

	let opacity = $derived(Opacity(confidence));
	let color = $derived(Color(sentiment));
	let score = $derived(calcScore(confidence, 2));
	let timestamp = $derived(formatTimestamp(publishedAt));
</script>

<a href={url} target="_blank">
	<div
		class="flex w-full flex-col gap-3 rounded-xl border-2 p-2 hover:bg-gray-600"
		style="background-color: rgba({color}, {opacity}); border-color: rgb({color});"
	>
		<div class="flex w-full gap-2">
			<div class="flex w-3/4">
				<h1 class="w-full overflow-clip text-ellipsis text-xl">{title}</h1>
			</div>
			<div class="grid h-full w-1/4 place-content-center">
				<img
					class="h-full w-full rounded-lg object-cover"
					src={urlToImg ?? 'https://placehold.co/300x200/png'}
					alt={title.slice(0, 20)}
				/>
			</div>
		</div>
		<div class="flex justify-between">
			<Badge variant="outline">Confidence Score: {score}</Badge>
			<Badge variant="default">{timestamp}</Badge>
		</div>
	</div>
</a>
