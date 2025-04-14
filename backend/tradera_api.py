"""
Tradera API Integration Module

This module handles all interactions with the Tradera API, including:
- Authentication with AppId and AppKey
- SOAP request formatting for SearchAdvanced
- Integration with BuyerService for bidding
- Token-based authorization for restricted operations
"""

import os
import requests
import xmltodict
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TraderaAPI:
    """Client for interacting with Tradera's SOAP API"""
    
    def __init__(self, app_id: str, app_key: str, sandbox: int = 0):
        """
        Initialize the Tradera API client
        
        Args:
            app_id: Tradera API application ID
            app_key: Tradera API application key
            sandbox: Use sandbox mode (0 for production, 1 for sandbox)
        """
        self.app_id = app_id
        self.app_key = app_key
        self.sandbox = sandbox
        self.max_result_age = 60  # Default max result age in seconds
        
        # API endpoints
        self.search_service_url = "https://api.tradera.com/v3/searchservice.asmx"
        self.buyer_service_url = "https://api.tradera.com/v3/buyerservice.asmx"
        self.public_service_url = "https://api.tradera.com/v3/publicservice.asmx"
        
        # SOAP namespaces
        self.soap_ns = "http://schemas.xmlsoap.org/soap/envelope/"
        self.api_ns = "http://api.tradera.com"
        
        # Headers for SOAP requests
        self.headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": ""  # Will be set per request
        }
        
        # User token for restricted operations
        self.user_id = None
        self.token = None
    
    def set_user_token(self, user_id: int, token: str):
        """
        Set user token for restricted operations
        
        Args:
            user_id: Tradera user ID
            token: Authentication token
        """
        self.user_id = user_id
        self.token = token
    
    def _create_authentication_header(self) -> str:
        """Create SOAP authentication header with AppId and AppKey"""
        return f"""
        <AuthenticationHeader xmlns="{self.api_ns}">
            <AppId>{self.app_id}</AppId>
            <AppKey>{self.app_key}</AppKey>
        </AuthenticationHeader>
        """
    
    def _create_authorization_header(self) -> str:
        """Create SOAP authorization header with UserId and Token"""
        if not self.user_id or not self.token:
            return ""
            
        return f"""
        <AuthorizationHeader xmlns="{self.api_ns}">
            <UserId>{self.user_id}</UserId>
            <Token>{self.token}</Token>
        </AuthorizationHeader>
        """
    
    def _create_configuration_header(self) -> str:
        """Create SOAP configuration header with Sandbox and MaxResultAge"""
        return f"""
        <ConfigurationHeader xmlns="{self.api_ns}">
            <Sandbox>{self.sandbox}</Sandbox>
            <MaxResultAge>{self.max_result_age}</MaxResultAge>
        </ConfigurationHeader>
        """
    
    def _create_soap_envelope(self, body: str, include_auth: bool = True) -> str:
        """
        Create a SOAP envelope with the appropriate headers and body
        
        Args:
            body: The SOAP body content
            include_auth: Whether to include authorization header (for restricted operations)
            
        Returns:
            Complete SOAP envelope as string
        """
        auth_header = self._create_authentication_header()
        config_header = self._create_configuration_header()
        authorization = self._create_authorization_header() if include_auth and self.user_id and self.token else ""
        
        return f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                      xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                      xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Header>
            {auth_header}
            {config_header}
            {authorization}
          </soap:Header>
          <soap:Body>
            {body}
          </soap:Body>
        </soap:Envelope>
        """
    
    def search_advanced(self, 
                       search_words: Optional[str] = None,
                       category_id: int = 0,
                       search_in_description: bool = True,
                       price_minimum: Optional[int] = None,
                       price_maximum: Optional[int] = None,
                       item_type: Optional[str] = None,
                       item_status: Optional[str] = None,
                       items_per_page: int = 25,
                       page_number: int = 1,
                       order_by: Optional[str] = "EndDateAscending") -> Dict:
        """
        Search for items with advanced parameters
        
        Args:
            search_words: Keywords to search for
            category_id: Category ID (0 for all categories)
            search_in_description: Whether to search in item descriptions
            price_minimum: Minimum price
            price_maximum: Maximum price
            item_type: Type of item (Auction, PureBuyItNow, ShopItem)
            item_status: Status of item
            items_per_page: Number of items per page
            page_number: Page number (starting from 1)
            order_by: How to order results
            
        Returns:
            Dictionary containing search results
        """
        # Create request body
        request_body = f"""
        <SearchAdvanced xmlns="{self.api_ns}">
          <request>
            <SearchWords>{search_words or ""}</SearchWords>
            <CategoryId>{category_id}</CategoryId>
            <SearchInDescription>{str(search_in_description).lower()}</SearchInDescription>
            <PriceMinimum>{f"<PriceMinimum>{price_minimum}</PriceMinimum>" if price_minimum is not None else "<PriceMinimum xsi:nil='true' />"}</PriceMinimum>
            <PriceMaximum>{f"<PriceMaximum>{price_maximum}</PriceMaximum>" if price_maximum is not None else "<PriceMaximum xsi:nil='true' />"}</PriceMaximum>
            <ItemType>{item_type or ""}</ItemType>
            <ItemStatus>{item_status or ""}</ItemStatus>
            <ItemsPerPage>{items_per_page}</ItemsPerPage>
            <PageNumber>{page_number}</PageNumber>
            <OrderBy>{order_by}</OrderBy>
          </request>
        </SearchAdvanced>
        """
        
        # Set SOAPAction header
        self.headers["SOAPAction"] = "http://api.tradera.com/SearchAdvanced"
        
        # Create full SOAP envelope
        soap_envelope = self._create_soap_envelope(request_body, include_auth=False)
        
        # Make the request
        response = requests.post(
            self.search_service_url,
            headers=self.headers,
            data=soap_envelope
        )
        
        # Check for errors
        if response.status_code != 200:
            logger.error(f"Error searching Tradera: {response.status_code} - {response.text}")
            return {"error": f"API error: {response.status_code}", "details": response.text}
        
        # Parse XML response
        try:
            response_dict = xmltodict.parse(response.text)
            soap_body = response_dict.get('soap:Envelope', {}).get('soap:Body', {})
            search_result = soap_body.get('SearchAdvancedResponse', {}).get('SearchAdvancedResult', {})
            
            # Process and return the results
            return {
                "total_items": int(search_result.get('TotalNumberOfItems', 0)),
                "total_pages": int(search_result.get('TotalNumberOfPages', 0)),
                "items": self._process_search_items(search_result.get('Items', [])),
                "errors": search_result.get('Errors', [])
            }
        except Exception as e:
            logger.error(f"Error parsing Tradera response: {str(e)}")
            return {"error": f"Response parsing error: {str(e)}"}
    
    def _process_search_items(self, items: Any) -> List[Dict]:
        """
        Process search items from Tradera response
        
        Args:
            items: Items from Tradera response (could be dict or list)
            
        Returns:
            List of processed item dictionaries
        """
        # Handle case where there's only one item (comes as dict, not list)
        if isinstance(items, dict):
            items = [items]
        elif not isinstance(items, list):
            return []
        
        processed_items = []
        for item in items:
            try:
                # Convert string values to appropriate types
                end_date = datetime.fromisoformat(item.get('EndDate').replace('Z', '+00:00')) if item.get('EndDate') else None
                
                processed_item = {
                    "id": int(item.get('Id', 0)),
                    "tradera_id": str(item.get('Id', '')),
                    "title": item.get('ShortDescription', ''),
                    "description": item.get('LongDescription', ''),
                    "current_price": int(item.get('MaxBid', 0)) if item.get('MaxBid') else 0,
                    "buy_now_price": int(item.get('BuyItNowPrice', 0)) if item.get('BuyItNowPrice') else None,
                    "seller_id": int(item.get('SellerId', 0)),
                    "seller_alias": item.get('SellerAlias', ''),
                    "end_date": end_date.isoformat() if end_date else None,
                    "next_bid": int(item.get('NextBid', 0)) if item.get('NextBid') else None,
                    "has_bids": item.get('HasBids', 'false').lower() == 'true',
                    "is_ended": item.get('IsEnded', 'false').lower() == 'true',
                    "item_type": item.get('ItemType', ''),
                    "url": item.get('ItemUrl', ''),
                    "category_id": int(item.get('CategoryId', 0)),
                    "bid_count": int(item.get('BidCount', 0)),
                    "thumbnail_url": item.get('ThumbnailLink', ''),
                    "image_urls": self._extract_image_urls(item.get('ImageLinks', {})),
                    "status": "ended" if item.get('IsEnded', 'false').lower() == 'true' else "active"
                }
                processed_items.append(processed_item)
            except Exception as e:
                logger.error(f"Error processing item: {str(e)}")
                # Skip this item and continue with others
                continue
                
        return processed_items
    
    def _extract_image_urls(self, image_links: Any) -> List[str]:
        """Extract image URLs from ImageLinks structure"""
        urls = []
        
        # Handle different possible structures
        if isinstance(image_links, dict):
            # Single image link
            if 'ImageLink' in image_links:
                if isinstance(image_links['ImageLink'], dict) and 'Url' in image_links['ImageLink']:
                    urls.append(image_links['ImageLink']['Url'])
                elif isinstance(image_links['ImageLink'], list):
                    for link in image_links['ImageLink']:
                        if isinstance(link, dict) and 'Url' in link:
                            urls.append(link['Url'])
        
        return urls
    
    def place_bid(self, item_id: int, bid_amount: int) -> Dict:
        """
        Place a bid on an auction
        
        Args:
            item_id: Tradera item ID
            bid_amount: Bid amount in SEK
            
        Returns:
            Dictionary with bid result
        """
        if not self.user_id or not self.token:
            return {"error": "User token not set. Authentication required for bidding."}
        
        # Create request body
        request_body = f"""
        <Buy xmlns="{self.api_ns}">
          <itemId>{item_id}</itemId>
          <buyAmount>{bid_amount}</buyAmount>
        </Buy>
        """
        
        # Set SOAPAction header
        self.headers["SOAPAction"] = "http://api.tradera.com/Buy"
        
        # Create full SOAP envelope
        soap_envelope = self._create_soap_envelope(request_body, include_auth=True)
        
        # Make the request
        response = requests.post(
            self.buyer_service_url,
            headers=self.headers,
            data=soap_envelope
        )
        
        # Check for errors
        if response.status_code != 200:
            logger.error(f"Error placing bid: {response.status_code} - {response.text}")
            return {"error": f"API error: {response.status_code}", "details": response.text}
        
        # Parse XML response
        try:
            response_dict = xmltodict.parse(response.text)
            soap_body = response_dict.get('soap:Envelope', {}).get('soap:Body', {})
            buy_result = soap_body.get('BuyResponse', {}).get('BuyResult', {})
            
            return {
                "status": buy_result.get('Status', ''),
                "next_bid": int(buy_result.get('NextBid', 0)) if buy_result.get('NextBid') else None,
                "success": buy_result.get('Status', '') == 'Bought'
            }
        except Exception as e:
            logger.error(f"Error parsing bid response: {str(e)}")
            return {"error": f"Response parsing error: {str(e)}"}
    
    def fetch_token(self, secret_key: str) -> Dict:
        """
        Fetch a user token after token login
        
        Args:
            secret_key: Secret key used in token login
            
        Returns:
            Dictionary with token information
        """
        # Create request body
        request_body = f"""
        <FetchToken xmlns="{self.api_ns}">
          <secretKey>{secret_key}</secretKey>
        </FetchToken>
        """
        
        # Set SOAPAction header
        self.headers["SOAPAction"] = "http://api.tradera.com/FetchToken"
        
        # Create full SOAP envelope
        soap_envelope = self._create_soap_envelope(request_body, include_auth=False)
        
        # Make the request
        response = requests.post(
            self.public_service_url,
            headers=self.headers,
            data=soap_envelope
        )
        
        # Check for errors
        if response.status_code != 200:
            logger.error(f"Error fetching token: {response.status_code} - {response.text}")
            return {"error": f"API error: {response.status_code}", "details": response.text}
        
        # Parse XML response
        try:
            response_dict = xmltodict.parse(response.text)
            soap_body = response_dict.get('soap:Envelope', {}).get('soap:Body', {})
            fetch_result = soap_body.get('FetchTokenResponse', {}).get('FetchTokenResult', {})
            
            # If successful, set the token for future requests
            if fetch_result.get('Token') and fetch_result.get('UserId'):
                self.set_user_token(
                    user_id=int(fetch_result.get('UserId')),
                    token=fetch_result.get('Token')
                )
            
            return {
                "user_id": int(fetch_result.get('UserId', 0)) if fetch_result.get('UserId') else None,
                "token": fetch_result.get('Token', ''),
                "expiration_date": fetch_result.get('ExpirationDate', ''),
                "success": bool(fetch_result.get('Token') and fetch_result.get('UserId'))
            }
        except Exception as e:
            logger.error(f"Error parsing token response: {str(e)}")
            return {"error": f"Response parsing error: {str(e)}"}
