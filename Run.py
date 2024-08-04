#!/usr/bin/env python3
try:
    import requests, re, time, os, base64, json
    from rich import print as printf
    from rich.panel import Panel
    from rich.console import Console
    from requests.exceptions import RequestException
except (Exception) as e:
    exit(f"{type(e).__name__} : {str(e).capitalize()}!")

COOKIES, SUKSES, GAGAL = {
    "NAME": None
}, [], []

class KIRIMKAN:

    def __init__(self) -> None:
        pass

    def VALIDASI_COOKIES(self, cookies):
        with requests.Session() as r:
            r.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Site': 'none',
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Host': 'tanglike.biz',
            })
            response = r.get('https://tanglike.biz/index.php')
            r.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'https://tanglike.biz/index.php',
                'Sec-Fetch-Site': 'same-origin',
                'Accept': '*/*',
                'Cookie': '; '.join([str(x) + '=' + str(y) for x, y in r.cookies.get_dict().items()]),
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Origin': 'https://tanglike.biz',
            })
            if 'EAAAAU' in str(cookies):
                data = {
                    'access_token': cookies,
                    'type': True,
                    'cookies': '',
                }
            else:
                data = {
                    'access_token': '',
                    'type': True,
                    'cookies': base64.b64encode(cookies.encode("ascii")).decode("ascii"),
                }
            response2 = r.post('https://tanglike.biz/login.php', data = data)
            if str(response2.text) == '2':
                COOKIES.update({
                    "NAME": '; '.join([str(x) + '=' + str(y) for x, y in r.cookies.get_dict().items()])
                })
                return ("0_0")
            else:
                printf(Panel(f"[italic red]Sepertinya Akun Facebook Anda Terkena Checkpoint Atau Sudah Kedaluwarsa, Silahkan Gunakan Akun Lain Untuk Login!", width=66, style="bold dark_goldenrod", title=">>> [Login Gagal] <<<"))
                time.sleep(6.5)
                self.MAIN()

    def PENGIRIMAN_LIKES(self, cookies, id_like):
        with requests.Session() as r:
            r.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': '{}'.format(cookies),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Host': 'tanglike.biz',
            })
            response = r.get('https://tanglike.biz/hacklike.php')
            if 'MEMBER ID:' not in str(response.text):
                printf(Panel(f"[italic red]Sepertinya Akun Facebook Anda Terkena Checkpoint Atau Sudah Kedaluwarsa, Silahkan Gunakan Akun Lain Untuk Login!", width=66, style="bold dark_goldenrod", title=">>> [Login Gagal] <<<"))
                time.sleep(6.5)
                self.MASUKAN_COOKIES()
            else:
                self.sitekey = re.search(r"{'sitekey' : '([^']+)'", str(response.text)).group(1)
                r.headers.update({
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Referer': 'https://tanglike.biz/hacklike.php',
                    'Accept': '*/*',
                    'Cookie': '{}'.format(cookies),
                    'Origin': 'https://tanglike.biz',
                })
                self.g_recaptcha_response = BYPASS().RECAPTCHA(self.sitekey)
                data = {
                    'g-recaptcha-response': '{}'.format(self.g_recaptcha_response),
                    'id_like': '{}'.format(id_like),
                    'limit': '100', # Số lượt thích phải ít hơn 100!
                    'tanglike': '',
                }
                response2 = r.post('https://tanglike.biz/hacklike.php', data = data)
                if 'Bạn đã dùng quá giới hạn hôm nay' in str(response2.text):
                    printf(Panel(f"[italic red]Anda Telah Melampaui Batas Hari Ini, Silakan Kembali Lagi Besok Atau Masuk Dengan Akun Lain Untuk Terus Menggunakan Layanan Ini!", width=66, style="bold dark_goldenrod", title=">>> [Limit] <<<"))
                    exit()
                elif 'Thành công - Đăng nhập thêm nick khác để hack nhiều hơn' in str(response2.text):
                    SUKSES.append(f'{str(response2.text)}')
                    printf(Panel(f"""[bold white]Status :[italic green] Thành công, gửi lượt thích![/]
[bold white]Link :[bold yellow] https://web.facebook.com/{id_like}
[bold white]Likes :[bold red] -+ 100""", width=66, style="bold dark_goldenrod", title=">>> [Sukses] <<<"))
                    self.DELAY(900, id_like)
                    return ("0_0")
                elif 'Like Không Thành Công - Vui lòng đợi 15p sau quay lại' in str(response2.text):
                    printf(f"[bold dark_goldenrod]   ──>[bold red] TERKENA LIMIT, SILAHKAN TUNGGU 15 MENIT!     ", end='\r')
                    time.sleep(5.5)
                    self.DELAY(895, id_like)
                    return ("-_-")
                elif 'Vui lòng điền đầy đủ' in str(response2.text):
                    printf(f"[bold dark_goldenrod]   ──>[bold red] COOKIES KAMU SUDAH TIDAK VALID!          ", end='\r')
                    time.sleep(5.5)
                    return ("-_0")
                else:
                    GAGAL.append(f'{str(response2.text)}')
                    printf(f"[bold dark_goldenrod]   ──>[bold red] GAGAL MENGIRIMKAN LIKES!                 ", end='\r')
                    time.sleep(5.5)
                    return ("0_-")

    def DELAY(self, times, id_like):
        global SUKSES, GAGAL
        for sleep in range(int(times), 0, -1):
            time.sleep(1.0)
            printf(f"[bold dark_goldenrod]   ──>[bold green] {id_like}[bold white]/[bold yellow]{sleep}[bold white] SUKSES:-[bold green]{len(SUKSES)}[bold white] GAGAL:-[bold red]{len(GAGAL)}    ", end='\r')
        return ("0_0")

    def MAIN(self):
        try:
            BANNER()
            printf(Panel(f"[italic white]Silahkan Masukan Cookies Akun Facebook, Anda Direkomendasikan Untuk Mengunakan[italic red] Akun Palsu[italic white] Dan Pastikan Cookies Yang Kamu Masukan Sudah[italic green] Benar[italic white]!", width=66, style="bold dark_goldenrod", title=">>> [Facebook Cookies] <<<", subtitle="╭──────", subtitle_align="left"))
            self.cookies = Console().input(f"[bold dark_goldenrod]   ╰─> ")
            self.VALIDASI_COOKIES(cookies=self.cookies)
            printf(Panel(f"[italic white]Silahkan Masukan ID Postingan, Pastikan Akun Tidak Terkunci Dan Postingan Bisa Disukai Oleh Publik!", width=66, style="bold dark_goldenrod", title=">>> [Postingan] <<<", subtitle="╭──────", subtitle_align="left"))
            self.id_like = int(Console().input(f"[bold dark_goldenrod]   ╰─> "))
            printf(Panel(f"[italic white]Sedang Mengirimkan Likes, Kamu Bisa Mengubah Key Jika Bypass Recaptcha Sudah Tidak Berhasil. Gunakan[italic green] CTRL + C[italic white] Jika Stuck Dan[italic red] CTRL + Z[italic white] Untuk Berhenti!", width=66, style="bold dark_goldenrod", title=">>> [Catatan] <<<"))
            while True:
                try:
                    self.PENGIRIMAN_LIKES(COOKIES['NAME'], self.id_like)
                except (KeyboardInterrupt):
                    printf(f"\r                                                    ", end='\r')
                    time.sleep(2.5)
                    continue
                except (RequestException):
                    printf(f"[bold dark_goldenrod]   ──>[bold red] KONEKSI KAMU BERMASALAH!", end='\r')
                    time.sleep(10.0)
                    continue
                except (Exception) as e:
                    printf(f"[bold dark_goldenrod]   ──>[bold red] {str(e).upper()}!", end='\r')
                    time.sleep(5.0)
                    continue
        except (Exception) as e:
            printf(Panel(f"[italic red]{type(e).__name__} : {str(e).title()}!", width=66, style="bold dark_goldenrod", title=">>> [Error] <<<"))
            exit()

