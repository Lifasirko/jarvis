from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from news.models import News, Category

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'}


async def get_news_liga(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, features="html.parser")
                
                all_text = soup.find(attrs={"class": "article-body article-grid__body"})
                text = ' '.join(p.text for i, p in enumerate(all_text.find_all('p')[:-1]) if i != 1) if all_text else None
                
                author = soup.find(attrs={"class":"user__name"})
                author = author.text if author else None
                
                article_figure = soup.find(attrs={"class": "article-body__figure is-basic"})
                if article_figure:
                    img = article_figure.find('img')
                    img_src = img['src'] if img and 'src' in img.attrs else None
                    text_img = article_figure.find('figcaption')
                    text_img = text_img.text if text_img else None
                else:
                    img_src = None
                    text_img = None
                
                caption = soup.find(attrs={"class":"article-header__caption"})
                caption_text = caption.text if caption else None
                
                return {
                    "url": url,
                    "caption": caption_text,
                    "author": author,
                    "image": img_src,
                    "image_caption": text_img,
                    "text": text
                }
            else:
                print(f"Error status: {response.status} for {url}")
                return None
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))
        return None


async def scraping_liga(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, features="html.parser")
                all_news = soup.find_all(attrs={"class": "news-card news-list-page__card"})
                
                news_list = []
                tasks = []
                
                for news_item in all_news:
                    time = news_item.find(attrs={"class":"news-card__time"})['datetime']
                    badge = news_item.find(attrs={"class":"news-card__badge"})
                    badge = badge.text if badge else None
                    link = news_item.find('a')['href']
                    title = news_item.find('h4').text if news_item.find('h4') else None
                    
                    news_dict = {
                        'time': time,
                        'badge': badge,
                        'link': link,
                        'title': title,
                    }
                    
                    news_list.append(news_dict)
                    tasks.append(asyncio.create_task(get_news_liga(session, link)))
                
                results = await asyncio.gather(*tasks)
                
                for news_item, result in zip(news_list, results):
                    if result:
                        news_item.update(result)
            
                return news_list
            else:
                print(f"Error status: {response.status} for {url}")
                return None
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))
        return None
    

async def get_news_techcrunch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, features="html.parser")
                
                all_text = soup.find_all(attrs={"class": "wp-block-paragraph"})[:-1]
                text = ' '.join([p.text for p in all_text])
                
                author = soup.find(attrs={"class":"wp-block-tc23-author-card-name"})
                author = author.text if author else None

                category = soup.find(attrs={"class":"is-taxonomy-category"})
                category = category.text if category else None

                title = soup.find(attrs={"class":"wp-block-post-title"})
                title = title.text if title else None

                time = soup.find(attrs={"class":"wp-block-post-date"})
                time = time.find('time')['datetime'] if time else None

                caption = None
                
                article_figure = soup.find(attrs={"class": "wp-block-post-featured-image"})
                if article_figure:
                    img_src = article_figure.find('img')['src']
                    text_img = article_figure.find('figcaption')
                    text_img = text_img.text if text_img else None
                else:
                    img_src = None
                    text_img = None
                
                return {
                    "link": url,
                    "caption": caption,
                    "author": author,
                    "badge": category,
                    "title": title,
                    "time": time,
                    "image": img_src,
                    "image_caption": text_img,
                    "text": text
                }
            else:
                print(f"Error status: {response.status} for {url}")
                return None
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))
        return None


async def scraping_techcrunch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, features="html.parser")
                all_news = soup.find_all(attrs={"class": "wp-block-tc23-post-picker"})
        
                tasks = []
        
                for news_item in all_news:
                    link = news_item.find('h2').find('a')['data-destinationlink']
                    tasks.append(asyncio.create_task(get_news_techcrunch(session, link)))
        
                results = await asyncio.gather(*tasks)
                return results
            else:
                print(f"Error status: {response.status} for {url}")
                return None
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))
        return None



class Command(BaseCommand):

    def handle(self, *args, **options):
        all_news = asyncio.run(self.main())
        
        for el in all_news:
            category, _ = Category.objects.update_or_create(name=el.get('badge'))

            news, created = News.objects.update_or_create(
                source=el.get('link'),
                defaults={
                    'title': el.get('title'),
                    'caption': el.get('caption'),
                    'content': el.get('text'),
                    'author': el.get('author'),
                    'image': el.get('image'),
                    'image_caption': el.get('image_caption'),
                    'published_time': el.get('time'),
                    'category': category,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created news: {news.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated news: {news.title}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully updated news database'))

    async def main(self):
        url_1 = 'https://news.liga.net/en'
        url_2 = 'https://techcrunch.com'

        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            news_1, news_2 = await asyncio.gather(
            scraping_liga(session, url_1),
            scraping_techcrunch(session, url_2)
        )

        all_news = news_1 + news_2 if news_1 and news_2 else news_1 or news_2 or []
        
        return all_news