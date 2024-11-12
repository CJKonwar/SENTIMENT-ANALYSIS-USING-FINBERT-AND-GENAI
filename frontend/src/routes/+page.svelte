<script lang="ts">
	import { onMount } from 'svelte';

	import '../app.css';

	import io from 'socket.io-client';
	import type { Socket } from 'socket.io-client';
	import type { Results, Company } from './types';

	import Bot from 'lucide-svelte/icons/bot';
	import Download from 'lucide-svelte/icons/download';
	import LoaderCircle from 'lucide-svelte/icons/loader-circle';

	import {
		NewsCard,
		NewsSkeleton,
		StockInfo,
		Tradingview,
		Insight,
		Summary,
		StockViews,
		Search,
		ChatBot
	} from './(components)';

	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { Toaster } from '$lib/components/ui/sonner';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import { toast } from 'svelte-sonner';

	let selectedCompany: Company = $state<Company>({ company_name: '', stock_symbol: '' });

	let results: Results = $state({
		news: [],
		basicInfo: [],
		investmentInsights: '',
		fundamentalSummary: '',
		bearishView: '',
		bullishView: ''
	});

	let symbol = $state('');

	let socket: Socket;

	onMount(() => {
		socket = io('http://localhost:5000');

		socket.on('news', (data) => {
			results.news = data.data;

		});

		socket.on('basic_info', (data) => {
			results.basicInfo = data.data;
		});

		socket.on('investment_insights', (data) => {
			results.investmentInsights = data.data;
		});

		socket.on('bullish', (data) => {
			results.bullishView = data.data;
		});

		socket.on('bearish', (data) => {
			results.bearishView = data.data;
		});

		socket.on('fundamental_summary', (data) => {
			results.fundamentalSummary = data.data;
		});

		socket.on('error', (data) => {
			toast.error(data.message);
		});

		return () => socket?.disconnect();
	});

	function handleUpdate(e: CustomEvent) {
		selectedCompany = e.detail;

		if (selectedCompany.company_name !== '' && selectedCompany.stock_symbol !== '') {
			results = {
				news: [],
				basicInfo: [],
				investmentInsights: '',
				fundamentalSummary: '',
				bearishView: '',
				bullishView: ''
			};
			socket.emit('fetch_data', {
				company_name: selectedCompany.company_name,
				symbol: selectedCompany.stock_symbol
			});
			symbol = selectedCompany.stock_symbol;
		}
	}

	async function downloadPDF() {
		const response = await fetch(`http://localhost:5000/api/download-pdf?symbol=${symbol}`);
		if (response.ok) {
			const blob = await response.blob();
			const url = URL.createObjectURL(blob);

			const a = document.createElement('a');
			a.href = url;
			a.download = `${symbol}-stock-info.pdf`;
			a.click();

			URL.revokeObjectURL(url);
		} else {
			console.error('Failed to download PDF');
		}
	}
</script>
<style>

	.right-section-mob{
		display: none;
	}
	/* Responsive design: stack left and right sections vertically on smaller screens */
	@media (max-width: 768px) {
		.main-container {
			flex-direction: column;
		}

		.left-section,
		.right-section-mob {
			width: 100%;
		}

		 .tradingview, .basic-info-section, .views-section, .insights-section, .summary-section, .news-section {
			margin-bottom: 1rem;
		}
	}
	@media (max-width: 768px) {
		.mob-chat{
			display: none;
		}
		.right-section-dex{
			display: none;
		}
		.right-section-mob {
			display: block;

		}
	}
</style>
<div class="fixed h-screen w-screen">
	<Toaster position="bottom-center" richColors />

	<nav class="mx-auto my-2 flex flex-col sm:flex-row items-center gap-6 px-8 py-4">
		<Search {selectedCompany} on:updateCompany={handleUpdate} />

