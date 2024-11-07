<script lang="ts">
	import { Skeleton } from '$lib/components/ui/skeleton';

	let { symbol = '' } = $props();

	$effect(() => {
		if (symbol === '') return;

		// Get the container element
		const container = document.querySelector('.tradingview-widget-container');

		// Clear any existing widget
		while (container?.firstChild) {
			container.removeChild(container.firstChild);
		}

		// Create a new script element for the Symbol Overview widget
		const script = document.createElement('script');
		script.type = 'text/javascript';
		script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js';
		script.async = true;
		script.innerHTML = JSON.stringify({
			symbols: [
				[
					symbol.toUpperCase(),
					`${symbol.toUpperCase()}|1D`
				]
			],
			chartOnly: false,
			width: '100%',
			height: '100%',
			locale: 'en',
			colorTheme: 'dark',
			autosize: true,
			showVolume: false,
			showMA: false,
			hideDateRanges: false,
			hideMarketStatus: false,
			hideSymbolLogo: false,
			scalePosition: 'right',
			scaleMode: 'Normal',
			fontFamily: '-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif',
			fontSize: '10',
			noTimeScale: false,
			valuesTracking: '1',
			changeMode: 'price-and-percent',
			chartType: 'area',
			maLineColor: '#2962FF',
			maLineWidth: 1,
			maLength: 9,
			headerFontSize: 'medium',
			lineWidth: 2,
			lineType: 0,
			dateRanges: [
				"1d|1",
				"1m|30",
				"3m|60",
				"12m|1D",
				"60m|1W",
				"all|1M"
			]
		});

		// Append the script to the container
		if (container) {
			container.appendChild(script);
		}
	});
</script>

{#if symbol === ''}
	<div class="flex h-full w-full p-2">
		<div class="h-full w-4/5 p-2">
			<Skeleton class="h-full w-full rounded-lg p-2" />
		</div>
		<div class="h-full w-1/5">
			<Skeleton class="m-2 px-2 py-5" />
			<Skeleton class="m-2 px-2 py-5" />
			<Skeleton class="m-2 px-2 py-5" />
			<Skeleton class="m-2 px-2 py-5" />
			<Skeleton class="m-2 px-2 py-5" />
			<Skeleton class="m-2 px-2 py-5" />
			<Skeleton class="m-2 px-2 py-5" />
			<Skeleton class="m-2 px-2 py-5" />
		</div>
	</div>
{:else}
	<div class="tradingview-widget-container" style="height:100%;width:100%"></div>
{/if}
