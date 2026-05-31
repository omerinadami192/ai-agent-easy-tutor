import os
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from schemas_scraper import InstagramUserInfo, InstagramUserPosts
from dotenv import load_dotenv
load_dotenv()

# INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
# INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

SESSION_FILE = Path(__file__).parent / "instagram_session.json"

class InstagramScraper():
    def __init__(self, username: str, password: str):
        self.cli = Client()
        self._login(username, password)

    def _login(self, username: str, password: str) -> None:
        """Önce diskteki session ile dener, geçersizse şifreyle yeniden login olur."""
        if SESSION_FILE.exists():
            try:
                self.cli.load_settings(SESSION_FILE)
                self.cli.login(username, password)
                self.cli.get_timeline_feed()
                print("Kayıtlı session ile giriş yapıldı.")
                return
            except LoginRequired:
                print("Session süresi dolmuş, yeniden login olunuyor...")
            except Exception as e:
                print(f"Session geçersiz ({e}), yeniden login olunuyor...")

            self.cli = Client()

        self.cli.login(username, password)
        self.cli.dump_settings(SESSION_FILE)
        print("Yeni session oluşturuldu ve kaydedildi.")

    def _get_user_by_username(self, username: str):
        try:
            user = self.cli.user_info_by_username(username)
            return user

        except Exception as e:
            print(f"Kullanıcı bulunamadı: {e}")
            return None

    def get_user_info(self, username: str) -> InstagramUserInfo:
        """ 
            Verilen username e sahip instagram kullanıcısıyla alakalı verileri InstagramUserInfo şemasına göre döndürür. 
        
            Args: 
                username: Verilen kullanıcının instagram kullanıcı adını içerir.

            Returns:
                bio: Kullanıcının biyografi metni
                full_name: Tam adı
                post_sayisi: Gönderi sayısı
                takipci_sayisi: Takipçi sayısı
                takip_sayisi: Takip edilen sayısı
                bio_linkleri: Bio linkleri
                profil_pic: Profil fotoğraf URL'si
        """

        try:
            user = self._get_user_by_username(username)
            bio = user.biography
            full_name = user.full_name
            post_sayisi = user.media_count
            takipci_sayisi = user.follower_count
            takip_sayisi = user.following_count
            bio_linkleri = user.bio_links
            profil_pic = user.profile_pic_url_hd

            return {
                "bio": bio,
                "full_name": full_name,
                "post_sayisi": post_sayisi,
                "takipci_sayisi": takipci_sayisi,
                "takip_sayisi": takip_sayisi,
                "bio_linkleri": bio_linkleri,
                "profil_pic": profil_pic
            }
        
        except Exception as e:
            print(f"Hesap bilgileri alınırken bir hata meydana geldi: {e}")
            return None

    def get_user_medias(self, username: str, post_amount: int = 10) -> InstagramUserPosts:
        """
        Aranan kullanıcının instagrama attığı post ve medyalarının bilgilerini döndüren fonksiyon.

        Args:
            username: Aranan kullanıcının instagram kullanıcı adı
            post_amount: Kullanıcının kaç tane postuna bakılacağı. Default olarak 10 dur.
                Kullanıcının çok fazla postu varsa llm tercihiyle arttırılabilir.

        Returns:
            list[dict]: Instagram postlarının detaylı listesi

            Post Schema:
                {
                    "baslik": str,           # Post caption text
                    "like_count": int,       # Beğeni sayısı
                    "comment_count": int,    # Yorum sayısı
                    "comments": list[dict]   # Yorum listesi
                }

            Comment Schema:
                {
                    "username": str,  # Yorumu yapan kullanıcı
                    "text": str       # Yorum içeriği
                }
"""
        
        try:
            user_id = self.cli.user_id_from_username(username)
            posts = self.cli.user_medias(user_id, amount=post_amount)

            result = []
            for post in posts:
                post_comments = []
                try:
                    yorumlar = self.cli.media_comments(post.id, amount=50)
                    for comment in yorumlar:
                        post_comments.append({
                            "username": comment.user.username,
                            "text": comment.text
                        })
                except Exception as e:
                    print(f"{post.id} idli postun yorumları alınamadı: {e}")

                result.append({
                    "baslik": post.caption_text,
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "comments": post_comments
                })

            return result

        except Exception as e:
            print(f"Hata kişinin postları alınırken hata oluştu: {e}")
            return None