</nav>



	<!-- Chat Bot Dialog -->
	<div class="chatbot-dex">
		<Dialog.Root>
		  <Dialog.Trigger class="absolute bottom-7 right-3 z-50 flex items-center gap-2 bg-gray-800 p-2 rounded-full">
			  <div class="mob-chat">
			<span class="text-white font-semibold">Chatbot</span>
				  </div>
			<div class="grid aspect-square w-16 place-content-center rounded-full bg-white">
			  <Bot size={34} class="text-black" />
			</div>
		  </Dialog.Trigger>
		  <Dialog.Content class="border-gray-600 p-2">
			<ChatBot />
		  </Dialog.Content>
		</Dialog.Root>

	</div>



	<!-- Main Container for Left and Right Sections -->
	<div class="main-container box-border flex h-[90vh] w-full">

		<!-- Left Section -->
		<div class="left-section no-scrollbar m-1 w-2/3 overflow-y-scroll pl-3 pr-2">
			<!-- Widgets and Trading Views -->
<!--			<div class="stock-widget h-[150px] w-full">-->
<!--				<StockWidget symbol={symbol ?? ''} />-->
<!--			</div>-->
<!--			<Separator class="my-2" />-->
			<div class="tradingview h-3/4 w-full border-2 border-gray-600">
				<Tradingview symbol={symbol ?? ''} />
			</div>

			<!-- Conditionally Rendered Sections -->
			{#if results.basicInfo.length > 0}
				<div class="basic-info-section">
					<StockInfo basicInfo={results.basicInfo} />
				</div>

			{/if}

			<div class="right-section-mob scrollbar m-1 box-border flex max-h-[100vh] w-1/3 flex-col gap-4 overflow-y-scroll rounded-xl border-2 border-gray-600 p-2">
			{#if results.news.length > 0}
				<h1 class="px-4 py-2 text-2xl">News Sentiments</h1>
				<div class="news-section flex h-max w-full flex-col gap-2">
					{#each results.news as news}
						<NewsCard {...news} />
					{/each}
				</div>
			{:else}
				<NewsSkeleton />
			{/if}
		</div>
			{#if results.bullishView.length > 0 || results.bearishView.length > 0}
				<Separator />
				<div class="views-section">
					<StockViews bearishView={results.bearishView} bullishView={results.bullishView} />
				</div>
			{/if}
			{#if results.investmentInsights.length > 0}
				<Separator />
				<div class="insights-section">
					<Insight data={results.investmentInsights} />
				</div>
			{/if}
			{#if results.fundamentalSummary.length > 0}
				<Separator />
					<Button
		class="flex gap-4 w-full sm:w-auto"
		on:click={downloadPDF}
		disabled={results.fundamentalSummary === '' ||
			results.investmentInsights === '' ||
			results.basicInfo.length === 0}
	>
		<!-- Conditional Icons -->
		{#if symbol === ''}
			<Download />
		{:else if results.fundamentalSummary === '' || results.investmentInsights === '' || results.basicInfo.length === 0}
			<LoaderCircle class="h-4 w-4 animate-spin" />
		{:else}
			<Download />
		{/if}
		<span>Download Advanced Fundamental</span>
	</Button>

				<Separator />

				<div class="summary-section">
					<Summary data={results.fundamentalSummary} />

				</div>
			{/if}

			<!-- Skeleton Loader for Loading State -->
			{#if results.fundamentalSummary === '' || results.investmentInsights === '' || results.basicInfo.length === 0}
				<div class="h-fit p-2">
					<Skeleton class="mx-4 my-3 w-1/2 px-2 py-5" />
					<Skeleton class="m-3 w-5/6 rounded-lg p-2" />
					<Skeleton class="m-3 w-11/12 rounded-lg p-2" />
					<Skeleton class="m-3 w-5/6 rounded-lg p-2" />
				</div>
			{/if}




		</div>

		<!-- Right Section: News Sentiments -->

			<div class="right-section-dex no-scrollbar m-1 box-border flex max-h-[100vh] w-1/3 flex-col gap-4 overflow-y-scroll rounded-xl border-2 border-gray-600 p-2">
			{#if results.news.length > 0}
				<h1 class="px-4 py-2 text-2xl">News Sentiments</h1>
				<div class="news-section flex h-max w-full flex-col gap-2">
					{#each results.news as news}
						<NewsCard {...news} />
					{/each}
				</div>
			{:else}
				<NewsSkeleton />
			{/if}
			</div>

	</div>
</div>
