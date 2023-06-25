from unittest.mock import patch, Mock
from django.test import TestCase
from kyiv_weather.exceptions import NetworkError, ParsingError, DataExtractionError
from kyiv_weather.models import Weather
from kyiv_weather.scraper import parse_weather, save_weather, sync_weather
from requests.exceptions import RequestException


class ScraperTestCase(TestCase):
    @patch('kyiv_weather.scraper.cloudscraper.create_scraper')
    def test_parse_weather_network_error(self, mock_scraper):
        mock_scraper.side_effect = RequestException('Network error')
        with self.assertRaises(NetworkError):
            parse_weather()

    @patch('kyiv_weather.scraper.BeautifulSoup')
    @patch('kyiv_weather.scraper.cloudscraper.create_scraper')
    def test_parse_weather_parsing_error(self, mock_scraper, mock_soup):
        mock_scraper.return_value.get.return_value.content = 'test'
        mock_soup.side_effect = Exception('Parsing error')
        with self.assertRaises(ParsingError):
            parse_weather()

    @patch('kyiv_weather.scraper.BeautifulSoup')
    @patch('kyiv_weather.scraper.cloudscraper.create_scraper')
    def test_parse_weather_data_extraction_error(self, mock_scraper, mock_soup):
        mock_soup.return_value.select.return_value = []
        with self.assertRaises(DataExtractionError):
            weather = [
                Weather(date="2023-05-30", temperature=25, description="Sunny"),
                Weather(date="2023-05-31", temperature=27, description="Cloudy"),
            ]
            mock_scraper.return_value.get.return_value.content = 'test'
            mock_soup.return_value.select.return_value = [Mock(), Mock()]
            parse_weather()
            save_weather(weather)

    @patch('kyiv_weather.scraper.Weather.objects.update_or_create')
    @patch('kyiv_weather.scraper.parse_weather')
    def test_save_weather(self, mock_parse, mock_update_or_create):
        mock_weather = Mock(spec=Weather)
        mock_parse.return_value = [mock_weather]
        save_weather(mock_parse())
        mock_update_or_create.assert_called_once_with(
            date=mock_weather.date,
            defaults={
                "temperature": mock_weather.temperature,
                "description": mock_weather.description,
            },
        )

    @patch('kyiv_weather.scraper.save_weather')
    @patch('kyiv_weather.scraper.parse_weather')
    def test_sync_weather(self, mock_parse, mock_save):
        sync_weather()
        mock_parse.assert_called_once()
        mock_save.assert_called_once()