def BANNER():
    os.system('cls' if os.name == 'nt' else 'clear')
    printf(Panel("""[bold red]● [bold yellow]● [bold green]●
[bold red] _________                       _____      _   __             
|  _   _  |                     |_   _|    (_) [  |  _         
|_/ | | \_|,--.   _ .--.   .--./) | |      __   | | / ] .---.  
    | |   `'_\ : [ `.-. | / /'`\; | |   _ [  |  | '' < / /__\\\\ 
   _| |_  // | |, | | | | \ \._//_| |__/ | | |  | |`\ \| \__., 
[bold white]  |_____| \\'-;__/[___||__].',__`|________|[___][__|  \_]'.__.' 
                         ( ( __))                              
            Free Facebook Likes - Coded by Rozhak""", width=66, style="bold dark_goldenrod"))
    return ("0_0")

class BYPASS:

    def __init__(self) -> None:
        pass

    def RECAPTCHA(self, sitekey): # Register here <https://multibot.in/dashboard/signup.php> and change the key!
        self.key = ("YOUR KEY!")
        response = requests.get(f'http://api.multibot.in/in.php?key={self.key}&method=userrecaptcha&googlekey={sitekey}&pageurl=https://tanglike.biz/hacklike.php')
        if 'ERROR_ZERO_BLANCE' in str(response.text):
            printf(Panel(f"[italic red]Kamu Harus Mengganti Key MultiBot Dengan Yang Baru, Silahkan Registerasi Dan Ubah Key Ini Dengan Key Yang Kamu Punya!", width=66, style="bold dark_goldenrod", title=">>> [Saldo Habis] <<<"))
            exit()
        self.status, self.id = str(response.text).split('|')[0], str(response.text).split('|')[1]
        if 'OK' in str(response.text):
            while True:
                response2 = requests.get(f'http://api.multibot.in/res.php?key={self.key}&id={self.id}')
                if 'OK|' in str(response2.text):
                    return (str(response2.text).split('|')[1])
                elif 'CAPCHA_NOT_READY' in str(response2.text):
                    printf(f"[bold dark_goldenrod]   ──>[bold green] SEDANG MELAKUKAN BYPASS RECAPTCHA!     ", end='\r')
                    time.sleep(2.5)
                    for sleep in range(60, 0, -1):
                        time.sleep(1.0)
                        printf(f"[bold dark_goldenrod]   ──>[bold white] TUNGGU[bold green] {sleep}[bold white] DETIK...                  ", end='\r')
                    continue
                else:
                    self.RECAPTCHA(sitekey)
        else:
            printf(f"[bold dark_goldenrod]   ──>[bold red] RECAPTCHA TIDAK DITEMUKAN!          ", end='\r')
            time.sleep(7.5)
            self.RECAPTCHA(sitekey)

if __name__ == '__main__':
    try:
        if os.path.exists("Penyimpanan/Youtube.json") == False:
            youtube_url = json.loads(requests.get('https://raw.githubusercontent.com/RozhakXD/TangLike/main/Penyimpanan/Subscribe.json').text)['Link']
            os.system(f'xdg-open {youtube_url}')
            with open('Penyimpanan/Youtube.json', 'w') as w:
                w.write(json.dumps({
                    "Status": True
                }))
            w.close()
            time.sleep(2.5)
        os.system('git pull')
        KIRIMKAN().MAIN()
    except (Exception) as e:
        printf(Panel(f"[italic red]{type(e).__name__} : {str(e).title()}!", width=66, style="bold dark_goldenrod", title=">>> [Error] <<<"))
        exit()
    except (KeyboardInterrupt):
        exit()
