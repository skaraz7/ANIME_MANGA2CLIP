import requests
from bs4 import BeautifulSoup

BASE_URL = "https://monoschinos2.net"

def get_trending_animes():
    url = f"{BASE_URL}/"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    trending = []
    for anime in soup.select("div.anime__item a"):
        title = anime.get("title")
        link = anime.get("href")
        if title and link:
            trending.append({
                "title": title.strip(),
                "url": BASE_URL + link
            })
    return trending

def get_episodes(anime_url):
    response = requests.get(anime_url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    episodes = []
    for ep in soup.select("ul#episodeList li a"):
        ep_title = ep.text.strip()
        ep_url = BASE_URL + ep.get("href")
        episodes.append({
            "episode": ep_title,
            "url": ep_url
        })
    return episodes

def get_mp4upload_link(episode_url):
    response = requests.get(episode_url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    
    mp4_link = None
    for iframe in soup.select("iframe"):
        src = iframe.get("src")
        if "mp4upload" in src:
            mp4_link = src
            break
    return mp4_link

if __name__ == "__main__":
    print("Buscando animes en tendencia...")
    animes = get_trending_animes()
    for anime in animes[:3]:  # solo 3 para probar
        print(f"\nAnime: {anime['title']}")
        episodes = get_episodes(anime["url"])
        if episodes:
            first_ep = episodes[0]
            print(f"  Episodio: {first_ep['episode']} - {first_ep['url']}")
            mp4 = get_mp4upload_link(first_ep["url"])
            if mp4:
                print(f"  MP4UPLOAD: {mp4}")
                print(f"  Descargar con: yt-dlp {mp4}")
