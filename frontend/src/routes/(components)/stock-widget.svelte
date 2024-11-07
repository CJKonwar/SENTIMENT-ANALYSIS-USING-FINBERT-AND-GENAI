<script lang="ts">
	import { Skeleton } from '$lib/components/ui/skeleton';

	let { symbol = '' } = $props();

	$effect(() => {
		if (symbol === '') return;
		const container = document.querySelector('.tradingview-widget-container2');

		while (container?.firstChild) {
			container.removeChild(container.firstChild);
		}

		const script = document.createElement('script');
		script.type = 'text/javascript';
		script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js';
		script.async = true;
		script.innerHTML = JSON.stringify({
			autosize: true,
			symbol: `NASDAQ:${symbol.toUpperCase()}`,
			width: '100%',
			locale: 'en',
			colorTheme: 'dark',
			isTransparent: false
		});

		if (container) {
			container.appendChild(script);
		}
	});
</script>

{#if symbol === ''}
	<Skeleton class="h-full w-full p-2" />
{:else}
	<div class="tradingview-widget-container2" style="height: 100%; width: 100%;"></div>
{/if}
