export interface News {
	title: string;
	url: string;
	urlToImg: string | null;
	confidence: number;
	sentiment: string;
	publishedAt: string;
}

export interface BasicInfo {
	Metric: string;
	Value: number | string;
}

export interface Results {
	news: News[];
	basicInfo: BasicInfo[];
	investmentInsights: string;
	fundamentalSummary: string;
	bearishView: string;
	bullishView: string;
}

export type Company = {
	company_name: string;
	stock_symbol: string;
};

export type Chat = {
	type: string;
	message: string;
};
