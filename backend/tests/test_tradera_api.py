import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import json
import xmltodict
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tradera_api import TraderaAPI

class TestTraderaAPI(unittest.TestCase):
    """Test cases for TraderaAPI class"""
    
    def setUp(self):
        """Set up test environment"""
        self.api = TraderaAPI(
            app_id="12345",
            app_key="test_key",
            sandbox=1
        )
        
        # Sample SOAP response for search
        self.sample_search_response = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                      xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <soap:Body>
            <SearchAdvancedResponse xmlns="http://api.tradera.com">
              <SearchAdvancedResult>
                <TotalNumberOfItems>2</TotalNumberOfItems>
                <TotalNumberOfPages>1</TotalNumberOfPages>
                <Items>
                  <Id>123456</Id>
                  <ShortDescription>Test Item 1</ShortDescription>
                  <BuyItNowPrice>1000</BuyItNowPrice>
                  <SellerId>9876</SellerId>
                  <SellerAlias>TestSeller</SellerAlias>
                  <MaxBid>500</MaxBid>
                  <ThumbnailLink>http://example.com/thumb1.jpg</ThumbnailLink>
                  <SellerDsrAverage>4.8</SellerDsrAverage>
                  <EndDate>2025-05-01T12:00:00Z</EndDate>
                  <NextBid>550</NextBid>
                  <HasBids>true</HasBids>
                  <IsEnded>false</IsEnded>
                  <ItemType>Auction</ItemType>
                  <ItemUrl>http://tradera.com/item/123456</ItemUrl>
                  <CategoryId>100</CategoryId>
                  <BidCount>3</BidCount>
                  <ImageLinks>
                    <ImageLink>
                      <Url>http://example.com/image1.jpg</Url>
                      <Format>jpg</Format>
                    </ImageLink>
                  </ImageLinks>
                  <LongDescription>This is a test item description</LongDescription>
                </Items>
                <Items>
                  <Id>789012</Id>
                  <ShortDescription>Test Item 2</ShortDescription>
                  <BuyItNowPrice>2000</BuyItNowPrice>
                  <SellerId>9876</SellerId>
                  <SellerAlias>TestSeller</SellerAlias>
                  <MaxBid>1200</MaxBid>
                  <ThumbnailLink>http://example.com/thumb2.jpg</ThumbnailLink>
                  <SellerDsrAverage>4.8</SellerDsrAverage>
                  <EndDate>2025-05-02T12:00:00Z</EndDate>
                  <NextBid>1250</NextBid>
                  <HasBids>true</HasBids>
                  <IsEnded>false</IsEnded>
                  <ItemType>Auction</ItemType>
                  <ItemUrl>http://tradera.com/item/789012</ItemUrl>
                  <CategoryId>100</CategoryId>
                  <BidCount>5</BidCount>
                  <ImageLinks>
                    <ImageLink>
                      <Url>http://example.com/image2.jpg</Url>
                      <Format>jpg</Format>
                    </ImageLink>
                  </ImageLinks>
                  <LongDescription>This is another test item description</LongDescription>
                </Items>
              </SearchAdvancedResult>
            </SearchAdvancedResponse>
          </soap:Body>
        </soap:Envelope>
        """
        
        # Sample SOAP response for bid
        self.sample_bid_response = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                      xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <soap:Body>
            <BuyResponse xmlns="http://api.tradera.com">
              <BuyResult>
                <NextBid>600</NextBid>
                <Status>Bought</Status>
              </BuyResult>
            </BuyResponse>
          </soap:Body>
        </soap:Envelope>
        """
        
        # Sample SOAP response for token
        self.sample_token_response = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                      xmlns:xsd="http://www.w3.org/2001/XMLSchema">
          <soap:Body>
            <FetchTokenResponse xmlns="http://api.tradera.com">
              <FetchTokenResult>
                <UserId>12345</UserId>
                <Token>abc123token</Token>
                <ExpirationDate>2025-05-01T12:00:00Z</ExpirationDate>
              </FetchTokenResult>
            </FetchTokenResponse>
          </soap:Body>
        </soap:Envelope>
        """
    
    def test_create_soap_envelope(self):
        """Test SOAP envelope creation"""
        body = "<TestBody>content</TestBody>"
        envelope = self.api._create_soap_envelope(body, include_auth=False)
        
        # Check that envelope contains required elements
        self.assertIn("<soap:Envelope", envelope)
        self.assertIn("<soap:Header>", envelope)
        self.assertIn("<soap:Body>", envelope)
        self.assertIn("<TestBody>content</TestBody>", envelope)
        self.assertIn(f"<AppId>{self.api.app_id}</AppId>", envelope)
        self.assertIn(f"<AppKey>{self.api.app_key}</AppKey>", envelope)
    
    @patch('requests.post')
    def test_search_advanced(self, mock_post):
        """Test search_advanced method"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_search_response
        mock_post.return_value = mock_response
        
        # Call method
        result = self.api.search_advanced(
            search_words="test",
            category_id=100,
            price_minimum=100,
            price_maximum=2000
        )
        
        # Verify request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Check URL
        self.assertEqual(args[0], self.api.search_service_url)
        
        # Check headers
        self.assertEqual(kwargs['headers']['SOAPAction'], "http://api.tradera.com/SearchAdvanced")
        
        # Check that request body contains search parameters
        self.assertIn("<SearchWords>test</SearchWords>", kwargs['data'])
        self.assertIn("<CategoryId>100</CategoryId>", kwargs['data'])
        self.assertIn("<PriceMinimum>100</PriceMinimum>", kwargs['data'])
        self.assertIn("<PriceMaximum>2000</PriceMaximum>", kwargs['data'])
        
        # Check result
        self.assertEqual(result['total_items'], 2)
        self.assertEqual(result['total_pages'], 1)
        self.assertEqual(len(result['items']), 2)
        
        # Check first item
        item1 = result['items'][0]
        self.assertEqual(item1['id'], 123456)
        self.assertEqual(item1['title'], 'Test Item 1')
        self.assertEqual(item1['current_price'], 500)
        self.assertEqual(item1['buy_now_price'], 1000)
        self.assertEqual(item1['seller_id'], 9876)
        self.assertEqual(item1['seller_alias'], 'TestSeller')
        self.assertEqual(item1['bid_count'], 3)
        self.assertEqual(item1['status'], 'active')
        self.assertEqual(item1['image_urls'], ['http://example.com/image1.jpg'])
    
    @patch('requests.post')
    def test_place_bid(self, mock_post):
        """Test place_bid method"""
        # Set user token
        self.api.set_user_token(12345, "test_token")
        
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_bid_response
        mock_post.return_value = mock_response
        
        # Call method
        result = self.api.place_bid(
            item_id=123456,
            bid_amount=550
        )
        
        # Verify request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Check URL
        self.assertEqual(args[0], self.api.buyer_service_url)
        
        # Check headers
        self.assertEqual(kwargs['headers']['SOAPAction'], "http://api.tradera.com/Buy")
        
        # Check that request body contains bid parameters
        self.assertIn("<itemId>123456</itemId>", kwargs['data'])
        self.assertIn("<buyAmount>550</buyAmount>", kwargs['data'])
        
        # Check that authorization header is included
        self.assertIn("<UserId>12345</UserId>", kwargs['data'])
        self.assertIn("<Token>test_token</Token>", kwargs['data'])
        
        # Check result
        self.assertEqual(result['status'], 'Bought')
        self.assertEqual(result['next_bid'], 600)
        self.assertTrue(result['success'])
    
    @patch('requests.post')
    def test_fetch_token(self, mock_post):
        """Test fetch_token method"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_token_response
        mock_post.return_value = mock_response
        
        # Call method
        result = self.api.fetch_token(
            secret_key="test_secret"
        )
        
        # Verify request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Check URL
        self.assertEqual(args[0], self.api.public_service_url)
        
        # Check headers
        self.assertEqual(kwargs['headers']['SOAPAction'], "http://api.tradera.com/FetchToken")
        
        # Check that request body contains secret key
        self.assertIn("<secretKey>test_secret</secretKey>", kwargs['data'])
        
        # Check result
        self.assertEqual(result['user_id'], 12345)
        self.assertEqual(result['token'], 'abc123token')
        self.assertEqual(result['expiration_date'], '2025-05-01T12:00:00Z')
        self.assertTrue(result['success'])
        
        # Check that token was set
        self.assertEqual(self.api.user_id, 12345)
        self.assertEqual(self.api.token, 'abc123token')
    
    def test_process_search_items(self):
        """Test _process_search_items method"""
        # Test with a single item (dict)
        single_item = {
            'Id': '123456',
            'ShortDescription': 'Test Item',
            'BuyItNowPrice': '1000',
            'SellerId': '9876',
            'SellerAlias': 'TestSeller',
            'MaxBid': '500',
            'ThumbnailLink': 'http://example.com/thumb.jpg',
            'EndDate': '2025-05-01T12:00:00Z',
            'NextBid': '550',
            'HasBids': 'true',
            'IsEnded': 'false',
            'ItemType': 'Auction',
            'ItemUrl': 'http://tradera.com/item/123456',
            'CategoryId': '100',
            'BidCount': '3',
            'ImageLinks': {
                'ImageLink': {
                    'Url': 'http://example.com/image.jpg',
                    'Format': 'jpg'
                }
            },
            'LongDescription': 'This is a test item description'
        }
        
        result = self.api._process_search_items(single_item)
        
        # Check that result is a list with one item
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        
        # Check item properties
        item = result[0]
        self.assertEqual(item['id'], 123456)
        self.assertEqual(item['title'], 'Test Item')
        self.assertEqual(item['current_price'], 500)
        self.assertEqual(item['buy_now_price'], 1000)
        self.assertEqual(item['seller_id'], 9876)
        self.assertEqual(item['seller_alias'], 'TestSeller')
        self.assertEqual(item['end_date'], '2025-05-01T12:00:00+00:00')
        self.assertEqual(item['next_bid'], 550)
        self.assertTrue(item['has_bids'])
        self.assertFalse(item['is_ended'])
        self.assertEqual(item['item_type'], 'Auction')
        self.assertEqual(item['url'], 'http://tradera.com/item/123456')
        self.assertEqual(item['category_id'], 100)
        self.assertEqual(item['bid_count'], 3)
        self.assertEqual(item['thumbnail_url'], 'http://example.com/thumb.jpg')
        self.assertEqual(item['image_urls'], ['http://example.com/image.jpg'])
        self.assertEqual(item['status'], 'active')

if __name__ == '__main__':
    unittest.main()
