import { scriptsApi } from './scripts';
import { auctionsApi } from './auctions';
import { biddingApi } from './bidding';

// Export all API services
export default {
  scripts: scriptsApi,
  auctions: auctionsApi,
  bidding: biddingApi
};
